from wgus import Metadata


def test_parse():
    x = """
    <protocol name="app_metadata" version="7.2" wgc_publisher_id="wargaming,steam">
    <version>20211020153201</version>
    <predefined_section>
    <app_id>WOT.RU.PRODUCTION</app_id>
    <chain_id>sd3_hd3</chain_id>
    <supported_languages>BE,KK,RU,UK,EN</supported_languages>
    <default_language>RU</default_language>
    <name>World of Tanks</name>
    <client_types default="sd">
    <client_type id="sd">
    <initial_app_type>incomplete</initial_app_type>
    <final_app_type>sd</final_app_type>
    <required_redistributables>
    <value elevation_required="false">dx90c_light</value>
    </required_redistributables>
    <min_supported_os>Win7</min_supported_os>
    <client_parts>
    <client_part id="locale" integrity="true" lang="true"/>
    <client_part id="client" integrity="true"/>
    <client_part app_type="sd" id="sdcontent" integrity="true"/>
    </client_parts>
    </client_type>
    <client_type arch="x64" id="hd">
    <initial_app_type>incomplete</initial_app_type>
    <final_app_type>hd</final_app_type>
    <required_redistributables>
    <value elevation_required="false">dx90c_light</value>
    </required_redistributables>
    <min_supported_os>Win7</min_supported_os>
    <client_parts>
    <client_part id="locale" integrity="true" lang="true"/>
    <client_part id="client" integrity="true"/>
    <client_part app_type="sd" id="sdcontent" integrity="true"/>
    <client_part app_type="hd" id="hdcontent" integrity="true"/>
    </client_parts>
    </client_type>
    </client_types>
    </predefined_section>
    </protocol>"""

    meta = Metadata.parse(x)
    assert (
        meta.predefined_section.client_types.get().id
        == meta.predefined_section.client_types.default
    )
