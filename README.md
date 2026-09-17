# ERP Customer Segmentation and Analysis System
A machine-learning-based application for analyzing ERP sales data and identifying customer segments.

## Overview
This project analyzes customer transaction data retrieved from an ERP database and groups customers according to their purchasing behavior. Customer-level features such as recency, monetary value, transaction activity, average order value, quantity, and product diversity are calculated from sales records. These features are standardized and clustered using K-Means. Cluster quality is evaluated using methods such as the elbow method and silhouette analysis, while PCA is used to visualize the resulting customer segments. The results are presented through an interactive Streamlit interface.

## Project Goals
The main objectives of the project are:
- Transform ERP sales data into meaningful customer level features.
- Identify groups of customers with similar purchasing behavior.
- Evaluate the quality and stability of the generated clusters.
- Provide interpretable descriptions of customer segments.
- Visualize customer groups through an interactive interface.
- Create a reusable analysis pipeline that can operate on ERP-derived data.

## Features
- Reads customer transaction data from an ERP database.
- Builds customer-level behavioral features from sales records.
- Standardizes numerical features before clustering.
- Performs customer segmentation using K-Means.
- Supports different values of K through the user interface.
- Evaluates clustering using elbow and silhouette analysis.
- Tests clustering robustness across different random initializations.
- Uses PCA for two-dimensional visualization.
- Generates interpretable descriptions of customer clusters.
- Displays results through a Streamlit application.

## Workflow
The application follows the pipeline below:

1. Sales and transaction data are retrieved from the ERP database.
2. Customer-level behavioral features are calculated from the raw transaction data.
3. The resulting numerical features are standardized before clustering.
4. Customers are grouped using K-Means clustering.
5. Candidate cluster configurations are evaluated using the elbow method and silhouette analysis.
6. Clustering stability is tested across different random initializations.
7. PCA is applied to obtain a two-dimensional representation of the customer segments.
8. Cluster-level statistics and interpretations are generated.
9. The resulting analysis is presented through the Streamlit user interface.

```
ERP Database
    ↓
Transaction Data
    ↓
Feature Engineering
    ↓
Standardization
    ↓
K-Means Clustering
    ↓
Evaluation & Robustness Analysis
    ↓
PCA Visualization
    ↓
Cluster Interpretation
    ↓
Streamlit Interface
```

## Technology Stack
- **Python** — Main programming language used for data processing, clustering, evaluation and application logic.
- **Pandas** — Data manipulation, feature engineering and aggregation.
- **NumPy** — Numerical operations used throughout the pipeline.
- **scikit-learn** — Used for feature standardization, PCA and silhouette analysis. The K-Means clustering algorithm itself is implemented separately within the project.
- **Streamlit** — Interactive user interface for running and exploring the customer segmentation analysis.
- **Plotly** — Interactive plotting and cluster visualization.
- **SQL** — Retrieval of transaction data from the ERP database.

## Project Structure
```
project/
├── main.py
├── docs/
│   └── ...
├── sql/
│   ├── exemplary/
│   └── private/
├── src/
│   ├── data_handler.py
│   ├── functions.py
│   ├── interpreter.py
│   └── erp/
│       ├── base.py
│       ├── fake_erp.py
│       └── logo_erp.py
├── tests/
├── ui/
│   ├── app.py
│   └── graphs.py
├── .gitignore
└── README.md
```
- `main.py` coordinates the main customer-analysis pipeline and connects the data-processing, clustering, evaluation, and interpretation components.
- The `src/` directory contains the core application logic. `data_handler.py` handles data preparation and customer-level feature generation, `functions.py` contains the main clustering and analysis functionality, and `interpreter.py` generates interpretable descriptions and statistics for the resulting customer segments.
- The `src/erp/` directory contains the data-access abstraction. `base.py` defines the common ERP interface, while `fake_erp.py` provides a synthetic or development data source. ` logo_erp.py` contains the implementation used to access the real ERP data source.
- The `ui/` directory contains the Streamlit application. `app.py` defines the main user interface, while `graphs.py` contains visualization-related functionality.
- The `sql/` directory contains SQL queries used during ERP data exploration and retrieval. Private or environment-specific queries are kept separate from reusable example queries.
- The `docs/` directory contains project documentation and analysis outputs.
- The `tests/` directory is reserved for automated tests.
- Sensitive configuration values, database credentials, private SQL details, generated cache files, and other local-only files are excluded from version control where appropriate.

## Installation

## Usage
Once the Streamlit application is running, the customer segmentation workflow can be performed through the user interface. The application is designed so that the main analysis workflow can be performed without directly modifying the underlying Python code.
1. Load or retrieve the customer transaction data from the configured data source.
2. Review the generated customer-level features.
3. Select the desired number of clusters, K.
4. Run the K-Means clustering process.
5. Inspect the elbow and silhouette analysis results to evaluate the selected clustering configuration.
6. Review the PCA visualization to examine the separation of customer segments in two dimensions.
7. Inspect the generated cluster statistics and interpretations to understand the behavioral characteristics of each customer group.
8. Export or review the generated analysis outputs where required.

## Model Evaluation
The quality and stability of the generated customer segments are evaluated using multiple methods:
- **Elbow Method** — Examines the clustering objective value across different values of K to identify where additional clusters provide diminishing improvement.
- **Silhouette Analysis** — Measures how well each customer fits within its assigned cluster compared with neighboring clusters.
- **Random Initialization Robustness** — Runs K-Means with different initial centroid selections to check whether similar clustering quality is obtained consistently.
- **PCA Visualization** — Projects the customer feature space into two dimensions to provide a visual representation of the resulting customer segments.

These methods are used together when assessing a clustering configuration rather than relying on a single evaluation metric.

## Data Privacy and Security
The project may operate on real ERP and customer transaction data. For this reason, sensitive information is kept separate from the source code and is not intended to be stored in the Git repository.
- Database credentials and environment-specific configuration values are stored locally using environment variables.
- The `.env` file is excluded from version control.
- CSV files containing real customer and transaction data are excluded from version control.
- Private and environment-specific SQL queries are kept separate from reusable example queries.
- Database access is limited to the data required for the analysis.
- Sensitive customer information should not be included in documentation, screenshots, test files, or public repository content.

The repository is intended to contain application source code and non-sensitive documentation rather than production customer data.

## Limitations
The current version of the project has several limitations:
- The clustering results depend on the quality and completeness of the available ERP transaction data.
- Customer segments are based only on the behavioral features currently included in the analysis.
- K-Means assumes relatively compact clusters and may not represent every possible customer distribution equally well.
- The number of clusters, K, must be selected based on evaluation results and user judgment.
- PCA visualizations reduce the original feature space to two dimensions and therefore do not preserve all information contained in the full dataset.
- Cluster interpretations describe observed purchasing behavior and should not be treated as predictions of future customer behavior.

## Future Improvements
Possible future improvements to the project include:
- Finalizing the installation and distribution process for easier use on other computers.
- Packaging or deploying the Streamlit application in a secure and practical way.
- Adding automated tests for data processing, clustering, and interpretation components.
- Improving validation and error handling for missing, invalid, or unexpected ERP data.
- Comparing K-Means with alternative clustering algorithms.
- Adding additional customer behavioral features where useful and supported by the available data.
- Improving cluster comparison and reporting functionality.
- Adding more detailed export options for analysis results.
- Further refining the user interface based on feedback from actual users.
- Making the data-access layer easier to adapt to different ERP systems or databases.
