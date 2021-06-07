from mediawiki import MediaWiki
import sys
import json
import os
import argparse
import requests
#from prettytable import PrettyTable
pwnwiki = MediaWiki(user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64')
pwnwiki = MediaWiki(url='https://www.pwnwiki.org/api.php')


parser = argparse.ArgumentParser(usage='%(prog)s [options]')
parser.add_argument("-v", "--version", help="Output program version", action="store_true")
parser.add_argument("-s", "--search", help="Search from PwnWiki",action='append',nargs = '*')
parser.add_argument("-l", "--language", help="Specify language search",action='append',nargs = '*')
parser.add_argument("-n", "--number", help="Number of pages",action='append',nargs = '*')

args = parser.parse_args()

if args.version:
    print("\033[1;34m[Version]\033[0m PwnDatas-DB-Project(PDDP) & vulsearch Jun.6 2021") #Blue

if args.number:
    number = args.number[0]
    number = ','.join(str(i) for i in number)
    #print(number)

if args.search:
    keyword = args.search[0]
    keyword = ','.join(str(i) for i in keyword)
    try:
        number = number
    except NameError:
        number = 20
    print("\033[1;34m[INFO]\033[0m According to your settings, the program outputs %s pieces of content." %(number))
    number = int(number)
    web_data = pwnwiki.opensearch(keyword, results=number)
    s = json.dumps(web_data)
    s1 = json.loads(s)
    #print(s1) #Success
    try:
        for i in range(0,20):
            display = ("https://www.pwnwiki.org/api.php?action=parse&page=%s&contentmodel=wikitext&format=json" %(s1[i][0]))
                #print("\033[32m[+]Vulnerability\033[0m" ,s1[i][0])  #標題
            response = requests.get(display)
            #print(response)
            content = response.text
            json_dict = json.loads(content)
                #print(json_dict)
            print("\033[32m[+]Vulnerability\033[0m" ,json_dict['parse']['displaytitle'])
                #print(json_dict['parse']['displaytitle'])
            print("\033[33m[+]URL\033[0m" ,s1[i][2])  #網址

            #print(display)
            #print(display_json)
            print('------------------------------------------------------------------------------------------------------')
    except:
        pass
