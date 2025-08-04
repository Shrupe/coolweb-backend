import pandas as pd
import requests
from tqdm import tqdm
import time
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert 

API_URL = "http://localhost:8000/api/v1/websites/"
CSV_PATH = "websites_extended.csv"

def get_existing_websites():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        websites = response.json()
        return {site["url"].strip().lower(): site["id"] for site in websites}
    except Exception as e:
        print(f"Error fetching existing websites: {e}")
        return {}

def import_csv_to_api(csv_path):
    df = pd.read_csv(
        csv_path, 
        quotechar='"', 
        encoding="utf-8", 
        skip_blank_lines=True
    )

    existing_websites = get_existing_websites()

    for _, row in tqdm(df.iterrows(), total=len(df)):
        url = row.get("URL")
        if pd.isna(url) or not isinstance(url, str) or not url.strip():
            print(f"Skipping row with missing or invalid URL: {row}")
            continue
        name = row["Name"]        
        url = row["URL"].strip().lower()
        description = row["Description"]
        tags = []

        # Use Category and Subcategory as tags if they exist
        if not pd.isna(row.get("Category")):
            tags.append(row["Category"].strip())
        if not pd.isna(row.get("Subcategory")):
            tags.append(row["Subcategory"].strip())

        website_data = {
            "name": name,
            "url": url,
            "description": description,
            "tags": tags,
            "screenshot_url": None
        }

        try:
            if url in existing_websites:
                # Update existing record (use PATCH or PUT as per your API design)
                website_id = existing_websites[url]
                res = requests.put(f"{API_URL}{website_id}/", json=website_data)
                if res.status_code == 200:
                    print(f"Updated: {name}")
                else:
                    print(f"Failed to update {name} — {res.status_code}: {res.text}")
            else:
                # Create new record
                res = requests.post(API_URL, json=website_data)
                if res.status_code == 201:
                    print(f"Added: {name}")
                else:
                    print(f"Failed to add {name} — {res.status_code}: {res.text}")
        except Exception as e:
            print(f"Error processing {name}: {e}")

        time.sleep(0.2)

if __name__ == "__main__":
    import_csv_to_api(CSV_PATH)
