import requests
import pandas as pd

years = [2020, 2021, 2022, 2023, 2024]

api_url = "https://graphql.anilist.co"

query = """
query ($year: Int, $page: Int) {
  Page(page: $page, perPage: 50) {
    media(type: ANIME, seasonYear: $year) {
      title {
        romaji
      }
      genres
      averageScore
      popularity
    }
    pageInfo {
      hasNextPage
    }
  }
}
"""

anime_data = []

for year in years:
    print(f"Fetching data for year {year}...")
    page = 1
    total_animes = 0
    max_animes = 250
    
    while total_animes < max_animes:
        variables = {"year": year, "page": page}
        response = requests.post(api_url, json={"query": query, "variables": variables})
        
        if response.status_code == 200:
            result = response.json()["data"]["Page"]
            data = result["media"]
            page_info = result["pageInfo"]
            
            for anime in data:
                anime_data.append({
                    "Title": anime["title"]["romaji"],
                    "Genres": ", ".join(anime["genres"]),
                    "Score": anime.get("averageScore", "N/A"),
                    "Popularity": anime.get("popularity", "N/A"),
                    "Year": year
                })
                total_animes += 1
                
                if total_animes >= max_animes:
                    break
            
            if not page_info["hasNextPage"]:
                break
            
            page += 1
        else:
            print(f"Error fetching data for year {year}: {response.status_code}")
            break

df = pd.DataFrame(anime_data)

csv_filename = "anilist_genres_years.csv"
df.to_csv(csv_filename, index=False)

print(f"Data fetching complete. Results saved to {csv_filename}.")
