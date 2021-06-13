import os
import requests

os.getcwd()
os.chdir('./Source')
os.listdir('.')

from bs4 import BeautifulSoup

terms = ['gay',
         'gay-dating',
         'homosexual',
         'men who have sex with men',
         'man who have sex with man',
         'MSM',
         'social media dating app',
         'socialmedia dating app',
         'gay social media dating app',
         'gay socialmedia dating app']

for search_term in terms:
    print('Saving results for query with term: ' +  search_term + ' from theappstore.org')
    page = requests.get('https://theappstore.org/search.php?search=' + search_term + '&platform=software')
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    # Save search results.
    with open(search_term + '_theaappstore.html', 'w') as f:
        f.write(soup.prettify())
