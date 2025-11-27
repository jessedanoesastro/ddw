import requests

BASE_URL = "http://127.0.0.1:5001/api"
USERNAME = "Jesse"
PASSWORD = "Hallo"


def get_token():
    """Vraag een token aan via Basic Auth (username/password)."""
    url = f"{BASE_URL}/tokens"
    resp = requests.post(url, auth=(USERNAME, PASSWORD))
    print("GET TOKEN status:", resp.status_code)
    print("GET TOKEN response:", resp.json())
    resp.raise_for_status()
    return resp.json()["token"]


def get_movies(token):
    """GET /api/movies – lijst van films ophalen."""
    url = f"{BASE_URL}/movies"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    print("\nGET /movies status:", resp.status_code)
    print("GET /movies JSON:", resp.json())
    resp.raise_for_status()
    return resp.json()


def create_movie(token):
    """POST /api/movies – nieuwe film aanmaken."""
    url = f"{BASE_URL}/movies"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "The Matrix",
        "year": 1999,
        "oscars": 4,
        "genre": "Sci-Fi"
    }
    resp = requests.post(url, json=payload, headers=headers)
    print("\nPOST /movies status:", resp.status_code)
    print("POST /movies JSON:", resp.json())
    resp.raise_for_status()
    return resp.json()


def update_movie(token, movie_id):
    """PUT /api/movies/<id> – film updaten."""
    url = f"{BASE_URL}/movies/{movie_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "oscars": 5,
        "genre": "Sci-Fi / Action"
    }
    resp = requests.put(url, json=payload, headers=headers)
    print(f"\nPUT /movies/{movie_id} status:", resp.status_code)
    print(f"PUT /movies/{movie_id} JSON:", resp.json())
    resp.raise_for_status()
    return resp.json()

def main():
    print("== API DEMO SCRIPT ==")
    token = get_token()
    print("\nTOKEN:", token)

    # 1. lijst films (kan eerst leeg zijn)
    get_movies(token)

    # 2. nieuwe film aanmaken
    movie = create_movie(token)
    movie_id = movie["id"]
    print("\nAangemaakte film ID:", movie_id)

    # 3. opnieuw lijst ophalen
    get_movies(token)

    # 4. film updaten
    update_movie(token, movie_id)

    # 6. nog een keer lijst ophalen
    get_movies(token)


if __name__ == "__main__":
    main()