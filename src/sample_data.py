from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


def generate_sample_transactions(output_path: str | Path, *, n_customers: int = 250, seed: int = 42) -> Path:
    """Generate a realistic synthetic e-commerce transaction dataset."""

    rng = np.random.default_rng(seed)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    profiles = [
        {"name": "high_value", "weight": 0.15, "orders": (10, 22), "qty": (2, 8), "price": (45, 180)},
        {"name": "loyal", "weight": 0.35, "orders": (5, 14), "qty": (1, 6), "price": (20, 120)},
        {"name": "occasional", "weight": 0.35, "orders": (2, 7), "qty": (1, 4), "price": (10, 80)},
        {"name": "at_risk", "weight": 0.15, "orders": (1, 4), "qty": (1, 3), "price": (5, 50)},
    ]

    customer_ids = [f"CUST-{i:05d}" for i in range(1, n_customers + 1)]
    profile_choices = rng.choice(len(profiles), size=n_customers, p=[p["weight"] for p in profiles])

    base_date = datetime(2026, 1, 1)
    rows: list[dict[str, object]] = []
    invoice_counter = 100000

    for customer_id, profile_idx in zip(customer_ids, profile_choices):
        profile = profiles[int(profile_idx)]
        order_count = int(rng.integers(profile["orders"][0], profile["orders"][1] + 1))

        for _ in range(order_count):
            invoice_date = base_date - timedelta(days=int(rng.integers(1, 365)))
            quantity = int(rng.integers(profile["qty"][0], profile["qty"][1] + 1))
            unit_price = round(float(rng.uniform(profile["price"][0], profile["price"][1])), 2)
            description = rng.choice(
                [
                    "Wireless Headphones",
                    "Ceramic Mug",
                    "Desk Lamp",
                    "Notebook Set",
                    "Premium Gift Box",
                    "Smart Speaker",
                    "Office Chair Mat",
                    "Reusable Bottle",
                ]
            )

            rows.append(
                {
                    "invoice_no": f"INV-{invoice_counter}",
                    "customer_id": customer_id,
                    "invoice_date": invoice_date.strftime("%Y-%m-%d"),
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "description": description,
                    "country": rng.choice(["United Kingdom", "United States", "Canada", "Germany", "France"]),
                }
            )
            invoice_counter += 1

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return output_path
