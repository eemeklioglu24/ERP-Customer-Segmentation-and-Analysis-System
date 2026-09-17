# Cluster and Business Analysis

## Purpose

This document examines the customer segments produced by the clustering system from a business and behavioral perspective.

Because the number of clusters, K, is configurable, the analysis presented here represents a specific clustering run rather than a permanen definition of the customer segments.

The objective is to determine whether the generated clusters correspond to distinguishable patterns of customer purchasing behavior and whether the resulting segmetn descriptions are supported by the underlying data.

## Reference Analysis

- **Analysis Date:** 17 September 2026
- **Number of clusters (K):** 5
- **Features used:** Recency, Monetary Value, Transaction Count, Average Order Value, Total Quantity, Product Diversity

The selected value of K is used only as a reference for examining the resulting customer segments. The application itself does not require this value of K.

## Cluster Feature Means

| Cluster | Recency | Monetary | Avg. Order Value | Product Count | Transaction Count | Total Quantity |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 184.17 | 79,783.82 | 25,574.40 | 15.25 | 3.42 | 7,629.50 |
| 1 | 74.16 | 5,341.76 | 2,135.90 | 32.47 | 3.26 | 468.55 |
| 2 | 262.51 | 2,381.06 | 1,823.87 | 20.59 | 1.56 | 226.39 |
| 3 | 18.47 | 115,350.17 | 4,603.50 | 270.80 | 29.67 | 7,306.27 |
| 4 | 28.25 | 26,269.28 | 2,470.53 | 161.67 | 12.04 | 2,677.38 |

## Cluster Size and Monetary Contribution

| Cluster | Customer Count | Total Monetary Value | Monetary Share |
|---|---:|---:|---:|
| 0 | 12 | 957,406 | 17.1% |
| 1 | 117 | 624,986 | 11.2% |
| 2 | 82 | 195,247 | 3.5% |
| 3 | 15 | 1,730,253 | 31.0% |
| 4 | 79 | 2,075,273 | 37.2% |

The reference dataset contains 305 customers in total.

A relatively small number of customers account for a substantial proportion of total monetary value. In particular, Clusters 0 and 3 contain only 27 customers combined but contribute approximately 48.1% of total monetary value.

## Cluster Profiles

### Cluster 0 — High-Spending, Infrequent Customers

Cluster 0 contains 12 customers and accounts for 17.1% of total monetary value.

Customers in this cluster have:

- High average monetary value.
- Extremely high average order value.
- Low transaction frequency.
- Relatively low product diversity.
- High total purchased quantity.
- Relatively long recency.

This cluster appears to represent customers who make relatively few purchases but place unusually large orders when they do purchase.

The automatically generated label **"Yüksek Harcamalı Seyrek Müşteriler"** is therefore consistent with the observed feature values.

### Cluster 1 — Moderate-Activity Customers

Cluster 1 contains 117 customers, making it the largest customer group, and accounts for 11.2% of total monetary value.

Customers in this cluster have:

- Moderate recency.
- Low-to-moderate monetary value.
- Low transaction frequency.
- Moderate product diversity.
- Relatively low purchased quantity.

These customers appear to represent a broad group of relatively ordinary or moderate-activity customers without particularly high purchasing intensity.

The automatically generated label **"Orta Değerli Müşteriler"** is broadly consistent with this behavior.

### Cluster 2 — Low-Activity / Inactive Customers

Cluster 2 contains 82 customers but accounts for only 3.5% of total monetary value.

Customers in this cluster have:

- The highest average recency.
- The lowest monetary value.
- The lowest transaction frequency.
- Low average order value.
- Low purchased quantity.
- Relatively limited product diversity.

This cluster appears to represent customers with weak recent purchasing activity and relatively little historical purchasing value.

The automatically generated label **"Orta Değerli Müşteriler"** does not describe this cluster particularly well. A label such as **"Düşük Aktiviteli Müşteriler"** or **"Pasif Müşteriler"** would better reflect the observed feature values.

### Cluster 3 — High-Spending, Highly Active Customers

Cluster 3 contains only 15 customers but contributes 31.0% of total monetary value.

Customers in this cluster have:

- Very low recency, indicating recent purchasing activity.
- The highest average monetary value.
- Very high transaction frequency.
- Extremely high product diversity.
- High purchased quantity.
- Moderate-to-high average order value.

This cluster represents a small group of highly active and economically important customers.

The automatically generated label **"Yüksek Harcamalı Aktif Müşteriler"** is strongly supported by the observed data.

### Cluster 4 — Frequent Active Customers

Cluster 4 contains 79 customers and contributes the largest share of total monetary value at 37.2%.

Customers in this cluster have:

- Low recency.
- High transaction frequency.
- High product diversity.
- Moderate monetary value per customer.
- Moderate average order value.
- High total purchased quantity.

These customers appear to purchase frequently and across a wide range of products, producing a large collective contribution to total monetary value.

The automatically generated label **"Sık Alım Yapan Müşteriler"** is consistent with the observed purchasing behavior.

## Business Observations

The reference clustering reveals several distinct customer behavior patterns.

- A small number of customers account for a disproportionately large share of total monetary value.
- Cluster 3 represents a particularly valuable group because its customers are both highly active and high-spending.
- Cluster 0 is also economically important despite its low transaction frequency because individual purchases are unusually large.
- Cluster 4 contributes the largest overall monetary share and represents a substantial group of frequent, active customers.
- Cluster 2 contains a relatively large number of customers but contributes very little monetary value and shows weak recent purchasing activity.
- Cluster 1 represents the largest customer group and appears to contain customers with comparatively ordinary purchasing behavior.

These results show that monetary value alone is not sufficient to describe customer behavior. Transaction frequency, recency, product diversity, quantity, and average order value provide additional information that distinguishes customers with very different purchasing patterns.

## Interpretation Review

The automatically generated cluster descriptions were compared with the underlying cluster statistics.

The interpretations for Clusters 0, 1, 3, and 4 were generally consistent with the observed feature values.

Cluster 2 revealed a limitation in the current interpretation logic. Although the cluster has the highest recency and the lowest monetary value and transaction frequency, it was labeled as "Orta Değerli Müşteriler". A description reflecting low activity or inactivity would better represent the observed behavior.

This issue should be reviewed as a potential improvement to the cluster interpretation rules.