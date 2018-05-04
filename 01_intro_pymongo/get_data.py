import requests
import json
from multiprocessing import Pool

def get_apikey(filename='apikey.txt'):
    """Gets the API key from aux file"""
    with open(filename, 'r') as f:
        return f.read().strip()

def search_movies(search):
    """Returns list of all movies returned by the OMDb API from the search"""
    search = search.lower().replace(' ', '+')
    page = 1
    movies = []
    while True:
        url = "http://www.omdbapi.com/?apikey={}&s={}&type=movie&page={}".format(apikey, search, page)
        r = requests.get(url)
        assert r.status_code == 200
        r = r.json()
        if (r['Response'] != "True"): 
            break
        movies.extend(r['Search'])
        page += 1
    return movies

def get_movie_data(imdb_id):
    """
    Simply fetches the answer from the OMDb API for the movie 
    with the given imdb_id.
    """
    url = "http://www.omdbapi.com/?apikey={}&i={}".format(apikey, imdb_id)
    r = requests.get(url)
    trys = 3
    while r.status_code != 200 and trys > 0:
        r = requests.get(url)
        trys -= 1
    if trys == 0:
        return {"Response": "False", "Error": "Connection Error"}
    else:
        r = r.json()
        assert r['Response'] == "True"
        return r


if __name__ == '__main__':

    apikey = get_apikey(filename='apikey.txt')
    movies = search_movies("Friday the 13th")
    imdb_ids = [movie["imdbID"] for movie in movies]
    with Pool() as p:
        jason = p.map(get_movie_data, imdb_ids)
    with open('jason.json', 'w') as f:
        json.dump(jason, f)
    

