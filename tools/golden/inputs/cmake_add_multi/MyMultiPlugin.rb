class MyMultiCelltypePlugin < CelltypePlugin
  def initialize( celltype, option )
    super
    TECSGEN::CMake.add_source( "multi_plugin.c" )
    TECSGEN::CMake.add_define( "K_MULTI=1" )
    TECSGEN::CMake.add_include( "inc_multi" )
    TECSGEN::CMake.add_line( "# from multi" )
  end
end

class MyMultiPlugin < MultiPlugin
  def self.get_plugin superClass
    if superClass == CelltypePlugin then
      return MyMultiCelltypePlugin
    else
      return nil
    end
  end
end
