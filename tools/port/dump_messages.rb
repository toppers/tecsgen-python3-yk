# Ruby 版 tecsgen のメッセージ定義（tecslib/messages/messages_*.rb）を JSON に書き出す。
# 文字列リテラルのエスケープ解釈を Ruby 自身に任せるため、Python へは JSON 経由で渡す。
#
# 使い方: ruby dump_messages.rb <messages_*.rb>  > out.json
# 作業コピーが CRLF でも結果が変わらないよう、読み込み時に CRLF を LF に直す。
require "json"

class TECSMsg
end

path = ARGV.fetch(0)
src = File.binread(path).force_encoding("UTF-8").gsub("\r\n", "\n")
eval(src, TOPLEVEL_BINDING, path)

out = {}
TECSMsg.class_variables.sort.each do |cv|
  h = TECSMsg.class_variable_get(cv)
  out[cv.to_s.delete_prefix("@@")] = h.to_h { |k, v| [k.to_s, v] }
end
puts JSON.pretty_generate(out)
