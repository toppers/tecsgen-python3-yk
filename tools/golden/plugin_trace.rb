# frozen_string_literal: false
# tecsgen が実際にロード・生成したプラグインを記録する計測フック。
# RUBYOPT=-r<このファイル> TECS_PLUGIN_LOG=<ログのパス> で使う。ログが無ければ何もしない。
#   load\t<ファイル名>  : Kernel#load / require で読んだファイル
#   new\t<クラス名>     : Plugin の子クラスのインスタンスを作った
LOG = ENV["TECS_PLUGIN_LOG"]
if LOG && !LOG.empty?
  $__tecs_trace_log = lambda do |kind, name|
    begin
      File.open(LOG, "a") { |io| io.puts "#{kind}\t#{name}" }
    rescue StandardError
      nil
    end
  end

  module Kernel
    alias_method :__tecs_orig_load, :load
    def load(file, *rest)
      $__tecs_trace_log.call("load", File.basename(file.to_s))
      __tecs_orig_load(file, *rest)
    end
    private :load

    alias_method :__tecs_orig_require, :require
    def require(file)
      $__tecs_trace_log.call("load", File.basename(file.to_s))
      __tecs_orig_require(file)
    end
    private :require
  end

  TracePoint.new(:end) do |tp|
    klass = tp.self
    next unless klass.is_a?(Class)
    next unless defined?(::Plugin) && klass <= ::Plugin
    next if klass.instance_variable_get(:@__tecs_traced)
    klass.instance_variable_set(:@__tecs_traced, true)
    tracer = Module.new do
      define_method(:initialize) do |*args, &blk|
        $__tecs_trace_log.call("new", self.class.name)
        super(*args, &blk)
      end
      private :initialize
    end
    klass.prepend(tracer)
  end.enable
end
