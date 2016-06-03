######################################
#  Name:     Ryan Hillhouse          #
#  Date:     03.06.2016              #
#                                    #
#  Description:                      #
#  Reads out data from duden.de.     #
#  Enter a word and it will return   #
#  a table containing the different  #
#  cases for both the plural- and    #
#  the singular form.                #
######################################

#Imports
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests
import re

#Array counter to display data in the CLI.
arr_index = 0

#Read arguments from CLI and assign to var
parser = ArgumentParser()
parser.add_argument("-w", "--word", dest="input_word", help="The word, or words, to get the article for.")
args = parser.parse_args()
input_word = args.input_word

#Replace German special chars with the international variant.
#List of char_to_replace:replace_with
rep = {"ö": "oe", "ü": "ue"}
rep = dict((re.escape(k), v) for k, v in rep.items())
pattern = re.compile("|".join(rep.keys()))
safe_word = pattern.sub(lambda m: rep[re.escape(m.group(0))], input_word)

#Final manipulation to word -> ready to post to server.
safe_word = safe_word.title()

#Post the word to the server and fetch the html content.
req = requests.get('http://www.duden.de/rechtschreibung/'+safe_word)
html = req.content

#Parse HTML and fetch the table containing the different cases.
soup = BeautifulSoup(html,"html.parser")
table_rows = soup.table.find_all('tr')

#Create a multidimensional array.
#One blank array containing 3 other blank ones.
singular = []
singular.append([])
singular.append([])
singular.append([])

#Add the content from the HTML table to the multidimensional array.
for row in table_rows:
    singular[0].append((row.contents[0]).contents[0])
    singular[1].append((row.contents[1]).contents[0])
    singular[2].append((row.contents[2]).contents[0])

#The length here is needed to dynamically adjust the alignment and spacing.
#This allows for a better depiction of the table in the CLI.
span_sizes = [len(max(singular[1:])),len(max(singular[1])),len(max(singular[2]))]

#Output the table by iterating through the array uding the cases are marker values.
#Some hardcoded extra spacing has been added to help with the daynamic spacing.
for case in singular[0][0:]:
    print(case.ljust(span_sizes[0]+10,' ') + (singular[1][arr_index]).ljust(span_sizes[1]+5,' ') + (singular[2][arr_index]).ljust(span_sizes[2]+5,' '))
    arr_index += 1
