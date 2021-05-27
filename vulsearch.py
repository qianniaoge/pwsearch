from mediawiki import MediaWiki
import sys
import json

pwnwiki = MediaWiki(user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64')
pwnwiki = MediaWiki(url='https://www.pwnwiki.org/api.php')

#get info
try:
    keyword = sys.argv[1]
except:
    print('+---------------------------------------------------------------------------------------------------------+')
    print('+ DES: by PwnWiki as https://www.pwnwiki.prg                                                              +')
    print('+      Free, editable vulnerability library for everyone                                                  +')
    print('+---------------------------------------------------------------------------------------------------------+')
    print('+ USE: vulsearch <NAME>                                                                                   +')
    print('+ vulsearch -update / vulsearch -language en <NAME>  /  vulsearch -local <NAME> / vulsearch -v            +')
    print('+ VER: PwnDatas-DB-Project(PDDP) & vulsearch May.27 2021                                                  +')
    print('+---------------------------------------------------------------------------------------------------------+')
    sys.exit(0)

web_data = pwnwiki.opensearch(keyword, results=20)  #最多輸出20個結果

#print(web_data)
s = json.dumps(web_data)
#print(s)
s1 = json.loads(s)
#print(s1)

try:
    for i in range(0,20) :
        print("\033[32m[+]Vulnerability\033[0m" ,s1[i][0])  #標題
        print("\033[33m[+]URL\033[0m" ,s1[i][2])  #網址
        print("---------------------------------------------------------------------------------------------------------------")
except:
    pass
