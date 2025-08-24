from pathlib import Path
import pandas as pd

RENAME_MAP = {
    "Date": "date", "Symbol": "symbol",
    "Open": "open", "High": "high", "Low": "low",
    "Close": "close", "Adj Close": "adj_close", "Volume": "volume"
}

# src/cleaning.py

from pathlib import Path
import pandas as pd
import re

# --- Map raw column names to standard snake_case names
RENAME_MAP = {
    "Date": "date", "Symbol": "symbol",
    "Open": "open", "High": "high", "Low": "low",
    "Close": "close", "Adj Close": "adj_close", "Volume": "volume"
}

# -----------------------------
# 1) Function to infer symbol from filename
# -----------------------------
def infer_symbol_from_filename(filepath: Path) -> str:
    """
    Infer the stock ticker from a filename like:
      msft_historical_2025-08-24_14-18-17.csv -> MSFT
      BRK-B_historical_2025-08-24_14-18-17.csv -> BRK-B

    Steps:
      1) Take the text before the first underscore (safe for your pattern)
      2) Validate it contains only letters/numbers/dot/hyphen
      3) If invalid, try reading the CSV header for a Symbol/Ticker column
      4) If still invalid, raise an error
    """
    p = Path(filepath)
    stem = p.stem  # e.g., "msft_historical_2025-08-24_14-18-17"

    # Step 1 & 2: take first part before "_" and validate
    candidate = stem.split("_", 1)[0].upper()
    if re.fullmatch(r"[A-Z0-9\.\-]+", candidate):
        return candidate

    # Step 3: fallback using regex capture
    m = re.match(r"^([A-Za-z0-9\.\-]+?)(?:_|$)", stem)
    if m:
        return m.group(1).upper()

    # Step 4: fallback to reading CSV header
    try:
        header = pd.read_csv(p, nrows=1)
        for col in ("Symbol", "symbol", "Ticker", "ticker"):
            if col in header.columns:
                val = header[col].iloc[0]
                if pd.notna(val) and str(val).strip():
                    return str(val).upper()
    except Exception:
        pass

    raise ValueError(f"Cannot infer symbol from filename: {p.name}. "
                     "Please rename to SYMBOL_... or include Symbol column.")


