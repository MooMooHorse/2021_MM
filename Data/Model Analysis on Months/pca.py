# Doc Address : https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np



df= pd.read_csv("ASS_IND.csv")

# scal1=StandardScaler()
L1=df["nFI"].to_list()
# scal1.fit_transform(L1)



# scal2=StandardScaler()
L2=df["nCFI"].to_list()
# scal2.fit_transform(L2)


# scal3=StandardScaler()
L3=df["nCMSFI"].to_list()
# scal3.fit_transform(L3)


# print(L1)
X = [ [x,y,z] for x,y,z in zip(L1,L2,L3) ] 
scal=StandardScaler()
X = scal.fit_transform(X)




pca = PCA(n_components=1)
# fit(X[, y]) Fit the model with X.
# transform(X) Apply dimensionality reduction to X.
X_r = pca.fit(X).transform(X)
comp =pca.components_[0]
print(comp)
result = []
for id_i,val_i in enumerate(X):

    result.append(np.dot(X[id_i],comp))
    

# print(result)
df=df.assign(Factor=result)

L4=df["tWCL"].to_list()


L5=df["nSSR"].to_list()
L6=df["nRep"].to_list()


print(df)

# fig=plt.Figure()
Com1=[(x,y) for x,y in zip(result,L4) ]
Com2=[(x,y) for x,y in zip(result,L5) ]
Com3=[(x,y) for x,y in zip(result,L6) ]



Com1.sort(key=lambda tup: tup[0])

Com2.sort(key=lambda tup: tup[0])

Com3.sort(key=lambda tup: tup[0])



Com1=np.array(Com1)
Com2=np.array(Com2)
Com3=np.array(Com3)
# print(Com1)

plt.subplot(1,3,1)

plt.plot(Com1[:-3,0],Com1[:-3,1])

plt.plot([-1,3], [930,930], 'r--')

# plt.show()

# plt.close(fig)

# fig=plt.Figure()
plt.subplot(1,3,2)

plt.plot(Com2[:-3,0],Com2[:-3,1])

plt.subplot(1,3,3)
plt.plot(Com3[:-3,0],Com3[:-3,1])



plt.show()

# plt.close(fig)

# ax=plt.subplot(1,3,1)
# ax.plot(result,L4)
# fig2,ax2=plt.subplot(1,3,2)
# plt.plot(result,L5)
# fig3,ax3=plt.subplot(1,3,3)
# plt.plot(result,L6)






"""
    printing meta-data
"""


# Comps=pca.components_[0]

# print(Comps[0]**2+Comps[1]**2+Comps[2]**2)

# Percentage of variance explained for each components
# print(
#     "explained variance ratio (first two components): %s"
#     % str(pca.explained_variance_ratio_)
# )

# Principal axes in feature space, representing the directions of maximum variance in the data. 
# print("components are %s"%str(pca.components_)) 

# Singular values of first n_components components
# print(pca.singular_values_)



"""
    end of printing meat-data
"""

# plt.figure()
# colors = ["navy", "turquoise", "darkorange"]
# lw = 2

# for color, i, target_name in zip(colors, [0, 1, 2], target_names):
#     plt.scatter(
#         X_r[y == i, 0], X_r[y == i, 1], color=color, alpha=0.8, lw=lw, label=target_name
#     )
# plt.legend(loc="best", shadow=False, scatterpoints=1)
# plt.title("PCA of IRIS dataset")

# plt.savefig("graph.png")
