# Synthetic celltype plugin that calls every TECSGEN::CMake.add_* method.
# (ASCII only. See README.md in this directory.)
class MyCMakePlugin < CelltypePlugin
  def initialize( celltype, option )
    super
    TECSGEN::CMake.add_source( "plugin_a.c" )
    TECSGEN::CMake.add_source( "plugin_a.c" )
    TECSGEN::CMake.add_source( :sym_b )
    TECSGEN::CMake.add_include( "$(BASE_DIR)/inc" )
    TECSGEN::CMake.add_include( "/abs/path\\win" )
    TECSGEN::CMake.add_define( "FOO=1" )
    TECSGEN::CMake.add_define( 42 )
    TECSGEN::CMake.add_link_option( "-Wl,--gc-sections" )
    TECSGEN::CMake.add_custom_command( "add_custom_command(OUTPUT x COMMAND y)" )
    TECSGEN::CMake.add_line( "# line1" )
    TECSGEN::CMake.add_line( "set(X 1)" )
    TECSGEN::CMake.add_line( "# line1" )
  end

  def new_cell( cell )
    TECSGEN::CMake.add_source( "from_new_cell.c" )
  end

  # gen_cmake_tecsgen runs at the start of generate, so this call is too late
  # to appear in CMakeLists.tecsgen.cmake.
  def gen_factory( file )
    TECSGEN::CMake.add_source( "too_late.c" )
  end
end
