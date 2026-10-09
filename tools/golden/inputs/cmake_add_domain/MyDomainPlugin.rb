# coding: utf-8

#== restrict テスト用ドメインプラグイン
class MyDomainPlugin < DomainPlugin
  def initialize( region, domain_type_name, option )
    super
    TECSGEN::CMake.add_source( "domain_plugin.c" )
    TECSGEN::CMake.add_define( "K_DOMAIN=1" )
    TECSGEN::CMake.add_include( "inc_domain" )
    TECSGEN::CMake.add_line( "# from domain" )
  end

  def add_through_plugin( join, current_region, next_region, through_type )
    return [:MyTracePlugin, ""]
  end

  # require の結合
  def joinable?(current_region, next_region, through_type )
    if next_region.get_name == "::" then
      return true
    end
  end

  def self.gen_post_code f
  end
end
