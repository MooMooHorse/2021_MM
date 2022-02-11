# Conquer The Flame



## Summary

Australia is undergoing huge wildfires in every state. To protect people and safety and property, we establish a model to use two types of drones to help Country Fire Authority (CFA) conduct “Rapid Bushfire Response”, and front-line personnel communicate with Emergency Operations Center (EOC).

We use `Victoria Fire Report Data`, using fire report places in certain time period to represent locations where fires happened on average. This allows us to take into account of factors such as fire size and frequency, economic cost and safety, weighted region area covered by drones. 

We set Fast Response Model for deployment of drones for fast response, we quantify the coverage with a weighted quantity. We build a model to investigate its' relationship with the economic cost. For a certain coverage by drone, we devise a strategy to distribute SSAs by using k-means with special distance function and we use minimum spanning tree to distribute repeaters to connect them. We show the mathematical properties to such distance to ensure the correctness of our algorithm.

We set Fire Prediction Model for second part of problem. we divide Victoria into several zones, and use statistics of zones in different time to form a time series. We predict the time series using convolutional Long Short-Term Memory (convLSTM).

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
* We assume once the fire is within the detective range of drones, it will be found out without delay.
* We assume the spread rate of fire is stable and at a certain value, which is not the case in real world, but one can use the original formulae given in the model to simply modify the model.
* Only 20 years of data is used for machine learning, the error produced is within the acceptable range.
* The terrain situation can be more complicated in real world, we idealize mountain and other barriers as parabolic-like object.



## Symbols

| Definition              | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| $dist$                  | Distance between two points in Euclidean coordinate system   |
| $R_e$                   | Radius of earth                                              |
| $\Delta \varphi _{lat}$ | Thange of latitude                                           |
| $\Delta \lambda _{lon}$ | Thange of longitude                                          |
| $eps$                   | Tf the distance between two points is lower or equal to (eps), these points are considered neighbuors. |
| $minPoints$             | The minimum number of points to form a dense region.         |
| $x_0$                   | Distance to drone when the fire is recorded in our data      |
| $x_1$                   | Distance to drone when drone detect fire                     |
| $dis_{j,t}$             | The shortest distance of fire location indexed $j$ to the nearest drone at distance $x$ from the drone |
| $r_c$                   | The radius of drone in idealized condition.                  |
| $vs_{j,x} $             | The spread rate of fire at the rim of fire area indexed $j$ at distance $x$ from the drone |
| $p_{j,x}$               | The probability for drones to detect rim of fire location $j$ at distance $x$ from the drone |
| $v$                     | Stable spread rate which is assumed to simply the model      |
| $WCL$                   | Weighted coverage loss : describing the loss the weighted area for a deployment strategy |
| $r_o$                   | Outer-radius of drone, meaning the furthest distance the drone can detect, that is, $50$ km |
| $tWCL$                  | Threshold for $WCL$ to determine how much SSA should be deployed. |
|                         |                                                              |
|                         |                                                              |
|                         |                                                              |

## Fast Response Model

To discuss the possible deployment of drones in order to detect fire and transmit the signal to EOC, we design Fast Response Model to maximize coverage and minimize the cost. To represent the fire distribution, fire frequency and fire size, we come up with several well-designed indices and use fire location in certain period to represent those factors with minimum lost of information.  Since it's not economically efficient to cover all the land of Victoria because the drones are able to move and the fact that fire can spread and then be detected, we use weighted covering lost(WCL) to represent the cost for not covering all the possible locations of fire. We use the data in 2020 for case study, but the strategy we adapt and the data we compute is generic and can be used in various situation. 

After sensitivity test, we proved the robustness of the model. It can be showed that the Fast Response Model can be used in different size of fire, different frequency of fire, and different distribution of fire in state of Victoria and other places in the world.

### Data Pre-processing (RH)

