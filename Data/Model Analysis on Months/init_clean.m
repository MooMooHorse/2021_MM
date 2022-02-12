clc
for year = 2010:2020
    for month= 1:12
        result=readmatrix("Monthly/modis_"+year+"_"+month+"_Australia.csv");
        
        lon=result(:,3);
        lat=result(:,2);
        [latout,lonout] = filterm(lat,lon,Z,R,0);
        
        T1=table(latout,lonout);
        
        writetable(T1,"FMonthly/modis_"+year+"_"+month+"_Australia.csv");
    end
end