# P2 の差分テスト用オラクル。ruby -r で先に読み込ませ、Ruby 版 tecsgen の構文解析の経過を
# 標準エラー出力に "@@P2 <JSON>" の形で1件1行で書き出す。
#
# 使い方: ruby -r <このファイル> tecsgen.rb <引数>...
#         （tests/ruby/ruby-p2-oracle を generate_golden.py の --ruby に渡す）
#
# Generator（CDL）と C_parser（import_C）の両方について、parse の呼び出しごとに次を記録する。
#   {"ev":"parse", "p":"cdl"|"c", "id":n, "files":[...]}   parse の開始
#   {"ev":"src",   "id":n, "file":名前, "data":中身 | null}   読むファイルの中身（読めなければ null）
#   {"ev":"q",     "id":n, "q":[[種別, 値, 位置]...]}          字句解析直後の @q（TYPE_NAME 置換前）
#   {"ev":"tok",   "id":n, "t":[種別, 値, 位置] | null}       next_token が返したトークン
#   {"ev":"red",   "id":n, "m":"_reduce_N"}                    アクションの呼び出し
#   {"ev":"err",   "id":n, "t":記号番号, "v":[種別, 値, 位置]}  on_error の呼び出し
#   {"ev":"abort", "id":n, "error":例外クラス名}                 例外による parse の中断
#   {"ev":"end",   "id":n}                                      parse の終了
# 値は [クラス名, 文字列] で表す。文字列はバイト列をそのまま latin-1 として JSON にする。
require "json"

module P2Oracle
  @next_id = 0
  @stack = []
  class << self
    attr_accessor :next_id, :stack
  end

  def self.emit(h)
    $stderr.write("@@P2 " + JSON.generate(h) + "\n")
  end

  def self.bytes(s)
    s.to_s.b.force_encoding("ISO-8859-1").encode("UTF-8")
  end

  def self.value(v)
    case v
    when Integer then ["Integer", v.to_s]
    when Symbol then ["Symbol", bytes(v.to_s)]
    when String then ["String", bytes(v)]
    when nil then ["NilClass", ""]
    when false then ["FalseClass", ""]
    else [v.class.to_s, bytes(v.to_s)]
    end
  end

  def self.token(tok)
    return nil if tok.nil? || tok == false
    kind, t = tok
    return [value(kind), nil, nil] unless t.respond_to?(:locale)
    loc = t.locale
    [value(kind), value(t.val), [bytes(loc[0]), loc[1], loc[2]]]
  end

  def self.current
    stack.last
  end

  module Hooks
    def parse(files)
      id = (P2Oracle.next_id += 1)
      P2Oracle.stack.push(id)
      P2Oracle.emit(ev: "parse", p: (is_a?(Generator) ? "cdl" : "c"), id: id,
                    files: Array(files).map { |f| P2Oracle.bytes(f) })
      # 字句解析の差分テストを移植元のソースなしで行えるよう、読むファイルの中身も残す
      Array(files).each do |f|
        data = File.binread(f.to_s) rescue nil
        P2Oracle.emit(ev: "src", id: id, file: P2Oracle.bytes(f), data: data && P2Oracle.bytes(data))
      end
      begin
        super
      rescue Exception => e
        # アクションの中の例外（SystemStackError など）で parse が中断した
        P2Oracle.emit(ev: "abort", id: id, error: e.class.to_s)
        raise
      ensure
        P2Oracle.emit(ev: "end", id: id)
        P2Oracle.stack.pop
      end
    end

    def do_parse
      P2Oracle.emit(ev: "q", id: P2Oracle.current, q: @q.map { |t| P2Oracle.token(t) })
      super
    end

    def next_token
      tok = super
      P2Oracle.emit(ev: "tok", id: P2Oracle.current, t: P2Oracle.token(tok))
      tok
    end

    def on_error(t, v, vstack)
      tok = v.respond_to?(:locale) ? [nil, v] : nil
      P2Oracle.emit(ev: "err", id: P2Oracle.current, t: t,
                    v: tok ? P2Oracle.token(tok) : P2Oracle.value(v))
      super
    end
  end

  def self.install(klass)
    return if klass.ancestors.include?(Hooks)
    reducers = Module.new do
      klass.instance_methods(false).grep(/\A_reduce_/).each do |m|
        define_method(m) do |*args|
          P2Oracle.emit(ev: "red", id: P2Oracle.current, m: m.to_s)
          super(*args)
        end
      end
    end
    klass.prepend(Hooks)
    klass.prepend(reducers)
  end
end

# Generator・C_parser のクラス定義（racc が生成した *.tab.rb）の読み込みが終わった時点で差し込む
TracePoint.new(:end) do |tp|
  name = tp.self.is_a?(Class) ? tp.self.name : nil
  next unless %w[Generator C_parser].include?(name)
  next unless tp.self.instance_methods(false).any? { |m| m.to_s.start_with?("_reduce_") }
  P2Oracle.install(tp.self)
end.enable
