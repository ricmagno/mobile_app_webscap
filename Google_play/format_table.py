import xlrd
import requests
import pandas as pd
from bs4 import BeautifulSoup


def remove(string):
    string = string.replace('"', '')
    string = string.replace(',', '')
    return string.translate(' \n\t\r')

def save(apps):
    apps = apps.dropna()
    apps = apps.reset_index(drop=True)
    apps.to_csv('~/Desktop/android_results.csv')


start_string_app = "<span>"
end_string_app = "</span>"

start_string_category = 'itemprop="genre">'
end_string_category = '</a>'

start_string_version = '<span class="htlgb">'
end_string_version = "</span>"

start_string_ratings = 'AYi5wd TBRnV><span aria-label='
end_string_ratings = ' ratings'

start_string_description = '<div jsname="sngebd">'
end_string_description = "</div>"

apps = pd.DataFrame(columns=['name', 'category', 'version', 'ratings', 'description'])
ratings = '' #Google Play does not provide ratings

mainData_book = xlrd.open_workbook("data.xls", formatting_info=True)
mainData_sheet = mainData_book.sheet_by_index(0)
for row in range(1, 1000):
    rowValues = mainData_sheet.row_values(row, start_colx=0, end_colx=8)
    company_name = rowValues[0]

    link = mainData_sheet.hyperlink_map.get((row, 0))
    url = '(No URL)' if link is None else link.url_or_path
    print(company_name.ljust(20) + ': ' + url)
    if len(url) < 10:
        print('\nDone!')
        exit()

    print('\n\n Searching app', row, '(', int((row*100)/571), ')\n\n')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    found_it = str(soup.find_all("h1", {"class": "AHFaub"}))
    app_name = remove((found_it[found_it.find(start_string_app)+len(start_string_app):found_it.rfind(end_string_app)]))
    print("\n\nApp name: ", app_name)

    try:
        found_it = str(soup.find_all("a", {"class": "hrTbp R8zArc"})[1])
    except:
        found_it = str(soup.find_all("a", {"class": "hrTbp R8zArc"}))    
    category = remove((found_it[found_it.find(start_string_category)+len(start_string_category):found_it.rfind(end_string_category)]))
    print("\n\nCategory: ", category)

    try:
        found_it = str(soup.find_all("span", {"class": "htlgb"})[7])
        version = remove((found_it[found_it.find(start_string_version)+len(start_string_version):found_it.rfind(end_string_version)]))
    except:
        version = 0

    print("\n\nVersion: ", version)

    found_it = str(soup.find_all("span", {"class": "AYi5wd TBRnV"}))
    print(found_it)
    ratings = remove((found_it[found_it.find(start_string_ratings)+len(start_string_ratings):found_it.rfind(end_string_ratings)]))[16:]
    print("\n\nRatings: ", ratings)

    found_it = str(soup.find_all("div", {"jsname": "sngebd"}))
    description = remove((found_it[found_it.find(start_string_description)+len(start_string_description):found_it.rfind(end_string_description)]))
    print("\n\nDescription: ", description)

    print('\n\nSummary \n', '\nApp Name:', app_name, '\nCategory', category,'\nVersion: ', version, '\nRatings', ratings, '\nDescription', description)

    data = [[str(app_name), str(category), str(version), ratings, str(description)]]
    results = pd.DataFrame(data, columns=['name', 'category', 'version', 'ratings', 'description'])

    print(results)
    apps = apps.append(results, ignore_index=True)
    print(apps.tail())
    save(apps)

    # with open('./Source/' + search_term + '.html', 'w') as f:
        # f.write(soup.prettify())
