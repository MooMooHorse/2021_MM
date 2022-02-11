from platform import node


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

def Calc_Cost(tree_edges):
    from math import ceil
    cost=0
    for edge in tree_edges:
        w=edge[1]
        cost=cost+ceil(w)+1
        # print(ceil(w))
    return cost


def plot_map(lat,lon,col,mksz,rangesize,figname="two_type.png"):
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
    m.plot(x,y,'o',c=tuple(col),markersize=rangesize,alpha=.2)

    # # x,y = m(lon2,lat2)
    # # m.plot(x,y,'go',markersize=4,alpha=.5)

    plt.title('2-type Drones plotting')
    plt.savefig(figname)
    # return plt
    # plt.show()

def Plot_Edge(u,v,w,node_set,sample=0):
    lat1=node_set[0][u]
    lat2=node_set[0][v]
    lon1=node_set[1][u]
    lon2=node_set[1][v]

    # print(w)

    
    from math import ceil
    dlat=(lat2-lat1)/(ceil(w)+1)
    dlon=(lon2-lon1)/(ceil(w)+1)

    # print(dlon)

    lat=lat1
    lon=lon1

    if sample:
        print(lat,lon)
        # print(lat1,lat2,lon1,lon2)

    import matplotlib.pyplot as plt
    import numpy as np
    color_size=5
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, color_size)]

    # print(lat,lat+dlat,lat+2*dlat,lat+3*dlat)
    for i in range(0,ceil(w)):
        # print(dlat,dlon)
        lat=lat+dlat
        lon=lon+dlon
        plot_map(lat,lon,colors[3],3,20)

def Plot_Ends(u,v,node_set):
    lat1=node_set[0][u]
    lat2=node_set[0][v]
    lon1=node_set[1][u]
    lon2=node_set[1][v]

    import matplotlib.pyplot as plt
    import numpy as np
    color_size=5
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, color_size)]

    plot_map(lat1,lon1,colors[3],3,20)
    plot_map(lat2,lon2,colors[3],3,20)
    # plt.show()

def Plot_Tree(tree_set,node_set):
    # print(len(tree_set))
    # DEBUG
    # sample=8
    for edge in tree_set:
        u,v=edge[0]
        w=edge[1]
        Plot_Ends(u,v,node_set)
        # if not sample:
        Plot_Edge(u,v,w,node_set)
        # Plot_Ends
        # print(sample)
        # sample=sample-1
    return 

import pandas as pd

df=pd.read_csv("Part1_Cluster/Center_Coord.csv")

xy=[df["latitude"].to_list(),df["longitude"].to_list()]

edge_set=Build_Tree(xy)
# print(edge_set[2])
tree_edges=Kruskal(len(xy[0]),edge_set)

cost=Calc_Cost(tree_edges)
print("cost is",cost)
Plot_Tree(tree_edges,xy)

# Plot_Edge(tree_edge[0])

# print(cost)
# print(tree_edges)
# print(Calc_Dis(xy[0][0],xy[1][0],xy[0][3],xy[1][3]))
