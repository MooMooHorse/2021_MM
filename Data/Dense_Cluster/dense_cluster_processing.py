

def plot_map(lat,lon,col,mksz,figname):
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt

    m = Basemap(llcrnrlon=140.874088,llcrnrlat=-39.054526,urcrnrlon=151.567450,urcrnrlat=-33.122107,projection='mill',\
                    resolution='l')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.fillcontinents(color='#3C5C9B', lake_color='#FFFFFF')
    m.drawmapboundary(fill_color='#FFFFFF')
    
    x,y = m(lon,lat)
    m.plot(x,y,'o',c=tuple(col),markersize=mksz,alpha=.5)

    # # x,y = m(lon2,lat2)
    # # m.plot(x,y,'go',markersize=4,alpha=.5)

    plt.title('Geo Plotting')
    plt.savefig(figname)



def Clustering(lat,lon,sparse_or_dense,figname):
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

    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))

    # #############################################################################
    # Plot result
    import matplotlib.pyplot as plt

    X=scal.inverse_transform(X)

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = labels == k

        xy = X[class_member_mask & core_samples_mask]
        if sparse_or_dense=="dense":
            plot_map(xy[:,0],xy[:,1],col,3,figname)
        # plt.plot(
        #     xy[:, 0],
        #     xy[:, 1],
        #     "o",
        #     c=tuple(col),
        #     markersize=3,
        # )

        xy = X[class_member_mask & ~core_samples_mask]
        if sparse_or_dense=="sparse":
            plot_map(xy[:,0],xy[:,1],col,3,figname)
        # plt.plot(
        #     xy[:, 0],
        #     xy[:, 1],
        #     "o",
        #     c=tuple(col),
        #     markersize=0.5,
        # )

    plt.title("Estimated number of clusters: %d" % n_clusters_)
    # plt.savefig(figname)



import pandas as pd
df=pd.read_csv("Dense_Cluster/ini_filt1.csv")

Clustering(df["latitude"].tolist(),df["longitude"].tolist(),"dense","dense_cluster.png")