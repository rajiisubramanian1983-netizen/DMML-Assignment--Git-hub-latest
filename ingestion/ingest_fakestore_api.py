import os
import json
import time
import logging
import requests
from datetime import date, datetime

# Base project path
base = r"D:\M.Tech\Second Sem\Data Management ML\Assignment\recomart_pipeline"

# Create only the folders this script needs
os.makedirs(f"{base}\\data_lake\\raw\\streaming\\fakestore_api", exist_ok=True)
os.makedirs(f"{base}\\logs", exist_ok=True)

log_dir = f"{base}\\logs"
fakestore_log_file = os.path.join(log_dir, f"fakestore_ingestion_{date.today().isoformat()}.log")

fakestore_logger = logging.getLogger("fakestore_ingestion")
fakestore_logger.setLevel(logging.INFO)

if not fakestore_logger.handlers:
    fh = logging.FileHandler(fakestore_log_file)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    fakestore_logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    fakestore_logger.addHandler(sh)

fakestore_logger.info("Logging initialized for FakeStoreAPI ingestion.")


def ingest_fakestore_api(retries=3, delay=5):
    """
    Polls FakeStoreAPI for product data and saves the response
    into the partitioned raw data lake folder (streaming/near-real-time source).
    """
    url = "https://fakestoreapi.com/products"
    ingestion_date = date.today().isoformat()
    dest_folder = os.path.join(base, "data_lake", "raw", "streaming", "fakestore_api", f"ingestion_date={ingestion_date}")
    os.makedirs(dest_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"products_{timestamp}.json"
    dest_path = os.path.join(dest_folder, filename)

    attempt = 0
    while attempt < retries:
        try:
            fakestore_logger.info(f"Attempt {attempt + 1}: Calling {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            with open(dest_path, "w") as f:
                json.dump(data, f, indent=2)

            fakestore_logger.info(f"SUCCESS: {len(data)} products saved to {dest_path}")
            return dest_path
        except Exception as e:
            attempt += 1
            fakestore_logger.error(f"FAILED attempt {attempt}: {e}")
            if attempt < retries:
                fakestore_logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                fakestore_logger.error(f"All {retries} attempts failed for FakeStoreAPI call")
                raise

    return None


if __name__ == "__main__":
    result_path = ingest_fakestore_api()
    print(f"\nFinal result: {result_path}")