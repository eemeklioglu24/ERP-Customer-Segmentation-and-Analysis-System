# Model Validation and Evaluation

## Purpose

The customer-segmentation system does not use a fixed number of clusters. The value of K is configurable through the user interface so that different clustering configurations can be evaluated depending on the dataset being analyzed.

The purpose of model validation in this project is therefore not to identify one permanently correct value of K. Instead, the application provides multiple evaluation methods that help the user assess whether a particular clustering configuration is reasonable.

The evaluation process considers:

- Clustering objective values across different values of K.
- Silhouette scores for measuring cluster cohesion and separation.
- Stability across different K-Means random initializations.
- PCA visualization as a visual aid for examining the resulting customer segments.

These methods are intended to be considered together. No single metric is treated as definitive evidence that a particular value of K is universally optimal.

## Elbow Analysis

The elbow method evaluates how the K-Means objective value changes as the number of clusters increases.

For each candidate value of K, the clustering algorithm calculates the within-cluster objective value. As K increases, this value will normally decrease because additional clusters allow customers to be grouped more closely around their assigned centroids.

The goal is not simply to choose the largest possible value of K. Instead, the elbow method looks for a point where increasing K produces progressively smaller improvements in the objective value.

This point can indicate a reasonable balance between:

- Lower within-cluster variation.
- Simpler cluster structure.
- Avoiding unnecessary fragmentation of customer groups.

The elbow method is used as a diagnostic tool rather than as an automatic rule for selecting K. Its result should be considered together with silhouette analysis, stability testing, and the practical interpretability of the resulting customer segments.

## Silhouette Analysis

Silhouette analysis evaluates how well each customer fits within its assigned cluster compared with neighboring clusters.

For each customer, the silhouette value considers:
- How close the customer is to other customers in the same cluster.
- How close the customer is to customers in the nearest alternative cluster.

The silhouette values generally range between -1 and 1:
- Values closer to **1** indicate that the customer is well matched to its assigned cluster and relatively far from neighboring clusters.
- Values around **0** indicate that the customer lies near a boundary between clusters.
- Negative values may indicate that the customer could potentially fit better witihin another cluster.

The application calculates silhouette results for candidate values of K so that different clustering configurations can be compared.

A higher silhouette score can indicate better-defined clusters, but it is not trated as the only criteria for selecting K. The score should be inerpreted together with elbow analysis, clustering stability, visualization, and the practical context of the data set.

## Random Initialization Robustness

K-Means clustering can produce different results depending on the initial positions of cluster centroids. Because of this, a single run is not sufficient to determine wheter a clustering configuration is stable.

The project evaluates robustness by running K-Means multiple times with different random initializations and comparing the resulting clustering quality.

The purpose of this test is to determine wheter:

- Similar objective values are obtained across repeated runs.
- Silhouette scores remain reasonably consistent.
- The clustering process frequently converges to similarly strong solutions.
- The selected value of K is not producing highly unstable results that depend heavily on a particular initialization.

If repeated runs produce substantially different results, this may indicate that the clustering configuration is sensitive to initialization or that the underlying customer structure is not clearly seperated for the chosen K.

Robustness testing therefore provides additional confidence that the observed clustering quality is not simply the result of one favorable  random initialization.

## PCA Visualization
Principal Component Analysis (PCA) is used to create a two dimensional representation of the standardized customer feature space.

The original clustering process uses all available customer features. PCA is applied only after the standardization to reduce the feature space for visualization purposes.

The PCA plot can help the user inspect:
- Whether customer groups appear visually seperated.
- Whether some clusters strongly overlap.
- Whether outliers are present.
- Whether the overall cluster structure appears inconsistent with the numerical evaluation metrics.

Because PCA compresses the original feature space into two dimensions, some information is necessarily lost during projection. Therefore, visual seperation in the PCA plot is not treated as proof that a clustering config is correct.

Likewise, overlapping clusters in two dimensions do not necessarily mean that the clusters are poorly seperated in the full feature space.

PCA is therefore a supporting visual diagnostic and is interpreted together with the elbow method, silhouette analysis, robustness testing, and cluster interpretability.

## Combined Evaluation

No single method is used to determine whether a clustering congiuration is acceptable.

Instead, candidate values of K are assessed using multiple sources of evidence:
- The elbow curve is inspected for diminishing improvement in the clustering objective.
- The silhouette scors are compared across candidate values of K.
- Repeated random initializations are used to assess clustering stability.
- PCA is used as a supporting visualization of the customer segments.
- The resulting clusters are checked for practical interpretablity.

A clustering configuration is considered more convincing when several of these indicators support the same general conclusion.

The final choice of K remains configurable and may change when the underlying ERP data changes.