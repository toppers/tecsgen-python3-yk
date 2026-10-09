class MySigPlugin < SignaturePlugin
  def initialize( signature, option )
    super
    TECSGEN::CMake.add_source( "signature_plugin.c" )
    TECSGEN::CMake.add_define( "K_SIGNATURE=1" )
    TECSGEN::CMake.add_include( "inc_signature" )
    TECSGEN::CMake.add_line( "# from signature" )
  end
end
