# Power BI Dashboard Guide

Use the exported file `outputs/rfm_customers_segmented.csv` or the SQL RFM output as your Power BI data source.

## Suggested Visuals

1. KPI cards
   - Total Customers
   - Total Revenue
   - Average Order Value
   - High Value Customers

2. Segment distribution bar chart
   - Axis: `segment`
   - Values: customer count

3. Scatter chart
   - X-axis: `frequency`
   - Y-axis: `monetary`
   - Size: `recency`
   - Legend: `segment`

4. Matrix table
   - Rows: `segment`
   - Columns: `recency`, `frequency`, `monetary`, `avg_order_value`

5. Slicers
   - `country`
   - `segment`

## Useful DAX Measures

- Total Customers = DISTINCTCOUNT(rfm_customers_segmented[customer_id])
- Total Revenue = SUM(rfm_customers_segmented[monetary])
- Average Order Value = DIVIDE([Total Revenue], SUM(rfm_customers_segmented[frequency]))

## Storytelling Angle

- Identify the most valuable customers
- Highlight customers at churn risk
- Show how buying frequency and spend differ across segments
- Help marketing teams target promotions by segment
