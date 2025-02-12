import requests
import pandas as pd

years = [2020, 2021, 2022, 2023, 2024]

# URL base da API do AniList
api_url = "https://graphql.anilist.co"

# Query GraphQL para buscar animes com paginação
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

# Estrutura de dados para armazenar os resultados
anime_data = []

# Loop sobre cada ano
for year in years:
    print(f"Fetching data for year {year}...")
    page = 1
    total_animes = 0
    max_animes = 250  # Número máximo de animes por ano
    
    while total_animes < max_animes:
        # Parâmetros para a query
        variables = {"year": year, "page": page}
        
        # Fazendo a requisição para a API
        response = requests.post(api_url, json={"query": query, "variables": variables})
        
        # Verificando se a requisição foi bem-sucedida
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
                
                # Verifica se já atingimos o número máximo de animes
                if total_animes >= max_animes:
                    break
            
            # Verifica se há mais páginas
            if not page_info["hasNextPage"]:
                break
            
            # Vai para a próxima página
            page += 1
        else:
            print(f"Error fetching data for year {year}: {response.status_code}")
            break

# Converte os dados para um DataFrame
df = pd.DataFrame(anime_data)

# Salva o DataFrame em um arquivo CSV
csv_filename = "anilist_genres_years.csv"
df.to_csv(csv_filename, index=False)

print(f"Data fetching complete. Results saved to {csv_filename}.")
