from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sales_data.csv"
DATABASE_FILE = BASE_DIR / "etl_pipeline.db"


@dataclass
class SaleRecord:
    order_id: int
    customer_name: str
    product: str
    quantity: int
    unit_price: float
    total_amount: float


def create_sample_input_file(file_path: Path) -> None:
    """Create a small CSV file so the pipeline can run end-to-end."""
    rows = [
        ["order_id", "customer_name", "product", "quantity", "unit_price"],
        [1, "Maddy", "Keyboard", 2, 45.50],
        [2, "Alex", "Mouse", 1, 18.00],
        [3, "Jordan", "Monitor", 2, 210.25],
        [4, "Sam", "USB Cable", 3, 7.99],
    ]

    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)


def extract(file_path: Path) -> list[dict[str, str]]:
    """Read raw data from a CSV file."""
    if not file_path.exists():
        create_sample_input_file(file_path)

    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def transform(rows: Iterable[dict[str, str]]) -> list[SaleRecord]:
    """Clean and enrich raw rows before loading."""
    transformed_rows: list[SaleRecord] = []

    for row in rows:
        quantity = int(row["quantity"])
        unit_price = float(row["unit_price"])
        transformed_rows.append(
            SaleRecord(
                order_id=int(row["order_id"]),
                customer_name=row["customer_name"].strip().title(),
                product=row["product"].strip(),
                quantity=quantity,
                unit_price=unit_price,
                total_amount=round(quantity * unit_price, 2),
            )
        )

    return transformed_rows


def load(records: Iterable[SaleRecord], database_path: Path) -> None:
    """Load transformed data into a SQLite table."""
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                order_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_amount REAL NOT NULL
            )
            """
        )

        cursor.executemany(
            """
            INSERT OR REPLACE INTO sales (
                order_id,
                customer_name,
                product,
                quantity,
                unit_price,
                total_amount
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    record.order_id,
                    record.customer_name,
                    record.product,
                    record.quantity,
                    record.unit_price,
                    record.total_amount,
                )
                for record in records
            ],
        )
        connection.commit()


def run_etl() -> None:
    raw_rows = extract(INPUT_FILE)
    clean_rows = transform(raw_rows)
    load(clean_rows, DATABASE_FILE)
    print(f"ETL pipeline completed successfully. Loaded {len(clean_rows)} rows.")
    print(f"Source CSV: {INPUT_FILE}")
    print(f"SQLite DB: {DATABASE_FILE}")


if __name__ == "__main__":
    run_etl()
