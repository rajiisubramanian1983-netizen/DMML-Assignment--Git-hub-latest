import os
import shutil
import time
import logging
from datetime import date

# Base project path
base = r"D:\M.Tech\Second Sem\Data Management ML\Assignment\recomart_pipeline"

# Create only the folders this script needs
os.makedirs(f"{base}\\data_lake\\raw\\batch\\kaggle_ecommerce", exist_ok=True)
os.makedirs(f"{base}\\logs", exist_ok=True)

log_dir = f"{base}\\logs"
log_file = os.path.join(log_dir, f"kaggle_ingestion_{date.today().isoformat()}.log")

logger = logging.getLogger("kaggle_ingestion")
logger.setLevel(logging.INFO)

if not logger.handlers:
    fh = logging.FileHandler(log_file)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(sh)

logger.info("Logging initialized for Kaggle batch ingestion.")


def ingest_kaggle_batch(source_path, retries=3, delay=5):
    """
    Copies the Kaggle CSV into the partitioned raw data lake folder.
    Includes retry logic, logging, and record count.
    """
    ingestion_date = date.today().isoformat()
    dest_folder = os.path.join(base, "data_lake", "raw", "batch", "kaggle_ecommerce", f"ingestion_date={ingestion_date}")
    os.makedirs(dest_folder, exist_ok=True)

    filename = "2019-Oct.csv"
    dest_path = os.path.join(dest_folder, filename)

    attempt = 0
    while attempt < retries:
        try:
            logger.info(f"Attempt {attempt + 1}: Starting copy of {filename}")
            shutil.copy(source_path, dest_path)

            logger.info("Counting records...")
            with open(dest_path, "r", encoding="utf-8") as f:
                row_count = sum(1 for _ in f) - 1  # minus 1 for header row

            logger.info(f"SUCCESS: {filename} copied to {dest_path} ({row_count:,} records)")
            return dest_path
        except Exception as e:
            attempt += 1
            logger.error(f"FAILED attempt {attempt}: {e}")
            if attempt < retries:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error(f"All {retries} attempts failed for {filename}")
                raise

    return None


if __name__ == "__main__":
    source_path = r"D:\M.Tech\Second Sem\Data Management ML\Assignment\2019-Oct.csv\2019-Oct.csv"
    result_path = ingest_kaggle_batch(source_path)
    print(f"\nFinal result: {result_path}")