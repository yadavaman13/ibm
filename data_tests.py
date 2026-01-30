import os
import sys
import pandas as pd

FILES = [
    "crop_yield.csv",
    "state_soil_data.csv",
    "state_weather_data_1997_2020.csv",
]

def detect_datetime_series(s):
    # try to coerce to datetime and see fraction parsed
    coerced = pd.to_datetime(s, errors='coerce')
    parsed_frac = coerced.notna().sum() / max(1, len(coerced))
    if parsed_frac >= 0.6:
        return True, coerced
    return False, coerced


def analyze_file(path):
    print(f"\n--- Analyzing: {path} ---")
    if not os.path.exists(path):
        print(f"MISSING: file not found: {path}")
        return {"status":"missing"}
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"ERROR reading CSV: {e}")
        return {"status":"read-error","error":str(e)}

    nrows, ncols = df.shape
    print(f"Rows: {nrows}, Columns: {ncols}")

    # overall missing
    total_cells = nrows * ncols
    missing_total = df.isna().sum().sum()
    print(f"Total missing cells: {missing_total} ({missing_total/total_cells:.2%} of all cells)")

    # per-column summary
    print("\nColumn summary:")
    summary = []
    for col in df.columns:
        col_ser = df[col]
        missing = col_ser.isna().sum()
        missing_pct = missing / max(1, nrows)
        dtype = col_ser.dtype
        unique = col_ser.nunique(dropna=True)
        col_info = {
            "column": col,
            "dtype": str(dtype),
            "missing": int(missing),
            "missing_pct": float(missing_pct),
            "unique": int(unique),
        }
        print(f"- {col}: dtype={dtype}, missing={missing} ({missing_pct:.2%}), unique={unique}")

        # sample problematic rows for this column
        if missing > 0:
            print(f"  Sample rows with missing in '{col}':")
            print(df[df[col].isna()].head(3).to_string(index=False))

        # numeric stats
        if pd.api.types.is_numeric_dtype(col_ser):
            desc = col_ser.describe()
            print(f"  Numeric: mean={desc.get('mean')}, min={desc.get('min')}, max={desc.get('max')}")
        else:
            # detect datetime-like
            is_dt, coerced = detect_datetime_series(col_ser.dropna())
            if is_dt:
                try:
                    rng = (coerced.min(), coerced.max())
                    print(f"  Detected datetime-like: range {rng[0]} -> {rng[1]}")
                except Exception:
                    pass

        summary.append(col_info)

    # duplicates
    dup_count = df.duplicated().sum()
    print(f"\nDuplicate rows: {dup_count} ({dup_count/nrows:.2%} of rows)" if nrows>0 else "\nDuplicate rows: 0")

    # small sample of anomalies: rows with any missing
    if missing_total > 0:
        print("\nRows with any missing values (up to 5 shown):")
        print(df[df.isna().any(axis=1)].head(5).to_string(index=False))

    # return summary dict
    return {
        "status": "ok",
        "rows": int(nrows),
        "cols": int(ncols),
        "missing_total": int(missing_total),
        "duplicates": int(dup_count),
        "columns": summary,
    }


def main():
    base = os.path.dirname(__file__)
    all_results = {}
    for fname in FILES:
        path = os.path.join(base, fname)
        res = analyze_file(path)
        all_results[fname] = res

    print("\n=== Summary ===")
    for k,v in all_results.items():
        print(f"{k}: {v.get('status')}, rows={v.get('rows')}, cols={v.get('cols')}, missing={v.get('missing_total')}, duplicates={v.get('duplicates')}")

    # exit code: 0 (script completed). Do not fail automatically.
    sys.exit(0)

if __name__ == '__main__':
    main()
