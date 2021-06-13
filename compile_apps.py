import glob, os, sys
import string, re
import pandas as pd

from bs4 import BeautifulSoup


debug = False

found_counter = 0


def clean_string(string):
    bad_chars = [' ', ',', ';', ':', '!', '*', '(', ')']
    for i in bad_chars :
        good_string = string.replace(i, "")
    good_string = re.sub(' +', ' ', string)
    return good_string

def remove(string):
    string = string.replace('"', '')
    return string.translate(' \n\t\r')

def term_to_link(string):
    emdash = '\u2014'
    string = string.replace("(",'')
    string = string.replace(")",'')
    string = string.replace("&",'')
    string = string.replace("#",'')
    string = string.replace("'",'')
    string = string.replace("’",'')    
    string = string.replace(",",'')
    string = string.replace(":",'')
    string = string.replace(".",'')
    string = string.replace("+",'')
    string = string.replace("!",'')
    string = string.replace(">",'')
    string = string.replace("|",'')
    string = string.replace(' ' + emdash + ' ', '-')
    string = string.replace(' – ', '-')
    string = string.replace("- ",' ')
    string = string.replace(" -",' ')
    string = string.replace('–', '-')
    string = string.replace(emdash, '')                                                                                                                                      
    string = string.replace(" - ",'-')
    string = string.replace("  ",'-')
    string = string.replace("--",'-')
    string = string.replace(" ",'-')
    return string
    
find_line_app = "ember1403"
start_string_app ="<span title="
end_string_app =">"

find_line_version= "What's New in Version "
start_string_version = "What's New in Version "
end_string_version = "<script"

find_line_ratings="star-rating-ratings text-muted"
start_string_ratings=">"
end_string_ratings="</span>"


find_line_description = 'Description' #'<div class="preformatted-text">' #'Description' #'<div class="preformatted-text">
start_string_description = '-start type=text/x-placeholder></script>'
end_string_description = '<script id='


data = pd.read_csv('./Source/data.csv', header=0)
terms = pd.DataFrame(data, columns=['apps', 'url'])
print(terms['apps'].count())

# index=np.arange(1)


apps = pd.DataFrame(data, columns=['name', 'version', 'ratings', 'description'])
# apps.set_index('name')

os.getcwd()
os.chdir('./Source/Apps/')
files = glob.glob("*.html")




description_start=0
description_end=0
print(len(files))
# exit()


if debug: print('HTML files: ', files, len(files), 'Looking for :', terms["apps"].count(), ' apps.')


for file in files:
    debug = 0
    ext = open(file, "r").readlines()

    ratings = 0
    start_flag = False
    end_flag = False
    line_count = 1
    description = ""
    
    for s in ext:
        
# Find App name
        if find_line_app in s:
            found_it = remove((s[s.find(start_string_app)+len(start_string_app):s.rfind(end_string_app)]))
            found_it = remove((found_it[found_it.find(">")+len(">"):found_it.rfind("</span")]))
            if debug: print(found_it)
            app_name = found_it
            print(app_name)

# Find App version
        if find_line_version in s:
            found_it = remove((s[s.find(start_string_version)+len(start_string_version):s.rfind(end_string_version)]))
            if debug: print(found_it)
            version = found_it

# Find App ratings        
        if find_line_ratings in s:
            found_it = ext[line_count]
            found_it = remove((found_it[found_it.find("(")+len("("):found_it.rfind(")")]))
            if debug: print(found_it, 'at line', line_count, ext[line_count])
            ratings = int(found_it.replace(',',''))

# Find App Description
        if find_line_description in s:
            start_flag = True
            if debug: print('Description started at line ',line_count+2)
            description_start = line_count

        if "</script></div>" in s:
            start_flag = False
            if debug: print('Description ended at line ',line_count)
            description_end = line_count
            
        line_count += 1
        
    description = ext[description_start:description_end]

    description_string = ""
    for i in description:
        description_string += i
    description_string = description_string[172:]
    # description_string = remove((description_string[description_string.find(start_string_description)+len(start_string_description):description_string.rfind(end_string_description)]))
    
    
        
    print('\n\nSummary \n', '\nApp Name:', app_name, '\nVersion: ', version, '\nRatings', ratings, '\nDescription', description)
    data = [[str(app_name), str(version), ratings, str(description_string)]]
    results = pd.DataFrame(data, columns=['name', 'version', 'ratings', 'description'])

    apps = apps.append(results, ignore_index=True)

apps = apps.dropna()
apps = apps.reset_index(drop=True)
apps.to_csv('~/Desktop/ios_results.csv')
print(apps.head())
