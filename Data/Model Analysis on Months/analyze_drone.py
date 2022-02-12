import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def Build_Tree(node_set):
    edge_set=[[] for i in range(len(node_set[0]))] 
    # print(edge_set)
    for i in range(len(node_set[0])):
        for j in range(len(node_set[0])):
            if i==j:
                continue
            w=Calc_Dis(node_set[0][i],node_set[1][i],node_set[0][j],node_set[1][j])
            w=max(w-40,0)/40
            edge_set[i].append([j,w])

    # print(edge_set[0])
    return edge_set


def Calc_Dis(latitude1,longitude1,latitude2,longitude2):
    from math import radians,sin,cos,atan2,sqrt
    R = 6373.0
    lat1 = radians(float(latitude1))
    lon1 = radians(float(longitude1))
    lat2 = radians(float(latitude2))
    lon2 = radians(float(longitude2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def Kruskal(vertex_num,out_edges):
    vnum=vertex_num
    reps=[i for i in range(vnum)]
    mst,edges=[],[]
    for vi in range(vnum):
        for el in out_edges[vi]:
            v=el[0]
            w=el[1]
            # print(w)
            edges.append((w,vi,v))
    edges.sort()
    for w,vi,vj in edges:
        if reps[vi]!=reps[vj]:
            mst.append(((vi,vj),w))
            if len(mst)==vnum-1:
                break
            rep,orep=reps[vi],reps[vj]
            for i in range(vnum):
                if reps[i]==orep:
                    reps[i]=rep
    return mst

def Calc_Cost(tree_edges):
    from math import ceil
    cost=0
    for edge in tree_edges:
        w=edge[1]
        cost=cost+ceil(w)+1
        # print(ceil(w))
    return cost

def K_Mean_Clustering(lat,lon,year,month):
    import numpy as np

    from sklearn.cluster import DBSCAN,k_means
    from sklearn import metrics
    from sklearn.datasets import make_blobs
    from sklearn.preprocessing import StandardScaler

    X=np.array( [xy for xy in zip(lat,lon)] )


    tWCL=902
    for cluster_num in range(1,30):
        db =  k_means(X,n_clusters=cluster_num)


        Center=db[0]
        labels = db[1]


        
        xy=[[],[]]

        for center in Center:
            xy[0].append(center[0])
            xy[1].append(center[1])


        edge_set=Build_Tree(xy)
        tree_edges=Kruskal(len(xy[0]),edge_set)

        cost=Calc_Cost(tree_edges)
        # print("cost is",cost)

        WCL=0
        for (ind,point) in enumerate(X):
            Cen=Center[labels[ind]]
            WCL+=Calc_Dis(Cen[0],Cen[1],point[0],point[1])**4
        
        if WCL/len(X)**2 < tWCL:
            return WCL/len(X)**2,cluster_num,cost,cost+cluster_num
        
    print(year,month)

    # print(WCL/len(X)**2)

DF_R=pd.read_csv("FIRE_INDEX.csv")

Col4=[]
Col5=[]
Col6=[]
for year in range(2010,2021):
    for month in range(1,13):
        df=pd.read_csv("FMonthly/modis_"+str(year)+"_"+str(month)+"_Australia.csv")

        EI=[0,0,0]

        if len(df["latout"]):
            EI=K_Mean_Clustering(df["latout"].to_list(),df["lonout"].to_list(),year,month)

        if EI==None:
            EI=[0,0,0]
        Col4.append(EI[0])
        Col5.append(EI[1])
        Col6.append(EI[2])


DF_R["tWCL"]=pd.Series(Col4)
DF_R["nSSR"]=pd.Series(Col5)
DF_R["nRep"]=pd.Series(Col6)

DF_R.to_csv("ASS_IND.csv")