# -----------------------------
# 2) Function to clean a single stock CSV
# -----------------------------
def clean_stock_file(filepath, symbol_hint: str | None = None) -> pd.DataFrame:
    """
    Read a raw CSV for a single stock, normalize columns, ensure date column,
    infer or validate 'symbol' column, sort by date, and return cleaned DataFrame.

    filepath: str or Path to the CSV
    symbol_hint: optional symbol you want to force (e.g., 'AAPL'); if provided, it is used.
    """
    p = Path(filepath)

    # --- Peek at columns
    header = pd.read_csv(p, nrows=0)
    cols = list(header.columns)
    parse_dates = ["Date"] if "Date" in cols else None

    # --- Read full CSV
    df = pd.read_csv(p, parse_dates=parse_dates)  # infer_datetime_format deprecated

    # --- Drop unnamed index columns
    unnamed_cols = [c for c in df.columns if c.startswith("Unnamed:")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    # --- Determine symbol
    final_symbol = None
    if symbol_hint:
        final_symbol = str(symbol_hint).upper()
    elif "Symbol" in df.columns:
        vals = df["Symbol"].dropna().unique().astype(str)
        if len(vals) == 1:
            final_symbol = vals[0].upper()
        elif len(vals) > 1:
            raise ValueError(f"File {p.name} contains multiple Symbols: {vals}. Please fix file.")

    if final_symbol is None:
        final_symbol = infer_symbol_from_filename(p)

    # If Symbol column exists but differs, warn and prefer Symbol column
    if "Symbol" in df.columns:
        unique_vals = df["Symbol"].dropna().unique().astype(str)
        if len(unique_vals) == 1:
            col_sym = unique_vals[0].upper()
            if col_sym != final_symbol:
                print(f"WARNING: symbol inferred {final_symbol} but file has Symbol='{col_sym}'. Using '{col_sym}'.")
                final_symbol = col_sym

    df["Symbol"] = final_symbol

    # --- Ensure Date exists and is datetime
    if "Date" not in df.columns:
        raise ValueError(f"File {p.name} does not contain a 'Date' column.")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # --- Rename columns to snake_case
    df = df.rename(columns=RENAME_MAP)

    # --- Force numeric types
    for col in ("open", "high", "low", "close", "adj_close"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "volume" in df.columns:
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").astype("Int64")

    # --- Sort by symbol/date and reset index
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)

    # --- Drop rows where date is NaT
    df = df[~df["date"].isna()].copy()

    return df


def clean_stock_file(filepath, symbol_hint: str | None = None) -> pd.DataFrame:
    """
    Read a raw CSV for a single stock, normalize columns, ensure date column,
    infer or validate 'symbol' column, sort by date, and return cleaned DataFrame.

    filepath: str or Path to the CSV
    symbol_hint: optional symbol you want to force (e.g., 'AAPL'); if provided, it is used.
    """
    p = Path(filepath)

    # --- Read header first (cheap) to check if 'Date' exists & if file already has a Symbol column
    header = pd.read_csv(p, nrows=0)
    cols = list(header.columns)

    # If the file has a 'Date' column, we'll parse it when reading full file (faster/cleaner).
    parse_dates = ["Date"] if "Date" in cols else None

    # --- Read the full CSV now, with Date parsing if available
    df = pd.read_csv(p, parse_dates=parse_dates, infer_datetime_format=True)

    # --- Drop any unnamed index column created by earlier saves, e.g. 'Unnamed: 0'
    unnamed_cols = [c for c in df.columns if c.startswith("Unnamed:")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    # --- Determine the final symbol to use
    # Priority:
    # 1) if symbol_hint provided -> use it
    # 2) if 'Symbol' column exists and has one unique non-null value -> use that
    # 3) else infer from filename (robust function)
    final_symbol = None
    if symbol_hint:
        final_symbol = str(symbol_hint).upper()
    elif "Symbol" in df.columns:
        vals = df["Symbol"].dropna().unique().astype(str)
        if len(vals) == 1:
            final_symbol = vals[0].upper()
        elif len(vals) > 1:
            raise ValueError(f"File {p.name} contains multiple Symbols: {vals}. Please fix file.")
        # else: column exists but empty, fallback to filename inference below

    if final_symbol is None:
        final_symbol = infer_symbol_from_filename(p)

    # If there is a Symbol column but its value disagrees with filename/inferred symbol, prefer the explicit column
    if "Symbol" in df.columns:
        # get unique values again (may be empty)
        unique_vals = df["Symbol"].dropna().unique().astype(str)
        if len(unique_vals) == 1:
            col_sym = unique_vals[0].upper()
            if col_sym != final_symbol:
                # warn user, but prefer the Symbol column because it came from data
                print(f"WARNING: symbol inferred {final_symbol} but file has Symbol='{col_sym}'. Using '{col_sym}'.")
                final_symbol = col_sym

    # Ensure the DataFrame has a Symbol column with the final tidy value
    df["Symbol"] = final_symbol

    # --- Ensure 'Date' column exists and is datetime
    if "Date" not in df.columns:
        raise ValueError(f"File {p.name} does not contain a 'Date' column.")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # --- Rename canonical columns to snake_case for consistency
    df = df.rename(columns=RENAME_MAP)

    # --- Enforce types on price/volume columns (coerce bad strings to NaN)
    for col in ("open", "high", "low", "close", "adj_close"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "volume" in df.columns:
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").astype("Int64")

    # --- Sort and reset index (time series order)
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)

    # --- Drop rows where date is NaT (couldn't parse)
    df = df[~df["date"].isna()].copy()

    return df
