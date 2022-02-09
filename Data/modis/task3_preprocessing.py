import pandas as pd
import os
if not os.path.exists('Monthly'):
    os.mkdir('Monthly')

for year in range(2003,2021):
    modis=pd.read_csv("modis_"+str(year)+"_Australia.csv")
    modis=modis[(modis['confidence']>=80)]
    modis['acq_date']=pd.to_datetime(modis['acq_date'])
    modis.drop(modis.columns[[2,3,4,6,7,8,9,10,11,12,13,14]],axis=1,inplace=True)
    modis.set_index('acq_date',inplace=True)

    for months in range(1,13):
        modis[str(year)+'-'+str(months)].to_csv('Monthly/modis_'+str(year)+'_'+str(months)+'_Australia.csv',)

