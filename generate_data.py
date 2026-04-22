import pandas as pd
import random
from datetime import datetime, timedelta

rows = []

for i in range(100000):  # 100K records
    rows.append({
        "id": i,
        "name": f"user_{i}",
        "city": random.choice(["Pune", "Mumbai", "Delhi", "Bangalore"]),
        "updated_at": datetime.now() - timedelta(days=random.randint(0, 30))
    })

df = pd.DataFrame(rows)
df.to_csv("data/source_data.csv", index=False)

print("Generated 100K records")