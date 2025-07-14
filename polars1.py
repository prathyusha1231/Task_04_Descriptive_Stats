import polars as pl


FILES = [
    "period_03/2024_fb_posts_president_scored_anon.csv",
    "period_03/2024_fb_ads_president_scored_anon.csv",
    "period_03/2024_tw_posts_president_scored_anon.csv",
]

PAGE_GROUP_LIMIT = 5
PAIR_GROUP_LIMIT = 5

def overall_numeric(df, numeric_cols):
    print(df.select(numeric_cols).describe())

def overall_non_numeric(df, numeric_cols):
    for col in df.columns:
        if col not in numeric_cols:
            uniques = df[col].n_unique()
            top5 = (
                df.group_by(col)
                  .agg(pl.len().alias("count"))             
                  .sort("count", descending=True)            
                  .head(5)
                  .to_dicts()
            )
            print(f"{col:30s} unique={uniques:<5d} top5={top5}")

def group_numeric(df, by, numeric_cols, limit):
    for key in df[by].unique()[:limit].to_list():
        grp = df.filter(pl.col(by) == key)
        print(f"\n-- group {by} = {key} --")
        print(grp.select(numeric_cols).describe())

def pair_group_numeric(df, numeric_cols, limit):
    pairs = df.select(["page_id","ad_id"]).unique()[:limit].to_dicts()
    for p in pairs:
        grp = df.filter(
            (pl.col("page_id")==p["page_id"]) &
            (pl.col("ad_id")==p["ad_id"])
        )
        print(f"\n-- group (page_id,ad_id)=({p['page_id']},{p['ad_id']}) --")
        print(grp.select(numeric_cols).describe())

if __name__ == "__main__":
    for path in FILES:
        print(f"\n===== PROCESSING: {path} =====")
        df = pl.read_csv(path)

        
        numeric_cols = [
            c for c, dt in zip(df.columns, df.dtypes)
            if dt in (
                pl.Int8, pl.Int16, pl.Int32, pl.Int64,
                pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64,
                pl.Float32, pl.Float64
            )
        ]

        print("\n=== Overall Numeric Summary ===")
        overall_numeric(df, numeric_cols)

        print("\n=== Overall Non-Numeric Summary ===")
        overall_non_numeric(df, numeric_cols)

        if "page_id" in df.columns:
            print(f"\n=== By page_id (first {PAGE_GROUP_LIMIT}) ===")
            group_numeric(df, "page_id", numeric_cols, PAGE_GROUP_LIMIT)

        if {"page_id","ad_id"}.issubset(df.columns):
            print(f"\n=== By (page_id, ad_id) (first {PAIR_GROUP_LIMIT}) ===")
            pair_group_numeric(df, numeric_cols, PAIR_GROUP_LIMIT)
