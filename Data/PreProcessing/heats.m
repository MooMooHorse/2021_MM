clc
for years=2003:2020
    for mouths=1:12
        result=readmatrix("Monthly\modis_"+int2str(years)+"_"+int2str(mouths)+"_Australia.csv");

        heat=ones(size(Z,1),size(Z,2));
        BS_lon=result(:,3);
        BS_lat=result(:,2);
        [row,col]=geographicToDiscrete(R,BS_lat,BS_lon);
        num_result=numel(row); %将经纬度值转换为网格的行列号，
        row_na=isnan(row);
        for i=1:num_result
            if row_na(i)==0
                heat(row(i),col(i))=heat(row(i),col(i))+1;
            end
        end


        kk=figure;
        kk.Visible=false;
        kk.Position(3:4)=[185 109];
        worldmap(Z,R);
        meshm(sqrt(sqrt(heat)),R);
        colormap('hot');
        saveas(kk,"Pic\modis_"+int2str(years)+"_"+int2str(mouths)+"_Australia.png")

    end
end