from flask import *

from bs4 import BeautifulSoup as bs
import requests

app = Flask(__name__)

@app.route('/')
def index():
    name={
        "Developer":"Akash Mane",
        "Profession":"Software Engineer"
        }

    return jsonify(name), 201


@app.route('/Get_Album')
def my_route():
    page = request.args.get('page', default = 1, type = str)
    movie = requests.get(page)
    listpage=bs(movie.content)


    ami=listpage.find(id='main_page_middle')
    mi=ami.find('left')


    text=ami.find('left').get_text()
    Album=""
    Artists=""
    Starcast=""
    Composed=""
    Year=""
    Description=""

    for line in text.splitlines():
        if "Album" in line.strip():
            Album=line.strip()[7::].replace('\t','')
        if "Artists" in line.strip():
            Artists=line.strip()[8::].replace('\t','')
        if "Starcast" in line.strip():
            Starcast=line.strip()[9::].replace('\t','')
        if "Composed by" in line.strip():
            Composed=line.strip()[12::].replace('\t','')
        if "Year" in line.strip():
            Year=line.strip()[5::].replace('\t','')
        if "Description" in line.strip():
            Description=line.strip()[12::].replace('\t','')
        



    Songs=[]

    allsongs=listpage.find_all(class_="col-lg-6 col-md-6 col-sm-12 col-xs-12 main_page_category_music")
    for i in allsongs:
        link=i.find('a')['href']
        r = requests.get(link)
        soup=bs(r.content)
        allinfo=soup.find(id='main_page_middle')
        info=allinfo.find('left')
        dlinks=info.find(class_="downloaddiv").find_all('a')

        links=[]
        for one in dlinks:
            links.append(one['href'])

        text=allinfo.find('left').get_text()

        for line in text.splitlines():
            if "Song Name" in line.strip():
                Sname=line.strip()[11::]
            if "Singer(s)" in line.strip():
                Singer=line.strip()[11::]
            if "Lead Star(s)" in line.strip():
                Lstar=line.strip()[14::]
            if "Music Composer" in line.strip():
                Mcomposer=line.strip()[16::]
        
        song={
        "title":soup.find(class_="col-lg-12 col-md-12 col-sm-12 col-xs-12 main_page_category_div up").string,
        "poster":"https://pagalnew.com"+info.find('left').find('img')['data-src'][2::],
        "songurl":"https://pagalnew.com"+allinfo.find('source')['src'][2::],
        "Dlinks":links,
        "Des":info.find('p').string,
        "Song Name":Sname,
        "Singer(s)":Singer,
        "Lead Star(s)":Lstar,
        "Music Composer":Mcomposer,

        }
        Songs.append(song)
        
    Movie={
        "Title":listpage.find(class_='col-lg-12 col-md-12 col-sm-12 col-xs-12 main_page_category_div up').string.replace('Pagalnew',''),
        "poster":mi.find('img')['data-src'],
        "Description":Description,
        "Album":Album,
        "Artists":Artists,
        "Starcast":Starcast,
        "Composed by":Composed,
        "Year":Year,
        "Songs":Songs

    }

    
    return jsonify(Movie), 201


@app.route('/param/<name>')
def my_view_func(name):
    que=f"Parameters are send by '/param/<name>' is {name}"
    return que

if __name__ == '__main__':
    app.run(debug=True)