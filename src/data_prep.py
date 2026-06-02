from __future__ import annotations

from pathlib import Path

import pandas as pd


COLUMN_ALIASES = {
    "customerid": "customer_id",
    "customer_id": "customer_id",
    "invoice": "invoice_no",
    "invoiceno": "invoice_no",
    "invoice_no": "invoice_no",
    "invoicedate": "invoice_date",
    "invoice_date": "invoice_date",
    "quantity": "quantity",
    "unitprice": "unit_price",
    "unit_price": "unit_price",
    "description": "description",
    "country": "country",
}

REQUIRED_COLUMNS = ["customer_id", "invoice_no", "invoice_date", "quantity", "unit_price"]


def load_transactions(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [str(col).strip() for col in df.columns]
    return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    for column in df.columns:
        key = column.strip().lower().replace(" ", "_")
        if key in COLUMN_ALIASES:
            rename_map[column] = COLUMN_ALIASES[key]
    return df.rename(columns=rename_map)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df).copy()

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    df = df.drop_duplicates()

    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["invoice_no"] = df["invoice_no"].astype(str).str.strip()
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    for column in ["customer_id", "invoice_no", "invoice_date", "quantity", "unit_price"]:
        df.loc[df[column].isin(["", "nan", "None"]), column] = pd.NA

    df = df.dropna(subset=REQUIRED_COLUMNS)
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]
    df = df[~df["invoice_no"].str.startswith("C", na=False)]

    if "description" in df.columns:
        df["description"] = df["description"].fillna("Unknown")
    if "country" in df.columns:
        df["country"] = df["country"].fillna("Unknown")

    df["total_price"] = df["quantity"] * df["unit_price"]
    return df.sort_values(["customer_id", "invoice_date", "invoice_no"]).reset_index(drop=True)


def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    reference_date = df["invoice_date"].max() + pd.Timedelta(days=1)

    rfm = (
        df.groupby("customer_id")
        .agg(
            recency=("invoice_date", lambda dates: (reference_date - dates.max()).days),
            frequency=("invoice_no", "nunique"),
            monetary=("total_price", "sum"),
            first_purchase=("invoice_date", "min"),
            last_purchase=("invoice_date", "max"),
            country=("country", lambda values: values.mode().iat[0] if not values.mode().empty else "Unknown"),
        )
        .reset_index()
    )

    rfm["avg_order_value"] = rfm["monetary"] / rfm["frequency"].replace(0, pd.NA)
    return rfm.sort_values("monetary", ascending=False).reset_index(drop=True)
