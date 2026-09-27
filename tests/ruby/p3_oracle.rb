# P3 の差分テスト用オラクル。ruby -r で先に読み込ませ、Ruby 版 tecsgen のモデルと、
# Python 版をオフラインで動かすのに要る外界とのやりとりを、標準エラー出力に
# "@@P3 <JSON>" の形で1件1行で書き出す。
#
# 使い方: ruby -r <このファイル> tecsgen.rb <引数>...
#         （tests/ruby/ruby-p3-oracle を generate_golden.py の --ruby に渡す）
#
# 記録するもの:
#   {"ev":"env", "cwd":..., "argv":[...], "base":$tecsgen_base_path, "env":{...}}  起動時
#   {"ev":"fs", "op":"exist?"|"directory?"|"file?"|"readable?", "cwd":..., "path":..., "r":bool}
#   {"ev":"dir", "cwd":..., "path":..., "r":[名前...] | null}                     Dir.foreach
#   {"ev":"read", "cwd":..., "path":..., "data":中身 | null}                       File.open(読み)・File.read 等
#   {"ev":"popen", "cwd":..., "cmd":..., "data":出力 | null}                        IO.popen（import_C の cpp）
#   {"ev":"plugin", "name":..., "super":...}                                         PluginModule#load_plugin
#   {"ev":"model", "at":"parse"|"sem1"|"sem2", "out":標準出力のバイト数, "n_error":..,
#    "n_warning":.., "dump":モデル}                                                   チェックポイント
#   {"ev":"exit", "out":標準出力のバイト数, "error":例外クラス名 | null}              終了時
#
# 文字列はバイト列をそのまま latin-1 として JSON にする（P2 と同じ）。
#
# モデルのダンプ（Python 側は tests/p3_model_dump.py）:
#   nil・true・false・Integer → そのまま、Float → {"f": 数値 | "NaN" | "Infinity" | "-Infinity"}
#   String → 文字列、Symbol → {"y": 文字列}、Array → 配列、Hash → {"h": [[キー, 値]...]}
#   Class・Module → {"cls": 名前}
#   tecslib のクラスのオブジェクト → {"c": クラス名, "iv": {インスタンス変数名(@抜き): 値}}
#     インスタンス変数は名前順に辿る。2回目以降に出会ったものは {"ref": 出会った順の番号}
#   パーサ（Racc::Parser の子孫）と、それ以外のクラスのオブジェクト → {"c": クラス名}
#   ルート: {"root": TECSGEN の @root_namespace, "cv": {クラス名: {クラス変数名(@@抜き): 値}}}
#     cv は tecslib で定義されたクラス・モジュールのクラス変数（自分が持つものだけ）を、クラス名順に
require "json"
require "stringio"