For the sake of CFA, our model should only be considering the fire situation within the range of state of Victoria. The data we obtained from NASA database is contains noise and locations out of border. The first step of data pre-processing is meant to sift out all the illegal point with criteria mentioned above. Considering the spatial location of noise point, we use DBSCAN clustering with ball tree[https://en.wikipedia.org/wiki/Ball_tree] algorithm, and is implemented by sci-learn project[https://scikit-learn.org/stable/about.html#citing-scikit-learn]. Since the data contains latitude and longitude, to define the distance function for clustering one need to use the haversine formula["http://www.movable-type.co.uk/scripts/latlong.html"] to calculate the great-circle distance between two points.
$$
dist=2\cdot R_{e} \cdot \arctan (\sqrt{\frac {\sin^2(\frac {\Delta \varphi_{lat} }{2})+\cos\varphi _1\cdot 
\cos \varphi _2 \cdot \sin^2({ \frac {\Delta \lambda_{lon}} {2} })}
{1-(\sin^2(\frac {\Delta \varphi_{lat} }{2})+\cos\varphi _1\cdot 
\cos \varphi _2 \cdot \sin^2({ \frac {\Delta \lambda_{lon}} {2} }))}})
$$
This ensures the correctness of clustering.

To define a noise point which is inefficient to cover it, we define two variables $eps$ and $minPoints$​ according to DBSCAN conventions. 

To more easily obtain the optimized value, we first normalize data with standard normalization, then we set 
$$
\left\{
\begin{array}{**lr**}
eps=0.15&  \\  
minPoints=8
\end{array}  
\right.
$$

![img](https://s2.loli.net/2022/02/11/FZf6Jrldk4aB8Hv.png)



### Deploying SSA 

To deploy drones in a way that reaches the target of fast response, we first need to quantify the target using one index, which we define it as weighted covering lost(WCL).
$$
WCL=\sum_j \int _{x0} ^{x1}  { (x-r_c)\cdot (1-p_{j,x})} \cdot vs_{j,x}  \  dx \\ \\
$$
To simplify our model, we assume $vs_{j,x}=v$, which is a stable value, then we have.
$$
WCL=\sum_j (\int _{x0} ^{x1}  { (x-r_c)\cdot p_{j,x}} \cdot  v  \  dx)^2
$$
In order to simply the model as well as simulate the distribution of $p_{j}$, we use Ridge Distribution to set $p_{j,x}$, which is the probability of rim of fire at the position which is $x$ km from the nearest SSA, as following
$$
p_{j,x}=\left\{
\begin{array}{**lr**}
\frac 1 2 - \frac 1 2 \sin \frac {\pi} {r_o}(x-\frac {r_o} {2} ) && 0\le x \le r_0 \\ 
0 && x > r_0
\end{array}  
\right.
$$
This gives us
$$
WCL=\sum_j (\int _{x0} ^{x1}  { (x-r_c)\cdot (\frac 1 2 + \frac 1 2 \sin \frac {\pi} {r_o}(x-\frac {r_o} {2} ))} \cdot  v  \  dx)^2
$$
We use the concept of substitution distance($sdist$) to investigate the deployment strategy.
$$
sdist=||\int _{x0} ^{x1}  { (x-r_c)\cdot (\frac 1 2 + \frac 1 2 \sin \frac {\pi} {r_o}(x-\frac {r_o} {2} ))} \cdot  v  \  dx||
$$
We define $sdist$ in a way that guarantees $sdist$ is positively correlated to $x$ which is the distance to the center, that is, the place where the nearest drone is deployed.

To balance economical costs and safety, we set a threshold for $WCL$, $tWCL$ which is currently set to a certain value in our later investigation, but it can be adjusted according to real situation. It will be illustrated more thoroughly in the following section about sensitivity and robustness. We use modified $k-means$ cluster to determine the positions of SSAs, which is described as follows

<img src="https://s2.loli.net/2022/02/11/gTmZnXOFjYIVMNi.png" alt="image-20220211181747899" style="zoom:67%;" />

This allows us to cluster the locations to their respective drones. k-means algorithm is used here since the $sdist$ is positively correlates to distance. So the correctness of the algorithm can be ensured.

![img](https://s2.loli.net/2022/02/11/5Uy3eBXLbxfSmwN.png)

Given the fire location distribution, we plot the SSA's location as follow. The range is marked as well. It can be observed that the fire is frequent and in large scale at the east of state of  Victoria. Our distribution perfectly fit the situation can reduce $WCL$ to acceptable level.

![img](https://s2.loli.net/2022/02/11/Ck7X2wBuEnJVUtW.png)

### Deploy Repeaters

The second part of Fast Response Model is connecting all the SSAs using the least repeaters, which requires

#### Dense Cluster



#### Sparse Cluster





## Fire Prediction Model

### Data Pre-processing

The data source used in this task is from Moderate-resolution Imaging Spectroradiometer(MODIS) provided by NASA. The obtained time series data of Australia wild-fire from 2003 to 2020 is saved in CSV format.


### Build Map with Fire Index




### ConvLSTM

Time series data prediction refers to learning past time series and predicting future changes. Traditional Neural networks cannot solve the problem of time-axis variation, so RNN (Recurrent Neural network) is developed (Jordan et al., 1997).

However, due to the poor performance of classical RNN in extracting long time series information and the limited time series information extracted, Hochreiter proposed LSTM network model (Hochreiter et al.,1997). In classical RNN, gates structure is added to selectively add and delete the past timing information, and input gate, output gate and forgetting gate are added to control the input and output of data of this unit (an LSTM cell is a basic unit) and the increase and decrease of the output information of the previous unit respectively. The LSTM formula is expressed as follows:

$\mathbfit{i}_t=\sigma(\mathbfit{W}_{xi}\mathbfit{X}_{t}+\mathbfit{W}_{hi}\mathbfit{H}_{t-1}+\mathbfit{W}_{ci}\circ\mathbfit{C}_{t-1}+b_i) $

$\mathbfit{f}_t=\sigma(\mathbfit{W}_{xf}\mathbfit{X}_{t}+\mathbfit{W}_{hf}\mathbfit{H}_{t-1}+\mathbfit{W}_{cf}\circ\mathbfit{C}_{t-1}+b_f) $

$\mathbfit{C}_t=\mathbfit{f}_{t}\circ\mathbfit{C}_{t-1}+\mathbfit{i}_t\circ\tanh(\mathbfit{W}_{xc}\mathbfit{X}_{t}+\mathbfit{W}_{hc}\mathbfit{H}_{t-1}+b_c)$

$\mathbfit{o}_t=\sigma(\mathbfit{W}_{xo}\mathbfit{X}_{t}+\mathbfit{W}_{ho}\mathbfit{H}_{t-1}+\mathbfit{W}_{co}\circ\mathbfit{C}_{t-1}+b_o)$


Where $t $ stands for time step, subscript $i,f,o$ stands for input gate, output gate and forgetting gate. $\mathbfit{C}$ and $\mathbfit{H}$ represent cell state (gated output information) and hidden state (output value at each time step) respectively, $\mathbfit{W}$ represents weight of corresponding data, $\mathbfit{X}$ represents input data, $b$ represents bias value, and $\sigma$ represents activation function. о means Hadamard product.

ConvLSTM is a variant of LSTM proposed on the basis of LSTM. It replaces the fully connected state between the input layer and the hidden layer and between the hidden layer and the hidden layer of LSTM with the convolution connection, which makes full use of the spatial information that LSTM cannot. LSTM needs to transform image data into one-dimensional vector when processing image data, and cannot process spatial structure information of original image data. Compared with LSTM model,Conv LSTM can better extract spatial and temporal structure information from time series images. ConvLSTM model formula is expressed as follows:

$\mathbfit{i}_t=\sigma(\mathbfit{W}_{xi}*\mathbfit{X}_{t}+\mathbfit{W}_{hi}*\mathbfit{H}_{t-1}+\mathbfit{W}_{ci}\circ\mathbfit{C}_{t-1}+b_i) $

$\mathbfit{f}_t=\sigma(\mathbfit{W}_{xf}*\mathbfit{X}_{t}+\mathbfit{W}_{hf}*\mathbfit{H}_{t-1}+\mathbfit{W}_{cf}\circ\mathbfit{C}_{t-1}+b_f) $

$\mathbfit{C}_t=\mathbfit{f}_{t}\circ\mathbfit{C}_{t-1}+\mathbfit{i}_t\circ\tanh(\mathbfit{W}_{xc}*\mathbfit{X}_{t}+\mathbfit{W}_{hc}*\mathbfit{H}_{t-1}+b_c)$

$\mathbfit{o}_t=\sigma(\mathbfit{W}_{xo}*\mathbfit{X}_{t}+\mathbfit{W}_{ho}*\mathbfit{H}_{t-1}+\mathbfit{W}_{co}\circ\mathbfit{C}_{t-1}+b_o)$

The symbol meaning in the formula is the same as that in LSTM. The full connection of input variables is replaced by convolution operation, $*$ represents convolution operation. According to the internal structure of ConvLSTM in FIG. 2, it can be seen that input gate, output gate and forgetting gate all carry out convolution operation for input and hidden layer.

![image-20220211203954162](https://s2.loli.net/2022/02/11/LRnaVqQxbZtSv29.jpg)

$\mathbfit{W}_{ci}\circ\mathbfit{C}_{t-1}$, $\mathbfit{W}_{cf}\circ\mathbfit{C}_{t-1}$ and $\mathbfit{W}_{co}\circ\mathbfit{C}_{t-1}$ in the formula indicate that the input, output and forgetting gates are connected to the Peephole(Gers et al., 2000) of the previous cellular state. As shown in the figure, the Peephole connection adds cell state information to each gate. Since the unit may have a door state of 0, which results in a lack of important information, adding the Peephole operation can improve this shortcoming.

Based on the deep learning framework Pytorch, the ConvLSTM is constructed using Python language, and the experimental equipment environment is NVIDIA GeForce GTX1080 GPU.



### Reference

Jordan M I.1997. Serial Order: A Parallel Distributed Processing Approach. Advances in Psychology, pp. 471-495 .[DOI:10.1016/S0166-4115(97)80111-2]

Hochreiter S and Schmidhuber J .1997.Long Short-Term Memory. Neural computation, 9(8):1735-1780.[DOI:10.1162/neco.1997.9.8.1735]

## Pearl and Spur Model

### Pearl Model (TBD)

### Spur Model (TBD)