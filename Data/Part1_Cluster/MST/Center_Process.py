def Kruskal(graph,vertex_num,out_edges):
    vnum=vertex_num
    reps=[i for i in range(vnum)]
    mst,edges=[],[]
    for vi in range(vnum):
        for v,w in out_edges[vi]:
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


def Build_Tree():
    

    return 
import pandas as pd

df=pd.read_csv("Part1_Cluster/Center_Coord.csv")
