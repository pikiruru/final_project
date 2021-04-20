from bs4 import BeautifulSoup
import requests
import json
import time

# from requests.models import Response

BASE_URL='https://www.imdb.com'
CACHE_FILE_NAME ='final_project_try.json'
CACHE_DICT = {}

def load_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILE_NAME,'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache):
    ''' Saves the current movie of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an request by its baseurl and params

    Parameters
    ----------
    baseurl: string
        The URL for the movie website
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    if params:
        unique_string = []
        connector ="_"
        for key in params.keys():
            unique_string.append(f"{key}_{params[key]}")
        unique_string.sort()
        unique_key = baseurl + connector + connector.join(unique_string)
    else:
        unique_key = baseurl
    return unique_key

def make_url_request_using_cache(url, cache, params):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    url: string
        The URL for the website
    cache: dict
        The dictionary to save
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
    '''
    unique_key = construct_unique_key(url,params)

    if (unique_key in cache.keys()):
        print("Using cache")
        return cache[unique_key]
    else:
        print("Fetching")
        time.sleep(1)
        cache[unique_key] = requests.get(url,params).text
        save_cache(cache)
        return cache[unique_key]

class Movie:
    '''a movie object

    every movie attributes
    ----------------------
    Title: string
        name of the movie(e.g.' The Godfather')

    Rating: float
        rating of a movie(e.g. 9.2)
    
    Year: integer
        year of the movie(e.g. 1972)

    Gerne: string
        gerne of the movie(e.g. 'Crime/Drama')

    Boxoffice: integer
        cumulative worldwide gross box office($) (e.g. 246,120,986)

    Taglines: string
        one sentence to introduce the movie(e.g. 'An offer you can't refuse.')

    '''
    def __init__(self,title,rating,year,gerne,boxoffice,taglines):
        self.title=title
        self.rating=rating
        self.year=year
        self.gerne=gerne
        self.boxoffice=boxoffice
        self.taglines=taglines
    
    def info(self):
        return self.title+" ("+f'{self.year}'+"):"+ self.gerne+" Rating: "

def build_chart_url_dict():
    ''' Build a dictionary of different charts and its url from 
        IMDb website: https://www.imdb.com/chart/top

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a chart name and value is the url of chart
        e.g.{"box_office":'https://www.imdb.com/chart/boxoffice'}
    
    '''
    chart_url=BASE_URL+'/chart/top'
    response=make_url_request_using_cache(chart_url,CACHE_DICT,params=None)
    soup = BeautifulSoup(response,"html.parser")
    charts = soup.find("div", class_="full-table")
    each_chart = charts.find_all("div", class_="table-cell primary")
    chart_dict={}

    for i in each_chart:
        chart_path = i.find("a").text
        chart_url=i.find("a")["href"]
        chart_dict[chart_url.strip().lower()]=BASE_URL+chart_url

    return chart_dict




def get_movie_instance(movie_url):
    ''' Make an instance from a movie URL.

    Parameters
    ----------
    movie_url:string
        The URL for a movie page in movie chart

    Returns
    -------
    instance
        a movie instance
    '''
    response = make_url_request_using_cache(movie_url,CACHE_DICT,params=None)
    soup=BeautifulSoup(response,'html.parser')

    title_wrapper=soup.find('div', class_='title_wrapper')
    title_year_info=title_wrapper.find('h1',class_='')
    title=(title.text)[:-7].strip()
    year=int(title.find('a').text)

    rating= float(soup.find('span',itemprop='ratingValue').text)

    storyline=soup.find('div',class_='article', id='titleStoryLine')
    tagline= (storyline.find_all('div', class_='txt-block'))[0].text
    taglines=tagline.splitlines()[-1]

    gerne_all=(storyline.find_all('div',class_='see-more inline canwrap'))[1].text
    gerne_word=gerne.split()[1:]
    gerne=''
    gerne=gerne.join(gerne_word)


    titledetail=soup.find('div', class_='article', id='titleDetails')
    all_detail_info=titledetail.find_all('div', class_='txt-block')
    for i in all_detail_info:
        word_list=i.text.split()
        if word_list[0]=='Cumulative':
            boxoffice=(i.text.split())[-1]
    boxoffice=boxoffice[1:]# check for string

    movie_object=Movie(title,rating,year,gerne,boxoffice,taglines)
    return movie_object

def get_movies_list_for_chart(chart_url):
    '''Make a list of movie instances from a chart URL.

    Parameters
    ----------
    chart_url:string
        The URL for chart page

    Returns
    -------
    list
        a list of movie instances
    '''



'''

url = "https://www.imdb.com/chart/top"
r = requests.get(url)
soup = BeautifulSoup(r.content,"html.parser")

tags = soup.find("div", class_="full-table")
# print(tags.text)
tags_each = tags.find_all("div", class_="table-cell primary")
#print(tags_each)

for tag in tags_each:
    path_prime1 = tag.find("a")
    print(path_prime1["href"])
    #path_list.append(path_prime1["href"])

'''

