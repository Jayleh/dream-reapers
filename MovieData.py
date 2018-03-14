
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import json

api = "87594855563381b8f9fa3b3224c9f19f"
idURL = "https://api.themoviedb.org/3/search/movie?query="
idURL1 = "&api_key="
detailURL = "https://api.themoviedb.org/3/movie/"
detailURL1 = "?api_key="


# In[2]:


csvPath = 'opening_weekend.csv'
opening = pd.read_csv(csvPath)
print(len(opening))
opening.head()


# In[3]:


# movies = opening['Title']
# print (movies)

idList = []
movieNames = []
movieList = []
grossList = []
openingMovies = []

for index, row in opening.iterrows():
    movie = row['Title']
#     finalMovie = movie.replace(":","")
#     finalMovie = movie.replace(" ","%20")
    gross = row['Weekend Gross']
    finalURL = idURL + movie + idURL1 + api
#     print (finalURL)
    json_file = requests.get(finalURL).json()
    moviesJSON = json_file['results']
#     print (moviesJSON)
#     print (len(json_file['results']))
    
    try:
        dates = []
        for n in np.arange(len(moviesJSON)):
#             print (n)
            date = moviesJSON[n]['release_date']
            date = int(date.replace("-",""))
#             print (date)
            dates.append(date)   
#         print (dates)      
#         print (recent)
    except:
        pass        
 
    try:
#         print(f'{dates}')
        new = max(dates)
        newestMovie = dates.index(new)
        recentMovie = moviesJSON[newestMovie]
        idNumber = recentMovie['id']
    #         movie = recentMovie['original_title']
        grossList.append(gross)
        movieNames.append(movie)
        idList.append(idNumber)
    except ValueError:
        pass
    
#     print(f'{movie} / {max(dates)} / {newestMovie} / {idNumber} / {gross}')
#     print('--------------------------------------------------------------------------------')
    
openingMoviesDF = pd.DataFrame({"movies":movieNames, "gross":grossList, "id_number":idList})
print (len(openingMoviesDF))
openingMoviesDF.head(50)


# In[4]:


for index, movie in openingMoviesDF.iterrows():
    detailsURL = detailURL + str(movie['id_number']) + detailURL1 + api
#     print (detailsURL)
    details = requests.get(detailsURL).json()
#     print(details)
    title = details['original_title']
#         print (title)
    budget = details['budget']
    rating = details['vote_average']
    release = details['release_date']
    weekendGross = movie['gross']
    try:
        genre = details['genres'][0]['name']
    except:
        genre = "N/A"
#     print (genre)
    movieDict = {"name": title, "gross":weekendGross, "rating": rating, "budget": budget, "release date": release, "genre":genre}
    movieList.append(movieDict)
    
moviesDF = pd.DataFrame(movieList)


# In[5]:


moviesDF = moviesDF.sort_values('budget', ascending = False)
print (len(moviesDF))
moviesDF.head(50)

