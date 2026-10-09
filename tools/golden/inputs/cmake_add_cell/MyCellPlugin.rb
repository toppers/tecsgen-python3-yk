class MyCellPlugin < CellPlugin
  def initialize( cell, option )
    super
    TECSGEN::CMake.add_source( "cell_plugin.c" )
    TECSGEN::CMake.add_define( "K_CELL=1" )
    TECSGEN::CMake.add_include( "inc_cell" )
    TECSGEN::CMake.add_line( "# from cell" )
  end
end
