clc

result=readmatrix("../Model Analysis on Months/Monthly/modis_2010_1_Australia.csv");

lon=result(:,2);
lat=result(:,1);
[latout,lonout] = filterm(lat,lon,Z,R,0);

T1=table(latout,lonout);

writetable(T1,"../Model Analysis on Months/FMonthly/modis_2010_1_Australia.csv");