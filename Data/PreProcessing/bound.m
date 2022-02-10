China=shaperead('STE_2021_AUST_GDA2020.shp','UseGeoCoords',true); %读入中国的国界文件shp文件
Scale=100; 
[Z,R]=vec2mtx(lat,lon,Scale,'filled');