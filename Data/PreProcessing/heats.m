clc
for years=2003:2020
    for mouths=1:12
        result=readmatrix("Monthly\modis_"+int2str(years)+"_"+int2str(mouths)+"_Australia.csv");

        heat=ones(size(Z,1),size(Z,2));
        BS_lon=result(:,3);
        BS_lat=result(:,2);
        [latin,lonin]=filterm(BS_lat,BS_lon,Z,R,0);
        [row,col]=geographicToDiscrete(R,latin,lonin);

        num_result=numel(row); %将经纬度值转换为网格的行列号，
        row_na=isnan(row);
        for i=1:num_result 
                heat(row(i),col(i))=heat(row(i),col(i))+1;
        end


        kk=figure;
        kk.Visible=false;
        kk.Position(3:4)=[906 522];
        worldmap(Z,R);
        meshm(sqrt(sqrt(heat)),R);
        colormap('hot');
        saveas(kk,"Pic\modis_"+int2str(years)+"_"+int2str(mouths)+"_Australia.png")

    end
end