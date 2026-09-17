# Application Smoke Test

This test verifies that the complete application can be started from a clean state and that the main customer-segmentatşon workflow operates correctly from data retrieval through visualization and interpretation.

The purpose is not to test every possible edge case, Instead it checks whether the primary application workflow is functional and suitable for demonstration.

## Test Date 17th September 2026
## 1. Clean Startup Test
The application starts from a fresh terminal session without requiring manual modification of the source code.

**Result:** PASS

## 2. Data Retrieval and Feature Generation Test

**Expected resut:**
The application retrieves the required transaction data from the configured ERP data source and successfully generates the customer-level feature dataset without errors.

The generated dataset should contain the expected customer-level features:

- Recency
- Monetary Value
- Average Order Value
- Product Count
- Transaction Count
- Total Quantity

**Result:**: PASS

## 3. Clustering and K Configuration Test

**Expected result:**  
The application successfully performs K-Means clustering using the value of K selected through the user interface.

Changing K should update the clustering result rather than continuing to use a previously selected or hardcoded value.

**Result:**  PASS

## 4. Evaluation and Visualization Test

**Expected result:**  
The application successfully generates the clustering evaluation outputs and visualizations for the selected value of K.

The following outputs should be available and update correctly:

- Elbow analysis
- Silhouette analysis
- Random initialization robustness results
- PCA visualization

**Result:**  PASS

## 5. Interpretation and Business Output Test

**Expected result:**  
The application successfully generates cluster-level statistics and human-readable interpretations for the current clustering configuration.

The displayed results should:

- Contain one interpretation for each generated cluster.
- Show cluster-level statistics such as customer count and monetary contribution.
- Update when K changes.
- Remain consistent with the underlying cluster feature values.
- Avoid missing, duplicated, or obviously stale cluster descriptions.

**Result:**  PASS

## 6. End-to-End Demonstration Test

**Expected result:**  
The complete customer-segmentation workflow can be demonstrated from beginning to end without modifying the source code or recovering from application errors.

The workflow should allow the user to:

- Retrieve and process ERP transaction data.
- Generate customer-level features.
- Select and modify K.
- Run customer clustering.
- Inspect elbow and silhouette evaluation results.
- Review robustness analysis.
- Inspect PCA visualization.
- Review cluster statistics and interpretations.
- Repeat the analysis using a different value of K.

**Result:** PASS