class MyCompositePlugin < CompositePlugin
  def initialize( celltype, option )
    super
    TECSGEN::CMake.add_source( "composite_plugin.c" )
    TECSGEN::CMake.add_define( "K_COMPOSITE=1" )
    TECSGEN::CMake.add_include( "inc_composite" )
    TECSGEN::CMake.add_line( "# from composite" )
  end
end
