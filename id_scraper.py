from bs4 import BeautifulSoup
import requests

'''
source = requests.get('https://tenor.com/users/isail').text
'''

def get_ids():
    with open("page.html", "r") as f:
        source = f.read() 

    soup = BeautifulSoup(source, 'html.parser')

    ids = []
    number_of_gifs = 0
    for gif in soup.find_all('figure', class_='GifListItem'):
        id = str(gif.a['href']).split('gif-')[1]
        ids.append(id)

        number_of_gifs += 1

    with open("ids.txt", 'a+') as f:
        for id in ids:
            f.write(id + ", ")

    print(ids)    
    print("NUMBER OF GIFS SCRAPED:", number_of_gifs)
