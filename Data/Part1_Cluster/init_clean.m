clc

% result=readmatrix("initial.csv");

% heat=ones(size(Z,1),size(Z,2));
% lon=result(:,2);
% lat=result(:,1);
% [latout,lonout] = filterm(lat,lon,Z,R,0);

% T1=table(latout,lonout);

writetable(T,"ini_filt2.csv")
%[row,col]=geographicToDiscrete(R,BS_lat,BS_lon);
% num_result=numel(row); %将经纬度值转换为网格的行列号，
% row_na=isnan(row);
% for i=1:num_result
%     if row_na(i)==0
%         heat(row(i),col(i))=heat(row(i),col(i))+1;
%     end
% end


% kk=figure;
% kk.Visible=false;
% kk.Position(3:4)=[185 109];
% worldmap(Z,R);
% meshm(sqrt(sqrt(heat)),R);
% colormap('hot');
% saveas(kk,"Pic\modis_"+int2str(years)+"_"+int2str(mouths)+"_Australia.png")
