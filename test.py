import requests
response = requests.get(f"https://api.kinopoisk.cloud/movies/1445243/token/0d12aad940f6c3a4cdd54cfce1d9e1b9")
print(response.json())
data_film = response.json()