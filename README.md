# CDC Data Pipeline

## Overview
This project demonstrates a Change Data Capture (CDC) pipeline using Python.

## Architecture
Bronze → Silver → Gold

## Tech Stack
- Python
- Pandas

## Features
- Incremental data processing
- Deduplication
- CDC logic using timestamp

## How to Run

```bash
python3 generate_data.py
python3 cdc_pipeline.py