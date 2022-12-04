from bs4 import BeautifulSoup
import requests
from flask import Flask
from flask import request
from flask_cors import CORS


app=Flask(__name__)
CORS(app, origins=["*"])



word="p"


################################################33

def start(n,sc,ec):

    name=search(n)
    global word
    word=name


    b=int(sc)
    e=int(ec)

    go=e-b
    print(word)
    last=''

    for i in range(go+1):
      ch= chapter(str(b))
      last=last+ch
      print(b)
      b=b+1

    return last


###################################################3
def search(na):

    print('processing...')

    
    names=na.replace(" ","+")
    url='https://vipnovel.com/?s='+names+'&post_type=wp-manga'

    html_text=requests.get(url).text

    soup=BeautifulSoup(html_text,'lxml')

    novel=soup.find('div', class_ ='row c-tabs-item__content')
    n=novel.find('div',class_='post-title')
    t=n.find('h3').text

    return t


###############################################################33

def chapter(next):

   

    names1=word.replace(" ","-")
    url1='https://vipnovel.com/vipnovel/'+ names1 +'/chapter-'+next+'/'
    print(url1+ "    l")

    html_text1=requests.get(url1).text

    soup1=BeautifulSoup(html_text1,'lxml')

    novel1=soup1.find('div', class_ ='text-left')


    print(url1)


   

    print('saved')

    return novel1.text


################################################################3

def search2(na):
    
    print('processing...')

    
    names=na.replace(" ","-")
    print(names)

    url='https://mixednovel.net/novel/'+names+'/'

    html_text=requests.get(url).text

    print(url)

    soup=BeautifulSoup(html_text,'lxml')

    print('pass2')

    novel=soup.find('div', class_ ='post-title').text
    print('pass3')



   

   

    print(novel)

    return novel


####################################################################




def chapter2(next):

   

    names1=word.replace(" ","-")
    url1='https://mixednovel.net/novel/'+ names1 +'/chapter-'+next+'/'
    print(url1+ "    l")

    html_text1=requests.get(url1).text

    soup1=BeautifulSoup(html_text1,'lxml')

    novel1=soup1.find('div', class_ ='text-left')


    print(url1)


   

    print('saved')

    return novel1.text

###############################################################




def start2(n,sc,ec):

    name=search2(n)
    global word
    word=name


    b=int(sc)
    e=int(ec)

    go=e-b
    print(word)
    last=''

    for i in range(go+1):
      ch= chapter2(str(b))
      last=last+ch
      print(b)
      b=b+1

    return last




#################################################################

@app.route("/server1")
def home():

    name=request.args.get("name")
    chapb=request.args.get("chapter")
    chape=request.args.get("lastchapter")

    last=start(name,chapb,chape)

   

    return last

#####################################################################


@app.route("/server2")
def home2():

    name=request.args.get("name")
    chapb=request.args.get("chapter")
    chape=request.args.get("lastchapter")

    last=start2(name,chapb,chape)

   

    return last


###################################################


@app.route("/")
def home3():
    return "heoo"






if __name__ == '__main__':

    app.run(debug=True,port=3000)















