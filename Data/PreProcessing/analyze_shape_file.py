import geopandas
path_to_data = geopandas.datasets.get_path("STE_2021_AUST_GDA2020.shp")
gdf = geopandas.read_file(path_to_data)
print(gdf)