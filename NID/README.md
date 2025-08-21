# [NID]
### Network intrusion detection - machine learning algorithms applied to the detection of malicous network activity

This project contains the classification of labeled network traffic (benign and various network attacks) with CART algorithms (IntruDTree and XGBoost) -> see **pipelines**. The network traffic data used is a balanced sample of the NF-UQ-NIDS-v2[^1]. It contains network traffic as NetFlows, where each data point is a summary of session between two end points.

Various types visualizations were generated from the results:
- The IntruDTree model[^2] requires a feature selection which was manually derived by ranking the features and observing the rise in accuracy with the addition of each feature by rank as visualized in **idtree_selection.ipynb**
- Model predictions are visualized as heatmaps in **model_predictions.ipynb**
- A part of the involved computer network is graphed in **network_connections.ipynb** utilizing the ```igraph``` library.
- A comparison of the class distirbution of network traffic in the original data[^1] to the sampled data used here as a bar plot in **class_distirbution.ipynb**

[^1]:Mohanad Sarhan, Siamak Layeghy, and Marius Portmann, Towards a Standard Feature Set for Network Intrusion Detection System Datasets, Mobile Networks and Applications, 103, 108379, 2022. https://doi.org/10.1007/s11036-021-01843-0

[^2]: P. I. Radoglou-Grammatikis and P. G. Sarigiannidis, "An Anomaly-Based Intrusion Detection System for the Smart Grid Based on CART Decision Tree," 2018 Global Information Infrastructure and Networking Symposium (GIIS), Thessaloniki, Greece, 2018, pp. 1-5, doi: 10.1109/GIIS.2018.8635743.,
