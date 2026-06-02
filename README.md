# E-Commerce Customer Segmentation Pipeline

A Python, SQL, and Power BI customer segmentation project that:

- cleans raw e-commerce transaction data
- computes RFM metrics: Recency, Frequency, Monetary
- clusters customers with K-Means
- exports business-ready outputs for Power BI

## Project Highlights

- Handles missing values, duplicate rows, invalid quantities, and negative prices
- Builds customer-level RFM features from transactional data
- Trains a K-Means model and labels segments such as High Value and At Risk
- Produces CSV outputs and charts for dashboarding
- Includes a SQL script to compute the same RFM table in a database

## Folder Structure

- `src/` - Python pipeline code
- `sql/` - RFM SQL query
- `dashboard/` - Power BI notes and dashboard guidance
- `data/` - raw and processed data folders
- `outputs/` - generated artifacts, models, and plots

## How to Run

1. Install dependencies:
   - `pip install -r requirements.txt`

2. Add your transaction file to:
   - `data/raw/transactions.csv`

   Expected columns:
   - `customer_id`
   - `invoice_no`
   - `invoice_date`
   - `quantity`
   - `unit_price`

   Optional columns:
   - `description`
   - `country`

3. Run the pipeline:
   - `python -m src.main`

The pipeline will generate:

- `outputs/cleaned_transactions.csv`
- `outputs/rfm_customers.csv`
- `outputs/segment_summary.csv`
- `outputs/models/kmeans_model.joblib`
- `outputs/plots/*.png`

## Sample Outputs

The model produces segment labels that can be used in Power BI:

- High Value
- Loyal
- Promising
- At Risk

## SQL

The file `sql/rfm_metrics.sql` can be used to reproduce the RFM aggregation inside a warehouse or relational database.

## Power BI Dashboard

Recommended visuals:

- KPI cards for total customers, total revenue, average order value
- bar chart for segment counts
- scatter plot for frequency vs monetary with recency color scale
- matrix table for segment-level averages
- slicers for country and segment

## Notes

- If `data/raw/transactions.csv` is missing, the pipeline can generate a synthetic demo dataset.
- Replace the synthetic sample with real transaction data before presenting the project publicly.
