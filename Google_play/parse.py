import requests
from bs4 import BeautifulSoup

terms = ['gay', 'LGBT', 'bisexual', 'homosexual']

for search_term in terms:
    page = requests.get('https://theappstore.org/search.php?search=' + search_term + '&platform=software')
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    # Save search results.
    # page = requests.get('https://fnd.io/#/nz/search?mediaType=iphone&term='+ search_term)
    # print(page.text)
    # soup = BeautifulSoup(page.content, 'html.parser')
    
    with open('./Source/' + search_term + '.html', 'w') as f:
        f.write(soup.prettify())

# title = soup.title.text # gets you the text of the <title>(...)</title>

# # print(page.text)
# # print(page.status_code)
# # Extract title of page
# page_title = soup.title

# # Extract body of page
# page_body = soup.body

# # Extract head of page
# page_head = soup.head

# # print the result
# print(page_title, page_head)

# # Create all_h1_tags as empty list
# # all_h1_tags = []

# # Set all_h1_tags to all h1 tags of the soup
# # for element in soup.select(''):
# #     all_h1_tags.append(element.text)

# # Create seventh_p_text and set it to 7th p element text of the page
# # seventh_p_text = soup.select('p')[6].text

# # print(all_h1_tags, seventh_p_text)
# print(soup.prettify())
# with open(search_term + '.txt', 'w') as f:
#     f.write(soup.prettify())
