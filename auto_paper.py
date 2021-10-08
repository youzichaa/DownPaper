import os
import urllib.request
import requests
from bs4 import BeautifulSoup

# Link
url = "https://dblp.uni-trier.de/db/conf/ccs/ccs2020.html"
# FLAG
OPEN_KEYWORD_SEARCH = True
# Keyword
Key_word = ['Secure', 'Privacy']
file_name = url.split("/")[-1].split(".")[0]
file_type = url.split("/")[-3]
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
# Journal
soup2 = soup.find_all('li', {"class": "entry article"})
if file_type == "conf":
    soup2 = soup.find_all('li', {"class": "entry inproceedings"})


fp = open('paperlink.txt', 'w')
for i in soup2:
    s = i.find('a')['href']+'\n'
    sci_link = 'https://sci-hub.ren/' + s
    # print(sci_link)
    fp.write(sci_link)
fp.close()

soup3 = soup.find_all('span', {"class": "title"})
fpname = open('papername.txt', 'w', encoding="utf-8")
for i in soup3:
    s = i.string
    # print(s)
    s = i.text + '\n'
    fpname.write(s)
fpname.close()


# Put title into list
fpname = open('papername.txt').readlines()
namelist = []
downloadlist = []
select_num = 0
for i in fpname:
    i = i[:-1]
    s = i.replace(':', '').replace('?', '').replace('</> ', '')
    namelist.append(s)
    # Search
    if OPEN_KEYWORD_SEARCH:
        for Keyword in Key_word:
            if Keyword in s:
                downloadlist.append(select_num)
                break
    else:
        downloadlist.append(select_num)
    select_num += 1

faillist = []

path = 'D:\\file\\paper\\' + file_name + '\\'
folder = os.path.exists(path)
if not folder:
    os.makedirs(path)
# Paperlink search
lines = open('paperlink.txt').readlines()  # line
f = open('paperlink.txt')
count = 0
select_num = 0
for line in f:
    if count == downloadlist[select_num]:
        line = line[:-1]

        out_fname = path + namelist[count] + '.pdf'  # filename
        # out_fname = 'paper/' + namelist[count] + '.pdf'  # filename
        if not os.path.exists(out_fname):
            res = requests.get(line)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            # news = soup.select('iframe')
            # pdf = news[0]['src']
            news = soup.select('#pdf')
            if news.__len__() == 0:
                faillist.append(select_num)
                print("failed ...", namelist[count])
            else:
                pdf = news[0]['src']
                print("downloading ...", namelist[count])
                check_http = pdf[0:6]
                if check_http != "https:":
                    pdf = "https:" + pdf
                r = requests.get(pdf)
                with open(out_fname, 'wb') as f2:
                    f2.write(r.content)
        else:
            print("existed ...", namelist[count])
        select_num += 1
        # print(select_num)
        if select_num >= len(downloadlist):
            break
    count += 1
f.close()

for iterfile in faillist:
    print(namelist[iterfile])
print("total:", downloadlist.__len__(), "fail:", faillist.__len__())