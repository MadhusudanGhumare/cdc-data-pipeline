import pandas as pd
import os

# -------------------------
# STEP 1: BRONZE
# -------------------------
df = pd.read_csv("data/source_data.csv")
df.to_csv("data/bronze.csv", index=False)
print("Bronze layer created")

# -------------------------
# STEP 2: SILVER
# -------------------------
df_silver = df.drop_duplicates(subset=["id"])
df_silver.to_csv("data/silver.csv", index=False)
print("Silver layer created")

# -------------------------
# STEP 3: GOLD (CDC)
# -------------------------
gold_path = "data/gold.csv"

if os.path.exists(gold_path):
    df_gold = pd.read_csv(gold_path)

    # Combine old + new
    df_combined = pd.concat([df_gold, df_silver])

    # Keep latest record per id
    df_combined = df_combined.sort_values("updated_at") \
                             .drop_duplicates("id", keep="last")
else:
    df_combined = df_silver

df_combined.to_csv(gold_path, index=False)

print("Gold layer updated (CDC applied)")