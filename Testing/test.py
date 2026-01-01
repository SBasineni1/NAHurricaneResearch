import fsspec
import geopandas as gpd


read_data = 'HurricaneData\e_110m_admin_0_countries.zip'
gdf = gpd.read_file(read_data)
print(gdf)