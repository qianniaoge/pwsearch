# PwnDatas-DB-Project
PwnDatas-DB-Project(PDDP)

安裝依賴：
```
pip3 install pymediawiki
pip3 install requests
```

使用：
```
cd /opt
git https://github.com/JustYoomoon/PwnDatas-DB-Project.git
cd

.bashrc加入
alias vulsearch="python3 /opt/PwnDatas-DB-Project/vulsearch.py"

source .bashrc
```

```
vulsearch <option>

舉例：
vulsearch -s CVE-2019-0708

查看版本：
vulsearch -v

指定語言查詢(開發中)：
vulsearch -s <Vul Name> -l <Language Code>

指定行數輸出（舉例爲30）：
vulsearch -n 30 -s <Vul Name>
```

截圖：
![](https://github.com/JustYoomoon/PwnDatas-DB-Project/blob/main/3156.png)
![](https://github.com/JustYoomoon/PwnDatas-DB-Project/blob/main/3164.png)

社區：
https://forums.pwnwiki.org/t/23


PwnWiki:
https://www.pwnwiki.org


中文Telegram群組:

https://t.me/pwnwiki_zh