module P3Oracle
  @active = true
  @out_bytes = 0
  class << self
    attr_accessor :active, :out_bytes
  end

  def self.emit(h)
    $stderr.write("@@P3 " + JSON.generate(h, max_nesting: false) + "\n")
  end

  def self.bytes(s)
    s.to_s.b.force_encoding("ISO-8859-1").encode("UTF-8")
  end

  def self.pwd
    bytes(Dir.pwd)
  end

  # Ruby 自身（require・rubygems）が調べるファイルは記録しない
  def self.noise?(path)
    s = path.to_s
    s.start_with?("/usr/lib/ruby/", "/var/lib/gems/") || s.include?("/.gem/") ||
      s.end_with?(".rb", ".so", ".gemspec")
  end

  # tecsgen の内部状態として比べないクラス（P1 で検証済みの静的な表など）
  SKIP_CV = %w[TECSMsg].freeze

  # tecslib で定義されたクラス・モジュールか
  def self.tecslib?(mod)
    name = mod.name
    return false if name.nil?
    loc = begin
      Object.const_source_location(name)
    rescue StandardError
      nil
    end
    # tecslib の下と、TECSGEN を最初に定義するトップの tecsgen.rb
    !loc.nil? && !loc.empty? && (loc[0].to_s.include?("/tecslib/") || loc[0].to_s.end_with?("/tecsgen/tecsgen.rb"))
  end

  class Dumper
    def initialize
      @seen = {}
      @tecslib = {}
    end

    def tecslib_class?(klass)
      return @tecslib[klass] if @tecslib.key?(klass)
      k = klass
      found = false
      while k
        if P3Oracle.tecslib?(k)
          found = true
          break
        end
        k = k.superclass
      end
      @tecslib[klass] = found
    end

    def dump(v)
      case v
      when nil, true, false, Integer then v
      when Float
        if v.nan? then { "f" => "NaN" }
        elsif v.infinite? then { "f" => (v > 0 ? "Infinity" : "-Infinity") }
        else { "f" => v }
        end
      when String then P3Oracle.bytes(v)
      when Symbol then { "y" => P3Oracle.bytes(v) }
      when Array then v.map { |e| dump(e) }
      when Hash then { "h" => v.map { |k, e| [dump(k), dump(e)] } }
      when Module then { "cls" => v.name.to_s }
      else dump_object(v)
      end
    end

    def dump_object(v)
      klass = v.class
      if defined?(Racc::Parser) && v.is_a?(Racc::Parser)
        return { "c" => klass.name.to_s }
      end
      return { "c" => klass.name.to_s } unless tecslib_class?(klass)
      if @seen.key?(v.object_id)
        return { "ref" => @seen[v.object_id] }
      end
      @seen[v.object_id] = @seen.size
      iv = {}
      v.instance_variables.sort.each do |name|
        iv[name.to_s.delete_prefix("@")] = dump(v.instance_variable_get(name))
      end
      { "c" => klass.name.to_s, "iv" => iv }
    end
  end

  def self.dump_model(root)
    d = Dumper.new
    top = d.dump(root)
    classes = ObjectSpace.each_object(Module).select { |m| tecslib?(m) }.sort_by { |m| m.name }
    cv = {}
    classes.each do |m|
      next if SKIP_CV.include?(m.name)
      vars = m.class_variables(false).sort
      next if vars.empty?
      h = {}
      vars.each { |name| h[name.to_s.delete_prefix("@@")] = d.dump(m.class_variable_get(name)) }
      cv[m.name] = h
    end
    { "root" => top, "cv" => cv }
  end

  def self.checkpoint(at, root)
    $stdout.flush
    # オラクル自身の失敗で tecsgen の挙動を変えないよう、例外は記録して握りつぶす
    begin
      dump = dump_model(root)
    rescue Exception => e
      emit(ev: "oracle_error", at: at, error: "#{e.class}: #{e.message}")
      return
    end
    emit(ev: "model", at: at, out: out_bytes,
         n_error: Generator.get_n_error, n_warning: Generator.get_n_warning,
         dump: dump)
  end

  # 標準出力に書いたバイト数を数える（チェックポイントまでの出力を正解データの stdout から切り出すため）
  module CountWrite
    def write(*args)
      P3Oracle.out_bytes += args.sum { |a| a.to_s.bytesize }
      super
    end
  end

  module FileHooks
    %i[exist? directory? file? readable?].each do |op|
      define_method(op) do |path|
        r = super(path)
        if P3Oracle.active && !P3Oracle.noise?(path)
          P3Oracle.emit(ev: "fs", op: op.to_s, cwd: P3Oracle.pwd, path: P3Oracle.bytes(path), r: r)
        end
        r
      end
    end
  end

  module DirHooks
    def foreach(path, *rest, &blk)
      names = begin
        Dir.entries(path, *rest)  # foreach と同じ readdir 順。super の Enumerator はこのフックに戻ってくる
      rescue SystemCallError
        nil
      end
      P3Oracle.emit(ev: "dir", cwd: P3Oracle.pwd, path: P3Oracle.bytes(path),
                    r: names && names.map { |n| P3Oracle.bytes(n) })
      raise Errno::ENOENT, path.to_s if names.nil?
      return names.each unless blk
      names.each(&blk)
      nil
    end
  end

  module IOHooks
    def popen(cmd, *rest, &blk)
      data = begin
        super(cmd, *rest) { |io| io.read }
      rescue SystemCallError
        nil
      end
      P3Oracle.emit(ev: "popen", cwd: P3Oracle.pwd, cmd: P3Oracle.bytes(cmd), data: data && P3Oracle.bytes(data))
      raise Errno::ENOENT, cmd.to_s if data.nil?
      io = StringIO.new(data.b)
      return io unless blk
      blk.call(io)
    end
  end

  # 読み込み用に開いたファイルの中身を記録する。書き込み用は記録しない（Python 版も自分で書く）
  module FileOpenHooks
    def open(path, mode = "r", *rest, **kw, &blk)
      if path.is_a?(String) && mode.to_s.start_with?("r") && P3Oracle.active && !P3Oracle.noise?(path)
        data = File.binread(path) rescue nil
        P3Oracle.emit(ev: "read", cwd: P3Oracle.pwd, path: P3Oracle.bytes(path),
                      data: data && P3Oracle.bytes(data))
      end
      super
    end
  end

  module PluginHooks
    def load_plugin(plugin_name, superClass)
      P3Oracle.emit(ev: "plugin", name: P3Oracle.bytes(plugin_name), super: superClass.to_s)
      super
    end
  end

  module TecsgenHooks
    def syntax_analisys(argv)
      super
      P3Oracle.checkpoint("parse", @root_namespace)
    end

    def semantics_analisys_1
      super
      P3Oracle.checkpoint("sem1", @root_namespace)
    end

    def semantics_analisys_2
      super
      P3Oracle.checkpoint("sem2", @root_namespace)
    end
  end

  def self.install_late
    PluginModule.prepend(PluginHooks)
    TECSGEN.prepend(TecsgenHooks)
    # オプション解析と setup の結果（Python 版の同じ処理と比べる）
    emit(ev: "globals", argv: ARGV.map { |a| bytes(a) }, base: bytes($tecsgen_base_path),
         tecspath: bytes($tecspath), import_path: $import_path.map { |p| bytes(p) },
         run_dir: bytes($run_dir), gen: bytes($gen), target: bytes($target),
         define: $define.map { |d| bytes(d) }, cpp: bytes($cpp))
  end
