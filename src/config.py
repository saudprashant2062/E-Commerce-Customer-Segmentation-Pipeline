from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
MODEL_DIR = OUTPUT_DIR / "models"
PLOT_DIR = OUTPUT_DIR / "plots"

DEFAULT_INPUT_FILE = RAW_DATA_DIR / "transactions.csv"
DEFAULT_CLEANED_FILE = OUTPUT_DIR / "cleaned_transactions.csv"
DEFAULT_RFM_FILE = OUTPUT_DIR / "rfm_customers.csv"
DEFAULT_SUMMARY_FILE = OUTPUT_DIR / "segment_summary.csv"
