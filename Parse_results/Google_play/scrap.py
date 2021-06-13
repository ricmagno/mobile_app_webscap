import glob, os, sys
import string
import pandas as pd

debug = 0

found_counter = 0

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
    

find_line = "pull-left"
start_string = "<a href="
end_string = " class="

data = pd.read_csv('./Source/data.csv', header=0)
terms = pd.DataFrame(data, columns=['Apps'])

terms['url'] = ""
terms['search_string']=""

print('Looking for :', terms["Apps"].count(), ' apps.')

os.getcwd()
os.chdir('./Source')
os.remove("consolidated.html")
files = glob.glob("*.html")
if debug: print('HTML files: ', files)

file = 'consolidated.html'
with open(file, 'w') as outfile:
    for fname in files:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

ext = open(file, "r").readlines()

debug = 1 
for index, term in terms["Apps"].items():
    if debug: print(term)
    for s in ext:
        if find_line in s:
            found_it = remove((s[s.find(start_string)+len(start_string):s.rfind(end_string)]))
            if debug: print(found_it)
            if debug: print(term_to_link(term).lower())
            if term_to_link(term[:39]).lower() in found_it:
                if debug: print (term_to_link(term).lower())
                terms.at[index, 'search_string'] = term_to_link(term[:39]).lower()
                print(term, " ", found_it)
                terms.at[index, 'url'] = found_it
                found_counter +=1
                break

print("URLs found: ", found_counter)
print(terms[100:140])

terms.to_csv('ios.csv')


# if terms['search_string'].empty:
    # print(terms[['Apps','search_string', 'url']])

