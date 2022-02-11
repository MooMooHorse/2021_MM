# Conquer The Flame



## Summary

Australia is undergoing huge wildfires in every state. To protect people and safety and property, we establish a model to use two types of drones to help Country Fire Authority (CFA) conduct “Rapid Bushfire Response”, and front-line personnel communicate with Emergency Operations Center (EOC).

We use `Victoria Fire Report Data`, using fire report places in certain time period to represent locations where fires happened on average. This allows us to take into account of factors such as fire size and frequency, economic cost and safety, weighted region area covered by drones. 

We set Fast Response Model for deployment of drones for fast response, we divide fire locations into clusters. There are two aspects we looked into, in-cluster relationship and relationship between clusters. For in-cluster relationship, according to the density of fire locations, we divide clusters into two types, dense cluster and sparse cluster. We establish separate models for each type of cluster. For dense cluster, we treated the cluster as a filled irregular region, and we establish Least Circles Maximum Coverage(LCMC) Model. For sparse cluster, we treat each fire location as node, and build edges for every node to form complete graph, and we build minimum spanning tree for it to ensure connectivity with lowest cost. For between-cluster relationship, we build edges between each cluster, and treat each cluster as a node. We ensure the connectivity by building minimum spanning tree.

We set Fire Prediction Model for second part of problem. we divide Victoria into several zones, and use statistics of zones in different time to form a time series. We predict the time series using Long Short-Term Memory (LSTM).

We set Pearl Model and Spur Model for Deployment of drones for front-line personnel in different circumstances, we use separate deployment strategies for small and big sized fire considering the effect of terrain. 

The sensitivity analysis shows robustness in our model. Meanwhile, we combine all the models to finish the annotated Budget Request to help CFA with acceptable cost.

**Keywords: Wild Fire Control, Clustering, Divide and Conquer, Minimum Spanning Tree, ConvLSTM, Terrian **



## Introduction

### Background

Wildfire spreads rapidly in Australia. In fire season, it's devastating for people's safety and properties. Victoria’s Country Fire Authority (CFA) uses different means to protect its people. Drones carrying high definition & thermal imaging cameras and telemetry sensors were sent for surveillance and situational awareness (SSA). Drone repeaters, transceivers that automatically rebroadcast signals at higher powers can help connect Emergency Operations Center (EOC) with SSA and front-line employees with VHF/UHF bands.



### Problem Restatement

#### Limits

* Drone-related
  * Cost $1000 per drone
  * Flight Range 30 km
  * Transmission Range 20 km
  * Flight Speed 20 m/s
* Fire-related
  * Size
  * Frequency

#### Targets

* Deployment of drones for fast response
  * Reduce cost
  * Increase weighted coverage
* Fire Prediction
* Deployment of drones for front-line personnel in different circumstances
  * Build models for different fire size
  * Build models considering different terrians



### Our work

![image-20220209230134033](https://s2.loli.net/2022/02/09/Ee5uXgjFw8dTsro.png)

## Assumptions and Justifications

* We use one year data in Victoria with data provided by Earth Data to represent the general cases in Australia. However, our model to this case adapt to arbitrary cases, so it's without losing generality.
* Dense Cluster is defined as a cluster of locations whose density is above a certain threshold. We treat dense cluster as homogeneous irregular system, since our strategy can give it a high coverage rate, thus the error will be decreased to acceptable level.
* Sparse Cluster is defined as a cluster of locations whose density is below a certain threshold. Instead of building minimum spanning tree on the whole state, we build it within cluster and between cluster respectively. This act will significantly improve the performance with our algorithm, but it will affect the optimization outcome. We use tolerated version to effectively compute the result within acceptable error, while it's preferred to build spanning tree treating each location as a node.
* Only 20 years of data is used for machine learning, the error produced is within the acceptable range.
* The terrain situation can be more complicated in real world, we idealize mountain and other barriers as parabolic-like object.



## Symbols

| Definition | Description |
| ---------- | :---------: |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |
|            |             |

## Fast Response Model

### Data Pre-processing (JXB)

### Clustering (JXB)

### In-Cluster Processing(RH)

### Between-Cluster Processing(RH)





## Fire Prediction Model

### Data Pre-processing (LR)

The data source used in this task is from Moderate-resolution Imaging Spectroradiometer(MODIS) provided by NASA. The obtained time series data of Australia wild-fire from 2003 to 2020 is saved in CSV format.

### Build Map with Fire Index (LR)

### Time series construction (LR)



### ConvLSTM (LR)

Time series data prediction refers to learning past time series and predicting future changes. Traditional Neural networks cannot solve the problem of time-axis variation, so RNN (Recurrent Neural network) is developed (Jordan et al., 1997).

However, due to the poor performance of classical RNN in extracting long time series information and the limited time series information extracted, Hochreiter proposed LSTM network model (Hochreiter et al.,1997). In classical RNN, gates structure is added to selectively add and delete the past timing information, and input gate, output gate and forgetting gate are added to control the input and output of data of this unit (an LSTM cell is a basic unit) and the increase and decrease of the output information of the previous unit respectively. The LSTM formula is expressed as follows:

$\mathbfit{i}_t=\sigma(\mathbfit{W}_{xi}\mathbfit{X}_{t}+\mathbfit{W}_{hi}\mathbfit{H}_{t-1}+\mathbfit{W}_{ci}\circ\mathbfit{C}_{t-1}+b_i) $

$\mathbfit{f}_t=\sigma(\mathbfit{W}_{xf}\mathbfit{X}_{t}+\mathbfit{W}_{hf}\mathbfit{H}_{t-1}+\mathbfit{W}_{cf}\circ\mathbfit{C}_{t-1}+b_f) $

$\mathbfit{C}_t=\mathbfit{f}_{t}\circ\mathbfit{C}_{t-1}+\mathbfit{i}_t\circ\tanh(\mathbfit{W}_{xc}\mathbfit{X}_{t}+\mathbfit{W}_{hc}\mathbfit{H}_{t-1}+b_c)$

$\mathbfit{o}_t=\sigma(\mathbfit{W}_{xo}\mathbfit{X}_{t}+\mathbfit{W}_{ho}\mathbfit{H}_{t-1}+\mathbfit{W}_{co}\circ\mathbfit{C}_{t-1}+b_o)$

Where $t $ stands for time step t, subscript $i,f,o$ stands for input gate, output gate and forgetting gate.

Based on the deep learning framework Pytorch, the ConvLSTM is constructed using Python language, and the experimental equipment environment is NVIDIA GeForce GTX1080 GPU.

### Model Fitting (LR)

### Reference

Jordan M I.1997. Serial Order: A Parallel Distributed Processing Approach. Advances in Psychology, pp. 471-495 .[DOI:10.1016/S0166-4115(97)80111-2]

Hochreiter S and Schmidhuber J .1997.Long Short-Term Memory. Neural computation, 9(8):1735-1780.[DOI:10.1162/neco.1997.9.8.1735]

## Pearl and Spur Model

### Pearl Model (TBD)

### Spur Model (TBD)