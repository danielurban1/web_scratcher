import bs4 as bs
import lxml
import urllib.request
import csv

html = urllib.request.urlopen("http://www.imdb.com/chart/top?ref=ft_250").read()
soup = bs.BeautifulSoup(html, "lxml")

id_list = []
number =0
for paragraph in soup.find_all('a'):
    if paragraph.get('href') and "title/tt0" in str(paragraph) and str(paragraph)[16:25] not in id_list:
        id_list.append(str(paragraph)[16:25])
        number +=1
        if number == 100:
            break
list_of_movies =[]
for id_number in id_list:
    adres = "http://www.omdbapi.com/?i="+id_number
    html2 = urllib.request.urlopen(adres).read()
    soup2 = bs.BeautifulSoup(html2, "lxml")
    list_of_movies.append(str(soup2.find_all("p")))
    
year_title = []    
for movie in list_of_movies:
    first = '"Title":"'
    last = '","Year":'
    start = movie.index( first ) + len( first )
    end = movie.index( last, start )
    title = movie[start:end]
    first = '"Year":"'
    last = '","Rated"'
    start = movie.index( first ) + len( first )
    end = movie.index( last, start )
    year = movie[start:end]
    movie = [title, year]
    year_title.append(movie)
year_title = sorted(year_title,  key = lambda x: int(x[1]))
year_title.insert(0, ["title", "year"])


with open ('%s.csv' % "movies", 'w', newline='') as file:
    a = csv.writer(file, delimiter=',')
    a.writerows(year_title)
print("Done!")