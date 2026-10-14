"""tecsmerge の正解データを Ruby 版から採取する。

WSL（Linux）上で実行することを前提とする。標準ライブラリだけで動く。

    python3 tools/golden/collect_tecsmerge.py \\
        --tecsgen-wc /mnt/e/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033 \\
        --out tests/golden/tecsmerge

入力のテンプレートは tests/golden/cases/ にある tecsgen の生成物（`*_templ.c`・`*_templ.h`）を使い、
保守中のファイル（コピー先）はそこから作る（関数本体の編集・関数の削除・キーワード行の欠落など）。
シナリオごとに、作業ディレクトリで Ruby 版の tecsmerge.rb を実行し、標準出力・標準エラー出力・終了コード・
実行後のファイル一式（バックアップ `_1` を含む）を保存する。Windows の Ruby は改行を変換するので使わない。
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CASES = ROOT / "tests" / "golden" / "cases"
USER_LINE = "  /* user edit */\n"


def pick_templates() -> list[Path]:
    """ENTRY_FUNC を持つテンプレートを、種類（.c と inline の .h）が混ざるよう決まった順で選ぶ。"""
    found = sorted(
        p
        for pat in ("*_templ.c", "*_templ.h")
        for p in CASES.glob(f"**/gen/{pat}")
        if b"#[<ENTRY_FUNC>]#" in p.read_bytes()
    )
    cs = [p for p in found if p.suffix == ".c"]
    hs = [p for p in found if p.suffix == ".h"]
    pick: list[Path] = []
    for group, n in ((cs, 4), (hs, 2)):
        step = max(1, len(group) // n)
        pick += group[::step][:n]
    return pick


def edit_old(text: str) -> str:
    """保守中のファイルを模す: 関数本体の先頭にユーザの行を足し、冒頭と末尾にも書き足す。"""
    out: list[str] = []
    for line in text.splitlines(keepends=True):
        out.append(line)
        if line.startswith("{"):
            out.append(USER_LINE)
    return "// old head\n" + "".join(out) + "/* old tail */\n"


def ports_and_funcs(text: str) -> tuple[list[str], list[str]]:
    ports = re.findall(r"^/\* #\[<ENTRY_PORT>\]#\s*(\w*)", text, re.MULTILINE)
    funcs = re.findall(r"^/\* #\[<ENTRY_FUNC>\]#\s*(\w*)", text, re.MULTILINE)
    return ports, funcs


def scenarios() -> list[dict]:
    out: list[dict] = []
    for n, t in enumerate(pick_templates()):
        raw = t.read_bytes().decode("latin-1")
        # ファイル名はケース名を含めずに揃える（テンプレート名はセルタイプ名）
        name = t.name.replace("_templ", "")
        tname = t.name
        tag = f"t{n}_{name.replace('.', '_')}"
        ports, funcs = ports_and_funcs(raw)
        p0 = ports[0]
        p0funcs = [f for f in funcs if f.startswith(p0 + "_")]
        base = {"src/" + tname: raw, "dst/" + name: edit_old(raw)}
        out.append(
            {"name": f"{tag}_merge", "files": base, "argv": ["src/" + tname, "dst"]}
        )
        out.append(
            {
                "name": f"{tag}_merge_oldmode",
                "files": base,
                "argv": ["-o", "src/" + tname, "dst"],
            }
        )
        out.append(
            {
                "name": f"{tag}_copy_new",
                "files": {"src/" + tname: raw, "dst/.keep": ""},
                "argv": ["src/" + tname, "dst"],
            }
        )
        out.append(
            {
                "name": f"{tag}_exist_only",
                "files": {"src/" + tname: raw, "dst/.keep": ""},
                "argv": ["-e", "src/" + tname, "dst"],
            }
        )
        # 受け口名の変更: テンプレート側を新しい名前にする
        new_p = p0 + "New"
        renamed = raw.replace(f"#[<ENTRY_PORT>]# {p0}", f"#[<ENTRY_PORT>]# {new_p}")
        renamed = re.sub(rf"\b{p0}_", f"{new_p}_", renamed)
        out.append(
            {
                "name": f"{tag}_rename_port",
                "files": {"src/" + tname: renamed, "dst/" + name: edit_old(raw)},
                "argv": ["-s", "-p", f"{p0}:{new_p}", "src/" + tname, "dst"],
            }
        )
        if p0funcs:
            f0 = p0funcs[0][len(p0) + 1 :]
            f1 = f0 + "_v2"
            renamed_f = raw.replace(f"{p0}_{f0}", f"{p0}_{f1}")
            out.append(
                {
                    "name": f"{tag}_rename_func",
                    "files": {"src/" + tname: renamed_f, "dst/" + name: edit_old(raw)},
                    "argv": ["-s", "-p", p0, "-f", f"{f0}:{f1}", "src/" + tname, "dst"],
                }
            )
            out.append(
                {
                    "name": f"{tag}_rename_both",
                    "files": {
                        "src/" + tname: renamed.replace(
                            f"{new_p}_{f0}", f"{new_p}_{f1}"
                        ),
                        "dst/" + name: edit_old(raw),
                    },
                    "argv": [
                        "-p",
                        f"{p0}:{new_p}",
                        "-f",
                        f"{f0}:{f1}",
                        "src/" + tname,
                        "dst",
                    ],
                }
            )
            # 削除された関数・受け口: コピー先に、テンプレートに無い関数と受け口を足す
            extra = edit_old(raw).replace(
                "/* #[<POSTAMBLE>]#",
                "/* #[<ENTRY_PORT>]# gone\n * #[</ENTRY_PORT>]# */\n/* #[<ENTRY_FUNC>]# gone_x\n"
                " * #[</ENTRY_FUNC>]# */\n{\n}\n/* #[<POSTAMBLE>]#",
            )
            out.append(
                {
                    "name": f"{tag}_deleted",
                    "files": {"src/" + tname: raw, "dst/" + name: extra},
                    "argv": ["src/" + tname, "dst"],
                }
            )
        # キーワード行の欠落（直前キーワード違反）
        broken = edit_old(raw).replace(" * #[</ENTRY_PORT>]# */\n", "", 1)
        out.append(
            {
                "name": f"{tag}_broken_order",
                "files": {"src/" + tname: raw, "dst/" + name: broken},
                "argv": ["src/" + tname, "dst"],
                "crash_ok": True,
            }
        )
        # ディレクトリ指定
        out.append(
            {
                "name": f"{tag}_dir_mode",
                "files": {
                    "src/" + tname: raw,
                    "src/other.txt": "x",
                    "dst/" + name: edit_old(raw),
                },
                "argv": ["src", "dst"],
            }
        )
        if n >= 1:
            continue
    # 引数・入力のエラー
    t = pick_templates()[0]
    raw = t.read_bytes().decode("latin-1")
    out += [
        {"name": "err_no_args", "files": {}, "argv": []},
        {"name": "err_one_arg", "files": {"d/.keep": ""}, "argv": ["d"]},
        {
            "name": "err_not_templ",
            "files": {"src/a.c": "x", "dst/.keep": ""},
            "argv": ["src/a.c", "dst"],
        },
        {
            "name": "err_dst_missing",
            "files": {"src/a_templ.c": raw},
            "argv": ["src/a_templ.c", "nodir"],
        },
        {
            "name": "err_dst_not_dir",
            "files": {"src/a_templ.c": raw, "f": "x"},
            "argv": ["src/a_templ.c", "f"],
        },
        {
            "name": "err_src_missing",
            "files": {"dst/.keep": ""},
            "argv": ["nosuch_templ.c", "dst"],
        },
        {
            "name": "err_func_before_port",
            "files": {"src/a_templ.c": raw, "dst/.keep": ""},
            "argv": ["-f", "a:b", "src/a_templ.c", "dst"],
            "crash_ok": True,
        },
        {
            "name": "err_func_same_name",
            "files": {"src/a_templ.c": raw, "dst/.keep": ""},
            "argv": ["-p", "x", "-f", "a:a", "src/a_templ.c", "dst"],
        },
        {
            "name": "err_func_duplicate",
            "files": {"src/a_templ.c": raw, "dst/.keep": ""},
            "argv": ["-p", "x", "-f", "a:b", "-f", "a:c", "src/a_templ.c", "dst"],
        },
        {
            "name": "err_rename_not_found",
            "files": {"src/a_templ.c": raw, "dst/a.c": edit_old(raw)},
            "argv": [
                "-p",
                "nosuch:other",
                "-p",
                "zz",
                "-f",
                "q:r",
                "src/a_templ.c",
                "dst",
            ],
        },
        {"name": "help", "files": {}, "argv": ["--help"]},
        {"name": "version", "files": {}, "argv": ["--version"]},
        {
            "name": "err_invalid_option",
            "files": {},
            "argv": ["--nosuch"],
        },
    ]
    return out + edge_scenarios()


def edge_scenarios() -> list[dict]:
    """周辺ケース: 複数ソース・長いオプション形・省略形・引数の欠けたオプション・名前の取り違え。"""
    pick = pick_templates()
    ta, tb = pick[0], pick[-1]
    ra, rb = ta.read_bytes().decode("latin-1"), tb.read_bytes().decode("latin-1")
    na, nb = ta.name.replace("_templ", ""), tb.name.replace("_templ", "")
    pa = ports_and_funcs(ra)[0][0]
    two = {
        "src/" + ta.name: ra,
        "src/" + tb.name: rb,
        "dst/" + na: edit_old(ra),
        "dst/" + nb: edit_old(rb),
    }
    one = {"src/" + ta.name: ra, "dst/" + na: edit_old(ra)}
    sa = "src/" + ta.name
    return [
        {"name": "x_multi_src", "files": two, "argv": [sa, "src/" + tb.name, "dst"]},
        {"name": "x_multi_src_dir_file", "files": two, "argv": ["src", sa, "dst"]},
        {
            "name": "x_multi_src_second_missing",
            "files": two,
            "argv": [sa, "src/nosuch_templ.c", "dst"],
        },
        {
            "name": "x_long_opts",
            "files": {**one, "dst2/.keep": ""},
            "argv": [
                "--exist-only",
                "--old-mode",
                "--show_change_set",
                f"--port={pa}:{pa}X",
                sa,
                "dst",
            ],
        },
        {
            "name": "x_abbrev_opts",
            "files": one,
            "argv": ["--exist", "--old", "--show", sa, "dst"],
        },
        {"name": "x_abbrev_ambiguous", "files": one, "argv": ["--e", sa, "dst"]},
        {"name": "x_show_only", "files": one, "argv": ["-s", sa, "dst"]},
        {"name": "x_double_dash", "files": one, "argv": ["--", sa, "dst"]},
        {"name": "x_opt_after_args", "files": one, "argv": [sa, "dst", "-o"]},
        {"name": "x_port_no_new", "files": one, "argv": ["-p", pa + ":", sa, "dst"]},
        {"name": "x_port_no_old", "files": one, "argv": ["-p", ":b", sa, "dst"]},
        {"name": "x_port_missing_arg", "files": one, "argv": [sa, "dst", "-p"]},
        {
            "name": "x_port_twice",
            "files": one,
            "argv": ["-p", f"{pa}:b", "-p", f"{pa}:c", sa, "dst"],
        },
        {
            "name": "x_func_three_parts",
            "files": one,
            "argv": ["-p", pa, "-f", "a:b:c", sa, "dst"],
        },
        {
            "name": "x_templ_regex_dot",
            "files": {"src/a_templXc": ra, "dst/.keep": ""},
            "argv": ["src", "dst"],
        },
        {
            "name": "x_dir_exist_only_merge",
            "files": two,
            "argv": ["-e", "src", "dst"],
        },
        {
            "name": "x_backup_second",
            "files": {**one, "dst/" + na + "_1": "old backup\n"},
            "argv": [sa, "dst"],
        },
        {
            "name": "x_src_empty_dir",
            "files": {"src/.keep": "", "dst/.keep": ""},
            "argv": ["src", "dst"],
        },
    ]


def snapshot(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)).replace("\\", "/"): p.read_bytes().decode("latin-1")
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tecsgen-wc", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    ruby_script = Path(args.tecsgen_wc) / "tecsgen" / "tecsmerge.rb"
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    names: set[str] = set()
    for sc in scenarios():
        assert sc["name"] not in names, sc["name"]
        names.add(sc["name"])
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            for rel, content in sc["files"].items():
                f = work / rel
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_bytes(content.encode("latin-1"))
            before = snapshot(work)
            r = subprocess.run(
                ["ruby", str(ruby_script), *sc["argv"]],
                cwd=work,
                capture_output=True,
                check=False,
            )
            after = snapshot(work)
        data = {
            "argv": sc["argv"],
            "input": before,
            "stdout": r.stdout.decode("latin-1"),
            "stderr": r.stderr.decode("latin-1"),
            "returncode": r.returncode,
            "tree": after,
            "crash_ok": sc.get("crash_ok", False),
        }
        (out / f"{sc['name']}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        print(f"{sc['name']}: exit {r.returncode}")


if __name__ == "__main__":
    main()
