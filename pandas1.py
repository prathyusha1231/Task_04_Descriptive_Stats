import pandas as pd


FILENAMES = [
    "period_03/2024_fb_posts_president_scored_anon.csv",
    "period_03/2024_fb_ads_president_scored_anon.csv",
    "period_03/2024_tw_posts_president_scored_anon.csv"
]
PAGE_GROUP_LIMIT = 5
AD_GROUP_LIMIT = 5

for fname in FILENAMES:
    print(f"\n===== PROCESSING FILE: {fname} =====")
    df = pd.read_csv(fname, encoding="utf-8")

    
    print("\n--- Numeric Summary ---")
    numeric_summary = df.describe().T[['count', 'mean', 'std', 'min', 'max']]
    print(numeric_summary)

    
    print("\n--- Non-Numeric Summary ---")
    non_numeric = df.select_dtypes(exclude=['number']).columns
    for col in non_numeric:
        vc = df[col].value_counts(dropna=False)
        unique = vc.shape[0]
        top5 = vc.head(5).to_dict()
        print(f"{col:30s} unique={unique:5d} top5={top5}")

    # Group by page_id 
    if 'page_id' in df.columns:
        print(f"\n--- Grouped by page_id (first {PAGE_GROUP_LIMIT} groups) ---")
        for i, (page, group) in enumerate(df.groupby('page_id')):
            if i >= PAGE_GROUP_LIMIT:
                print("... truncated ...")
                break
            print(f"\n-- page_id = {page} --")
            print(group.describe().T[['count', 'mean', 'std', 'min', 'max']])

    # Group by page_id and ad_id 
    if {'page_id','ad_id'}.issubset(df.columns):
        print(f"\n--- Grouped by (page_id, ad_id) (first {AD_GROUP_LIMIT} groups) ---")
        for i, ((page, ad), group) in enumerate(df.groupby(['page_id', 'ad_id'])):
            if i >= AD_GROUP_LIMIT:
                print("... truncated ...")
                break
            print(f"\n-- page_id = {page}, ad_id = {ad} --")
            print(group.describe().T[['count', 'mean', 'std', 'min', 'max']])

