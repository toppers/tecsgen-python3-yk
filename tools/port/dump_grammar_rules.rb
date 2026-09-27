# racc の文法ファイル（bnf.y.rb・C_parser.y.rb）から、規則とアクションのソースを JSON に書き出す。
# アクションの骨格は tools/port/gen_action_stubs.py が作る。
#
# 使い方: ruby dump_grammar_rules.rb <*.y.rb>  > out.json
# 作業コピーが CRLF でも結果が変わらないよう、読み込み時に CRLF を LF に直す。
require "json"
require "racc/static"
require "racc/grammarfileparser"

path = ARGV.fetch(0)
src = File.binread(path).force_encoding("UTF-8").gsub("\r\n", "\n")
grammar = Racc::GrammarFileParser.new.parse(src, File.basename(path)).grammar
rules = grammar.each_rule.map do |r|
  action = r.action
  {
    ident: r.ident,
    target: r.target.to_s,
    symbols: r.symbols.map(&:to_s),
    action: action.empty? ? nil : action.source.text.dup.force_encoding("UTF-8"),
    lineno: action.empty? ? nil : action.source.lineno,
  }
end
puts JSON.generate(rules)
