import pandas as pd
import requests
import time
import re

# Load your existing items metadata file
items = pd.read_csv("data/itemsclean_with_metadata.csv")

def extract_first_isbn(value):
    """
    Extract the first valid-looking ISBN from the ISBN Valid column.
    Some rows have several ISBNs separated by ; or spaces.
    """
    if pd.isna(value):
        return None

    value = str(value)

    # Split when there are several ISBNs
    candidates = re.split(r"[;, ]+", value)

    for candidate in candidates:
        candidate = candidate.replace("-", "").strip()

        if len(candidate) in [10, 13]:
            return candidate

    return None


def fetch_google_books(isbn):
    """
    Fetch book metadata from Google Books API using ISBN.
    """
    if not isbn:
        return {
            "api_title": None,
            "api_authors": None,
            "api_publisher": None,
            "api_published_date": None,
            "api_description": None,
            "api_categories": None,
            "api_thumbnail": None,
        }

    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "items" not in data:
            return {
                "api_title": None,
                "api_authors": None,
                "api_publisher": None,
                "api_published_date": None,
                "api_description": None,
                "api_categories": None,
                "api_thumbnail": None,
            }

        volume_info = data["items"][0].get("volumeInfo", {})

        return {
            "api_title": volume_info.get("title"),
            "api_authors": ", ".join(volume_info.get("authors", [])) if volume_info.get("authors") else None,
            "api_publisher": volume_info.get("publisher"),
            "api_published_date": volume_info.get("publishedDate"),
            "api_description": volume_info.get("description"),
            "api_categories": ", ".join(volume_info.get("categories", [])) if volume_info.get("categories") else None,
            "api_thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
        }

    except Exception as e:
        print(f"Error with ISBN {isbn}: {e}")

        return {
            "api_title": None,
            "api_authors": None,
            "api_publisher": None,
            "api_published_date": None,
            "api_description": None,
            "api_categories": None,
            "api_thumbnail": None,
        }


# Extract one ISBN per book
items["first_isbn"] = items["ISBN Valid"].apply(extract_first_isbn)

# Call the API for each book
api_results = []

for idx, row in items.iterrows():
    isbn = row["first_isbn"]
    api_data = fetch_google_books(isbn)
    api_results.append(api_data)

    if idx % 50 == 0:
        print(f"Processed {idx} books")

    # Small pause to avoid sending requests too fast
    time.sleep(0.2)

# Convert API results to dataframe
api_df = pd.DataFrame(api_results)

# Combine original data with API data
items_enriched_api = pd.concat([items, api_df], axis=1)

# Save enriched file
items_enriched_api.to_csv("data/items_enriched_api.csv", index=False)

print("Done. Saved to data/items_enriched_api.csv")