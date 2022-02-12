import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def init_map():
    from mpl_toolkits.basemap import Basemap

    m = Basemap(llcrnrlon=140.874088,llcrnrlat=-39.054526,urcrnrlon=151.567450,urcrnrlat=-33.122107,projection='mill',\
                    resolution='l')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.fillcontinents(color='#3C5C9B', lake_color='#FFFFFF')
    m.drawmapboundary(fill_color='#FFFFFF')
    return m

def init_color(size):
    colors = [ plt.cm.Spectral(each) for each in np.linspace(0, 1, size)]
    return colors

def plot_map(m,lat,lon,col):
    x,y = m(lon,lat)
    m.plot(x,y,'o',c=col,markersize=4,alpha=.5)

    return m

def end_plot(titlename="plot",figname="temp.png"):
    plt.title(titlename)
    plt.savefig(figname)



def Clustering(lat,lon):
    import numpy as np

    from sklearn.cluster import DBSCAN
    from sklearn import metrics
    from sklearn.datasets import make_blobs
    from sklearn.preprocessing import StandardScaler

    X= [xy for xy in zip(lat,lon)] 
    scal=StandardScaler()
    X = scal.fit_transform(X)

    # #############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.15, min_samples=8,algorithm='ball_tree', metric='haversine').fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_


    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    # print("Total number of locations: %d"%len(X))
    # print("Estimated number of clusters: %d" % n_clusters_)
    # print("Mean_Cluster_Size:",np.floor((len(X)-n_noise_)/n_clusters_))

    MEAN=0
    if n_clusters_:
        MEAN=int(np.floor((len(X)-n_noise_)/n_clusters_))
    if year==2011 and month ==4 :
        print(len(X))
    return len(X),n_clusters_,MEAN
    # print("Estimated number of noise points: %d" % n_noise_)
    # print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))

    # #############################################################################
    # Plot result
    # import matplotlib.pyplot as plt

    # X=scal.inverse_transform(X)

    # # Black removed and is used for noise instead.
    # unique_labels = set(labels)
    # colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    # cooll=colors[2]
    # # print(cooll)
    # for k, col in zip(unique_labels, colors):
    #     # print("!")
    #     if k == -1:
    #         # Black used for noise.
    #         col = [0, 0, 0, 1]

    #     class_member_mask = labels == k

    #     xy = X[class_member_mask & core_samples_mask]
    #     if sparse_or_dense=="dense":
    #         # print("!")
    #         plot_map(xy[:,0],xy[:,1],cooll,3,0,figname)

    #     xy = X[class_member_mask & ~core_samples_mask]
    #     if sparse_or_dense=="sparse":
    #         plot_map(xy[:,0],xy[:,1],col,3,0,figname)

    # plt.title("Estimated number of clusters: %d" % n_clusters_)
    # plt.savefig(figname)





    # print(labels==0)

    # import matplotlib.pyplot as plt
    # unique_labels = set(labels)
    # colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    # # print(cooll)
    # for k, col in zip(unique_labels, colors):

    #     class_member_mask = labels == k

    #     xy = X[class_member_mask]
        
    #     plot_map(xy[:,0],xy[:,1],col,3,0)


Map=init_map()
colors=init_color(10)

DF_R=pd.DataFrame()
Col0=[]
Col1=[]
Col2=[]
Col3=[]
for year in range(2010,2013):
    for month in range(1,13):
        df=pd.read_csv("FMonthly/modis_"+str(year)+"_"+str(month)+"_Australia.csv")
        FI=[0,0,0]
        if len(df["latout"]):
            FI=Clustering(df["latout"],df["lonout"],year,month)
        Col0.append(str(year)+"/"+str(month))
        Col1.append(FI[0])
        Col2.append(FI[1])
        Col3.append(FI[2])

DF_R["YYYY/MM"]=pd.Series(Col0)
DF_R["nFI"]=pd.Series(Col1)
DF_R["nCFI"]=pd.Series(Col2)
DF_R["nCMSFI"]=pd.Series(Col3)
DF_R.to_csv("FIRE_INDEX.csv")


# Map=plot_map(Map,df["latout"],df["lonout"],colors[2])


end_plot()