end

$stdout.singleton_class.prepend(P3Oracle::CountWrite)
File.singleton_class.prepend(P3Oracle::FileHooks)
File.singleton_class.prepend(P3Oracle::FileOpenHooks)
Dir.singleton_class.prepend(P3Oracle::DirHooks)
IO.singleton_class.prepend(P3Oracle::IOHooks)

P3Oracle.emit(ev: "env", cwd: P3Oracle.pwd, argv: ARGV.map { |a| P3Oracle.bytes(a) },
              env: ENV.to_h.select { |k, _| k =~ /\A(LANG|LC_ALL|LC_CTYPE|TECS\w*|TECSGEN\w*)\z/ }
                      .transform_values { |v| P3Oracle.bytes(v) })

# モデルの全クラスが読み込まれた後（TECSGEN.init の後、run1 の前）に差し込む
TracePoint.new(:call) do |tp|
  next unless tp.method_id == :run1 && tp.defined_class.name == "TECSGEN"
  tp.disable
  P3Oracle.install_late
end.enable

at_exit do
  err = $!
  $stdout.flush
  P3Oracle.emit(ev: "exit", out: P3Oracle.out_bytes,
                error: (err.nil? || err.is_a?(SystemExit)) ? nil : err.class.to_s,
                status: err.is_a?(SystemExit) ? err.status : nil)
end
