# P1 の差分テスト用オラクル。Ruby 版 tecsgen のソースを読み込み、Python 版と同じ入力に対する
# Ruby 版の結果を JSON で返す。
#
# 使い方: ruby p1_oracle.rb <移植元 tecsgen ディレクトリ> <cases.json>
# 作業コピーが CRLF でも結果が変わらないよう、読み込むソースの CRLF を LF に直す。
require "json"
require "kconv"
require "stringio"

SRC = ARGV.fetch(0)

def load_src(rel)
  path = File.join(SRC, rel)
  src = File.binread(path).force_encoding("UTF-8").gsub("\r\n", "\n")
  eval(src, TOPLEVEL_BINDING, path)
end

# tecs_lang.rb のクラス本体が呼ぶトップレベル関数（tecsgen.rb で定義されている）
$debug = false
$IN_EXERB = false
$kcode = nil
def dbgPrint(str); end
def require_tecsgen_lib(fname, b_fatal = true)
  path = File.join(SRC, fname)
  return false unless File.exist?(path)
  load_src(fname)
  true
end

load_src("tecslib/core/messages.rb")

cases = JSON.parse(File.read(ARGV.fetch(1), encoding: "UTF-8"))
results = cases.map do |c|
  case c["kind"]
  when "lang"
    # ENV を差し替えて tecs_lang.rb のクラス本体を実行し直す
    saved = ENV.to_h
    %w[LANG TECSGEN_LANG TECSGEN_FILE_LANG TERM].each { |k| ENV.delete(k) }
    c["env"].each { |k, v| ENV[k] = v }
    $kcode = c["kcode"]
    begin
      # -k が不正なときの診断メッセージが結果の JSON に混ざらないよう、標準出力を退避する
      $stdout = StringIO.new
      load_src("tecslib/core/tecs_lang.rb")
      r = { "lang_file" => $LANG_FILE&.to_s, "charset_file" => $CHARSET_FILE&.to_s,
            "lang_console" => $LANG_CONSOLE&.to_s, "charset_console" => $CHARSET_CONSOLE&.to_s,
            "file_encode" => $Ruby19_File_Encode }
    rescue SystemExit => e
      r = { "exit" => e.status }
    ensure
      $stdout = STDOUT
      ENV.replace(saved)
    end
    r
  when "parse_lang"
    load_src("tecslib/core/tecs_lang.rb") unless defined?(TECS_LANG)
    TECS_LANG.parse_lang(c["lang"]).map { |x| x&.to_s }
  when "message"
    # Generator.error2 / warning2 のメッセージ組み立て部分（bnf.y.rb）と同じ処理
    load_src("tecslib/messages/messages_console_#{c["lang"]}.rb")
    msg = case c["type"]
          when "error" then TECSMsg.get_error_message(c["body"])
          when "warning" then TECSMsg.get_warning_message(c["body"])
          end
    begin
      count = 1
      c["args"].each { |a|
        str = a.to_s
        msg.sub!(/\$#{count}/, str)
        count += 1
      }
      msg
    rescue IndexError
      "!IndexError"   # 置換文字列の \k<name> が未定義の名前を指す
    end
  when "to_s"
    c["value"].to_s
  when "inspect"
    c["value"].inspect
  end
end
STDOUT.binmode
STDOUT.write(JSON.generate(results))
