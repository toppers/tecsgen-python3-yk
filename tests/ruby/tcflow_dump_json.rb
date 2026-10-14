# tcflow が書いた関数リスト（Marshal 形式の tcflow.rbdmp）を、Python 版の tcflow.json と同じ
# 構造の JSON にして標準出力へ書く。差分テストの正解データを採るために使う。
#
# 使い方: ruby tcflow_dump_json.rb <移植元 tecsgen ディレクトリ> <tcflow.rbdmp>
#
# 文字列は、バイト列を latin-1 で復号した表現にそろえる（Python 版の内部表現と同じ）。
require "json"

src, dump = ARGV.fetch(0), ARGV.fetch(1)
require File.join(src, "flowlib", "classes.rb")

def latin1(s)
  s.nil? ? nil : s.to_s.dup.force_encoding("ISO-8859-1").encode("UTF-8")
end

list = TCFlow::Function.load_funclist(dump)
out = {}
list.each do |name, f|
  unless f.instance_of?(TCFlow::Function)
    out[latin1(name)] = f
    next
  end
  ivar = ->(n) { f.instance_variable_get(n) }
  out[latin1(name)] = {
    "param_var" => ivar.(:@param_var).keys.map { |k| latin1(k) },
    "local_var" => ivar.(:@local_var).keys.map { |k| latin1(k) },
    "global_var" => ivar.(:@global_var).to_h { |k, v| [latin1(k), v] },
    "call_func" => ivar.(:@call_func).to_h { |k, v| [latin1(k), v.instance_of?(TCFlow::Function) ? latin1(k) : 0] },
    "b_ref" => ivar.(:@b_ref),
    "locale" => ivar.(:@locale).map { |x| x.is_a?(String) ? latin1(x) : x },
  }
end
puts JSON.generate(out)
