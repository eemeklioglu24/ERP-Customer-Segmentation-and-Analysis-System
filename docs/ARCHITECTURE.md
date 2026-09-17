# System Architecture

## System Overview

The application is structured as a modular customer-segmentation pipeline that separates data access, data processing, machine-learning logic, interpretation, visualization, and user-interface responsibilities.
At a high level, the system follows this flow:
```
ERP Data Source
      ↓
ERP Access Layer
      ↓
Data Processing and Feature Engineering
      ↓
Feature Standardization
      ↓
K-Means Clustering
      ↓
Evaluation and Analysis
      ↓
Cluster Interpretation
      ↓
Visualization
      ↓
Streamlit User Interface
```
## Module Responsibilities

### `main.py`
Coordinates the overall analysis workflow. It connects the data source, feature-generation logic, clustering pipeline, evaluation steps, and interpretation components.

### `src/data_handler.py`
Handles data preparation and customer-level feature engineering. Raw transaction data is transformed into the numerical behavioral features used by the clustering pipeline.

### `src/functions.py`
Contains the main numerical and machine-learning functionality used by the project, including clustering-related operations and supporting analysis logic.

### `src/interpreter.py`
Converts numerical cluster statistics into human-readable descriptions. It is responsible for generating interpretable summaries of customer segments.

### `src/erp/base.py`
Defines the common interface used by ERP data sources. This allows the rest of the application to interact with different data providers without depending directly on a specific ERP implementation.

### `src/erp/fake_erp.py`
Provides a development or synthetic ERP data source. It allows the application pipeline to be tested without requiring access to the real ERP database.

### `src/erp/logo_erp.py`
Provides the implementation used to retrieve data from the configured real ERP system.

### `ui/app.py`
Defines the Streamlit user interface and connects user interactions to the underlying analysis pipeline.

### `ui/graphs.py`
Contains visualization functionality used by the Streamlit application, including cluster evaluation and customer-segmentation plots.

### `sql/`
Contains SQL queries used for ERP exploration and transaction-data retrieval. Environment-specific or sensitive queries are kept separate from reusable examples.

## Data Flow

The application processes data through the following stages:

1. **Data Retrieval**  
   Transaction records are obtained from either the real ERP implementation or the development data source through the ERP access layer.

2. **Raw Transaction Data**  
   The retrieved records are represented as a Pandas DataFrame containing the transaction information required by the analysis pipeline.

3. **Feature Engineering**  
   Transaction-level records are aggregated into customer-level behavioral features:

   - Recency
   - Monetary value
   - Transaction count
   - Average order value
   - Total quantity
   - Product diversity

4. **Feature Standardization**  
   The numerical customer features are standardized so that features with different units and scales can be compared fairly during clustering.

5. **K-Means Clustering**  
   The standardized feature matrix is passed to the K-Means implementation. Each customer is assigned to one cluster.

6. **Cluster Evaluation**  
   Clustering quality is examined using objective values, silhouette analysis, and robustness checks across different random initializations.

7. **PCA Projection**  
   The standardized feature space is projected into two dimensions using PCA for visualization purposes. PCA is not currently used as the input space for clustering.

8. **Cluster Interpretation**  
   Customer-level cluster assignments are combined with cluster statistics. These statistics are then used to generate human-readable descriptions of each segment.

9. **Presentation Layer**  
   Cluster results, evaluation information, interpretations, and visualizations are passed to the Streamlit interface for presentation to the user.

The main data flow can therefore be summarized as:

```
ERP / Development Data Source
            ↓
Raw Transaction Data
            ↓
Customer Feature Engineering
            ↓
Standardized Feature Matrix
            ↓
       K-Means
            ↓
Customer Cluster Assignments
       ↙           ↘
 Evaluation      Interpretation
       ↓              ↓
   PCA / Plots    Cluster Summaries
       ↘              ↙
        Streamlit Interface
```

## Separation of Concerns

The project separates major responsibilities so that changes in one part of the system have minimal impact on the others.

- **Data access** is isolated inside the ERP layer. The rest of the application does not need to know the implementation details of the real database connection.
- **Data preparation and feature engineering** are handled separately from the user interface.
- **Clustering and evaluation logic** are kept separate from visualization and presentation code.
- **Cluster interpretation** is implemented independently from the clustering algorithm itself.
- **Visualization logic** is separated from the main Streamlit page where possible.
- **The Streamlit interface** acts primarily as the presentation and interaction layer rather than containing the full analysis logic.

This structure makes the application easier to maintain, test, and extend. For example, a different ERP data source can be introduced by implementing the same data-access interface without rewriting the clustering pipeline.

## Architectural Boundaries

The main architectural boundaries are:

```
Data Source Layer
    ↓
Processing / Analysis Layer
    ↓
Interpretation / Visualization Layer
    ↓
User Interface Layer
```

Each layer should communicate through clearly defined inputs and outputs rather than directly depending on implementation details from unrelated layers.

Sensitive database configuration and credentials remain outside the analysis and user-interface layers and are supplied through local environment configuration.