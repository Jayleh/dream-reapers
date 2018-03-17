movie_query = input("What Movie would you like to search? ")
omdbapi = "e8913e4c"
omdb1 = "http://www.omdbapi.com/?t="
omdb2 = "&apikey="

moviedbapi = "87594855563381b8f9fa3b3224c9f19f"
idURL = "https://api.themoviedb.org/3/search/movie?query="
idURL1 = "&api_key="
detailURL = "https://api.themoviedb.org/3/movie/"
detailURL1 = "?api_key="

# prepare to search by twitter hashtag
movie_search = movie_query.replace(" ", "")
movie_search = movie_search.replace(":", "")
movie_search = movie_search.replace("’", "")
movie_search = movie_search.replace(".", "")
movie_search = movie_search.replace(",", "")
movie_search = movie_search.replace("!", "")
movie_search = movie_search.replace("?", "")
movie_search = movie_search.replace("-", "")
movie_search = movie_search.replace("&", "")
movie_search = movie_search.replace("$", "")
movie_search = "#" + movie_search
# print (movie_query)
# print (f'Searching Twitter for {movie_search}')
publicTweets = api.search(movie_search, count=100)
compoundList = []
for tweet in publicTweets['statuses']:
    text = tweet['text']
    results = analyzer.polarity_scores(text)
    compound = results['compound']
    compoundList.append(compound)
twitter_compound = np.mean([compoundList])
print(f'{movie_query} has a Vader Compound Score of {twitter_compound.round(2)}')
#-----------------------------------------------------------------------
# print ('Searching API')
omdb_url = omdb1 + movie_query + omdb2 + omdbapi
# print (omdb_url)
try:
    q_json = requests.get(omdb_url).json()
    rated = q_json['Rated']
    rated_col = r_df['rated']
#     print(rated_col)
    counter = 0
    for name in rated_col:
        if name == rated:
            r_index = counter
        else:
            counter = counter + 1
    r_int = r_df['intercept'][r_index]
    r_m = r_df['slope'][r_index]
    rscore = (r_int + (r_m * twitter_compound)).round(2)
    print(f'{movie_query} is rated: {rated}')
    print(f'Based on this rating, we expect a Movie Success Score of {rscore}')

except:
    print(f'Could not find rating for {movie_query}')

print("---------------------------------------------------------------------------------")

id_query = idURL + movie_query + idURL1 + moviedbapi
# print (id_query)
try:
    moviedbquery = requests.get(id_query).json()
    movie_idnumber = moviedbquery['results'][0]['id']
#     print (movie_idnumber)
    details_URL = detailURL + str(movie_idnumber) + detailURL1 + moviedbapi
#     print (details_URL)
    details_URL_json = requests.get(details_URL).json()
    genreList = []
    for entry in details_URL_json['genres']:
        #         print (entry)
        g_name = entry['name']
        genreList.append(g_name)
#     print (genreList)
    for genre in genreList:
        for g in genres:
            if genre == g:
                matchGenre = genre
    g_counter = 0
    for name in genres:
        if name == matchGenre:
            g_index = g_counter
        else:
            g_counter = g_counter + 1
#     print (g_index)
    g_int = g_df['intercept'][g_index]
#     print (g_int)
    g_m = g_df['slope'][g_index]
#     print (g_m)
    g_score = (g_int + (g_m * twitter_compound)).round(2)
    print(f"{movie_query} has the genre: {matchGenre}")
    print(f'Based on this genre, we expect a Movie Success Score of {g_score}')
except:
    print(f"Could not find a genre match for {movie_query}")
print("---------------------------------------------------------------------------------")

z_score = (zintercept + (zslope * twitter_compound)).round(2)
print(f'Based on Vader Sentiment Analysis, we expect an overall Movie Success Score of {z_score}')
