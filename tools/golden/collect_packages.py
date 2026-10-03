"""Collect Ruby tecsgen plugin goldens from unpacked TECS-WG packages."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import sys
import tempfile
import tomllib
from pathlib import Path

from collect_kernel import (
    Normalizer,
    command_version,
    run_case,
    same_as_committed,
    svn_export,
)

DEFAULT_MANIFEST = Path(__file__).with_name("cases_packages.toml")


def inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes package: {relative}")
    return path


def cdl_hashes(root: Path) -> dict[str, str]:
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*.cdl"))
        if p.is_file()
    }


def trace_plugins(path: Path) -> tuple[list[str], list[str]]:
    if not path.exists():
        return [], []
    events = [
        line.split("\t", 1)
        for line in path.read_text(errors="replace").splitlines()
        if "\t" in line
    ]
    loaded = sorted({name for kind, name in events if kind == "load"})
    created = sorted({name for kind, name in events if kind == "new"})
    return loaded, created


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packages-root", type=Path, required=True)
    parser.add_argument("--tecsgen-wc", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--work", type=Path, default=Path.home() / "p5packageplugins")
    parser.add_argument("--case", action="append", default=[], help="case id glob")
    parser.add_argument(
        "--include-disabled", action="store_true", help="run diagnostic cases"
    )
    parser.add_argument(
        "--append", action="store_true", help="add only cases absent from output"
    )
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--p3-oracle",
        action="store_true",
        help="正解データは採り直さず、P3 オラクルを差し込んで実行し、記録を <out>/p3/<id>.jsonl.gz に書く"
        "（コミット済みの正解データと同じ出力になることを確かめる）。--case で対象を選ぶ",
    )
    opts = parser.parse_args(argv)

    cases = tomllib.loads(opts.manifest.read_text(encoding="utf-8"))["case"]
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        parser.error("duplicate case id")
    if not opts.include_disabled:
        cases = [case for case in cases if case.get("enabled", True)]
    if opts.case:
        cases = [
            case
            for case in cases
            if any(fnmatch.fnmatchcase(case["id"], pat) for pat in opts.case)
        ]
    if not cases:
        parser.error("no matching cases")

    root = opts.packages_root.resolve()
    out = opts.out.resolve()
    committed = out
    if opts.p3_oracle:
        # 正解データ本体は触らず、作業ディレクトリの下に採る
        out = (opts.work / "p3-scratch").resolve()
        shutil.rmtree(out, ignore_errors=True)
    previous: dict = {}
    if not opts.p3_oracle and out.exists() and any(out.iterdir()):
        if not opts.append or not opts.case:
            parser.error(f"output is not empty: {out}; use --append with --case")
        previous_path = out / "environment.json"
        if not previous_path.is_file():
            parser.error(f"missing environment.json in existing output: {out}")
        previous = json.loads(previous_path.read_text(encoding="utf-8"))
        for case in cases:
            if (out / "cases" / case["id"]).exists():
                parser.error(f"case already exists: {case['id']}")
    out.mkdir(parents=True, exist_ok=True)
    opts.work.mkdir(parents=True, exist_ok=True)
    trace_hook = Path(__file__).with_name("plugin_trace.rb").resolve()
    failed: list[str] = []
    errors: dict[str, str] = {}
    results: list[dict] = []

    with tempfile.TemporaryDirectory(prefix="package-golden-", dir=opts.work) as tmp:
        temporary = Path(tmp)
        tecsgen_src = temporary / "tecsgen-src"
        tecsgen_revision = svn_export(opts.tecsgen_wc / "tecsgen", tecsgen_src)
        pristine = temporary / "pristine"
        pristine.mkdir()
        revisions: dict[str, str] = {}
        inputs: dict[str, dict[str, str]] = {}
        for case in cases:
            package = case["package"]
            if package in revisions:
                continue
            package_root = inside(root, package)
            if not package_root.is_dir():
                raise FileNotFoundError(package_root)
            source = inside(package_root, case.get("source_subdir", "."))
            dest = pristine / package
            shutil.copytree(source, dest, symlinks=True)
            tecsgen_dest = inside(dest, case.get("tecsgen_dest", "tecsgen"))
            if tecsgen_dest.is_symlink() or tecsgen_dest.is_file():
                tecsgen_dest.unlink()
            elif tecsgen_dest.is_dir():
                shutil.rmtree(tecsgen_dest)
            tecsgen_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(tecsgen_src, tecsgen_dest, symlinks=True)
            for selected in (item for item in cases if item["package"] == package):
                workdir = selected.get("workdir", "obj-golden")
                for name in selected.get("clean", []):
                    clean_path = inside(dest, f"{workdir}/{name}")
                    if clean_path.is_dir():
                        shutil.rmtree(clean_path)
                    elif clean_path.exists():
                        clean_path.unlink()
            revisions[package] = package
            inputs[package] = cdl_hashes(source)

        run_root = temporary / "run"
        normalizer = Normalizer(run_root, tecsgen_src)
        for case in cases:
            package = case["package"]
            trace = temporary / "plugin-trace.log"
            trace.write_text("")
            previous_rubyopt = os.environ.get("RUBYOPT")
            previous_log = os.environ.get("TECS_PLUGIN_LOG")
            os.environ["RUBYOPT"] = f"-r{trace_hook}"
            os.environ["TECS_PLUGIN_LOG"] = str(trace)
            kernel_case = {**case, "repo": package}
            try:
                meta = run_case(
                    kernel_case,
                    pristine=pristine,
                    run_root=run_root,
                    out_dir=out,
                    normalize=normalizer,
                    revisions=revisions,
                    timeout=opts.timeout,
                    p3_log=(out / "p3-log" / f"{case['id']}.log")
                    if opts.p3_oracle
                    else None,
                )
            except (RuntimeError, OSError, ValueError) as exc:
                failed.append(case["id"])
                errors[case["id"]] = str(exc)
                print(f"ERROR {case['id']}: {exc}", file=sys.stderr)
                continue
            finally:
                if previous_rubyopt is None:
                    os.environ.pop("RUBYOPT", None)
                else:
                    os.environ["RUBYOPT"] = previous_rubyopt
                if previous_log is None:
                    os.environ.pop("TECS_PLUGIN_LOG", None)
                else:
                    os.environ["TECS_PLUGIN_LOG"] = previous_log
            loaded, created = trace_plugins(trace)
            case_dir = out / "cases" / case["id"]
            (case_dir / "plugin_trace.txt").write_bytes(trace.read_bytes())
            meta.update(
                package=package,
                source_subdir=case.get("source_subdir", "."),
                input_cdl_sha256=inputs[package],
                plugins_loaded=loaded,
                plugins_instantiated=created,
            )
            valid = (
                meta["exit_code"] == 0
                and meta["errors"] == 0
                and not meta["timed_out"]
                and bool(created)
                and bool(meta["created"] or meta["modified"])
            )
            meta["golden_valid"] = valid
            (case_dir / "meta.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            if not valid:
                failed.append(case["id"])
                diagnostic = out / "diagnostics" / case["id"]
                diagnostic.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(case_dir, diagnostic)
            print(
                f"{'OK' if valid else 'INCOMPLETE'} {case['id']}: exit={meta['exit_code']} plugins={created} files={len(meta['created']) + len(meta['modified'])}"
            )
            results.append(meta)

    if opts.p3_oracle:
        # 全件が正解データと同じ出力だったときだけ、記録をコミット対象の場所へ置く
        differing = []
        for case in cases:
            diff = same_as_committed(
                out, committed, case["id"], ignore=("meta.json", "plugin_trace.txt")
            )
            if diff:
                print(f"DIFFERS from committed golden: {case['id']}: {diff}")
                differing.append(case["id"])
        if failed or differing:
            return 1
        for rec in sorted((out / "p3").rglob("*.jsonl.gz")):
            target = committed / "p3" / rec.relative_to(out / "p3")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(rec, target)
        print(f"P3 records written to {committed / 'p3'}")
        return 0

    previous_failed = set(previous.get("failed", []))
    previous_failed.difference_update(case["id"] for case in cases)
    all_failed = sorted(previous_failed | set(failed))
    previous_errors = {
        key: value
        for key, value in previous.get("errors", {}).items()
        if key not in {case["id"] for case in cases}
    }
    environment = {
        "ruby": command_version(["ruby", "--version"]),
        "tecsgen_revision": tecsgen_revision,
        "manifest_sha256": hashlib.sha256(opts.manifest.read_bytes()).hexdigest(),
        "packages": sorted(set(previous.get("packages", [])) | set(revisions)),
        "cases": len(list((out / "cases").rglob("meta.json"))),
        "failed": all_failed,
        "errors": {**previous_errors, **errors},
    }
    (out / "environment.json").write_text(
        json.dumps(environment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
