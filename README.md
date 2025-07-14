# Dataset Exploration and Summary

This repository demonstrates three approaches to analyzing 2024 US Presidential Election social media data using **Pure Python**, **Pandas**, and **Polars**. The analysis explores 293,058 social media posts and advertisements across Facebook and Twitter platforms. The same descriptive statistics are replicated using:

- **Pure Python** 
- **Pandas**
- **Polars**

Throughout, the approaches are compared, challenges are highlighted, recommendations are offered for data analysts.

---

## File Structure

- `pure_python.py`      | Implementation with the Python standard library (no third‑party dependencies).
- `pandas1.py`           | Loading and analysis using pandas 
- `polars1.py`           | Loading and analysis using Polars 
- `dataexploration.py`   | Initial data exploration and structure analysis
- `election_visualizations.py`   | Visualizing insights
- `README.md` - This file

---

## Dataset

- **Facebook Posts**: 19,009 organic posts with engagement metrics
- **Facebook Ads**: 246,745 political advertisements with spending data  
- **Twitter Posts**: 27,304 tweets with interaction statistics


## How to Run

```bash
# Pure Python approach
python pure_python.py

# Pandas approach  
python pandas1.py

# Polars approach
python polars1.py

# For Visulaizations
pip install matplotlib seaborn pandas
python election_visualizations.py
```

## Scripts Overview

### 1. Pure Python (`script1_pure_python.py`)

- **Load**: `csv.reader`
- **Numeric stats**: Manual loop, strip commas (`"268,841" → 268841`), compute `count`, `mean`, `min`, `max`, `std`.
- **Non‑numeric**: Track unique values and top‑5 frequencies.
- **Grouping**: Build dictionaries to aggregate by `page_id` and `(page_id, ad_id)`.

### 2. Pandas (`script2_pandas.py`)

- **Load**: `pd.read_csv()`
- **Numeric stats**: `df.describe().T[['count','mean','std','min','max']]`
- **Non‑numeric**: `.value_counts().head()` + `.nunique()`
- **Grouping**: `.groupby('page_id').describe()` and `.groupby(['page_id','ad_id']).describe()`

### 3. Polars (`script3_polars.py`)

- **Load**: `pl.read_csv()`
- **Numeric stats**: `df.select(numeric_cols).describe()`
- **Non‑numeric**: `df.groupby(col).agg(pl.len().alias('count')).sort('count', descending=True)`
- **Grouping**: Filter by unique `page_id` / `(page_id, ad_id)` and `.describe()` on each subset.

---

## Comparison of Approaches

| Feature                   | Pure Python         | Pandas                     | Polars                          |
| ------------------------- | ------------------- | -------------------------- | ------------------------------- |
| **Dependencies**          | None                | pandas                     | polars                          |
| **Lines of code**         | High (manual loops) | Medium (API calls)         | Medium (API calls)              |
| **Parsing flexibility**   | Manual              | High (parse\_dates, dtype) | Growing (efficient CSV parsing) |
| **Statistical functions** | Manual formulas     | Built‑in methods           | Built‑in methods                |
| **Grouping**              | Custom dicts        | `.groupby()`               | `.groupby()`                    |
| **Performance**           | Seconds–tens of sec | \~1–2 seconds              | <1 second                       |

**Key challenges**:

- Handling comma‑formatted numbers (`"268,841"`); Handled by stripping commas in Pure Python, while Pandas and Polars handled this automatically during CSV parsing.
- Distinguishing zeros from missing values. Distinguished empty strings from zeros by checking for stripped empty values before numeric conversion.
- API quirks: Polars' sort parameter, Pandas skipping empty columns in `describe()`.

---

## Key Findings

### Scale of Political Advertising
- **Facebook ads dominated**: 246,745 ads vs 19,009 organic posts (13:1 ratio)
- **Total spending**: $262+ million across all advertisements
- **Top advertiser**: "HARRIS FOR PRESIDENT" (49,788 ads)

### Engagement Patterns
- **Extreme inequality**: Standard deviation often exceeded mean values
- **Facebook**: Average 4,190 interactions (range: 0 to 696,853)
- **Twitter**: Average 6,914 likes (range: 0 to 915,221)
- **Viral content**: Few posts received massive engagement while most stayed under 1,000 interactions

### Content Analysis
- **Economy focus**: Top political topic (12% of ads, 16% of Twitter posts)
- **Advocacy messaging**: 55% of all content across platforms
- **Attack content**: 27% of ads, 31% of Twitter posts
- **Quality concerns**: 19% of ads showed incivility, 7% flagged for potential scams

---

## Performance

On a \~250 K‑row ads file:

- **Pure Python**: several seconds (single-pass) to tens of seconds (multiple passes).
- **Pandas**: \~1–2 s to load and summarize.
- **Polars**: <1 s for load and summary (Rust + SIMD optimizations).

---

## Recommendations for Analysts

1. **Start with Pandas** for quick insights and a rich ecosystem.
2. **Use pure Python** if you need to teach fundamentals or remove dependencies.
3. **Adopt Polars** when you need maximum performance on large datasets.

---

## AI‑Generated Code Patterns

When asked for descriptive stats on CSVs, coding AI tools typically default to Pandas.
This is a solid recommendation for most data analysis tasks due to Pandas' balance of functionality and ease of use.

---

## Data Cleaning & Next Steps

- **Parse dates**: Convert `Post Created` into proper `datetime`, then split date/time.
- **Unpack JSON columns**: `delivery_by_region`, `demographic_distribution` can be normalized into multiple columns.
- **Handle nulls**: Decide when empty strings mean zero vs missing.
- **Benchmark**: Add simple timing (`time.perf_counter()`) around each script to profile hot spots.

---

## Conclusion

- **Pandas**: Best balance of ease, flexibility, and community support.
- **Pure Python**: Great for learning and zero-dependency demos.
- **Polars**: Top choice when speed and low overhead are critical.


