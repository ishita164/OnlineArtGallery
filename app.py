from flask import Flask, json, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth

import sqlite3
import requests
import json
from flask import Flask, request, jsonify
from sample import token_generate, get_code

#Imported for implementing  crawler
from bs4 import BeautifulSoup
from beaut_soup import getCompetitions











app = Flask(__name__)

oauth = OAuth(app)

app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
app.config['GOOGLE_CLIENT_ID'] = "1089032102274-3ibqjeagn18l9rv47vnhidj8qelqllh8.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"
app.config['GITHUB_CLIENT_ID'] = "82e100468a396d48bb1a"
app.config['GITHUB_CLIENT_SECRET'] = "6a301d38a20837ebe262424fe194945922c01820"

google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)


github = oauth.register (
  name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)



# Default route
@app.route('/')
def index():
    return render_template('index.html') 


# Google login route
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    print(f"\n{resp}\n")
    return render_template('home.html')


# Github login route
@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


# Github authorize route
@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    print(f"\n{resp}\n")
    return "You are successfully signed in using github"


#Home
@app.route('/login/google/Home1')
def web_home():
    
    return render_template('home.html') 

#index1
@app.route('/login/google/collections')
def get_artsapi():

    # get_code()
    # print("get_code done!!")
    
    

    artsapi = []
    try:
        conn = database_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM artsapi")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            item = {}
            item["art_id"] = i["art_id"]
            item["artname"] = i["artname"]
            item["artistname"] = i["artistname"]
            item["desc"] = i["desc"]
            item["link"] = i["link"]
            artsapi.append(item)

    except:
        artsapi = []

    coll_data = artsapi
    return render_template('index1.html', data=coll_data[:])

#1
@app.route('/login/google/artists')
def web_1():
     # create a header containing our token 
    headers = {"X-Xapp-Token" : token_generate()}

    r = requests.get("https://api.artsy.net/api/artists/4d8b92b34eb68a1b2c0003f4", headers=headers)

    # parse the server response 
    j = json.loads(r.text)
    print("J is printed: ", j)

    slug = j['slug']
    print("my slug: ", slug)

    ap = slug
    slugurl = f'https://www.wikiart.org/en/App/Painting/PaintingsByArtist?artistUrl={ap}&json=2'

    r2 = requests.get(slugurl).json()
    
    print(r2)

    print(r2[0]['image'])
    return render_template('1.html', data=j, imgandy = r2[0]['image'][:-10])

#about
@app.route('/login/google/about')
def web_about():
    return render_template('about.html')

#addArt
# @app.route('/login/google/addart', methods = ["POST", "GET"])
# def web_addart():
#     artinfo = request.get_json()
#     return render_template('addArt.html', data = artinfo)


def database_conn():
    connect = sqlite3.connect('database.db')
    return connect


def table_creation():
    try:
        connect = database_conn()
        cursor = connect.cursor()
        cursor.execute('''
         CREATE TABLE artsapi(
                art_id INTEGER PRIMARY KEY NOT NULL,
                artname TEXT NOT NULL,
                artistname TEXT NOT NULL,
                desc TEXT NOT NULL,
                link TEXT NOT NULL
            );
        ''')

        connect.commit()
        print("Art table created successfully!")
    except:
        print("Art table creation failed.")
    finally:
        connect.close()

def insert_art(item):
    try:
        conn = database_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO artsapi (artname, artistname, desc, link) VALUES (?, ?, ?, ?)", (item['artname'], item['artistname'], item['desc'], item['link']))
        conn.commit()
        inserted_art = get_by_id(cur.lastrowid)
    except:
        conn().rollback()
    finally:
        conn.close()
    return inserted_art

@app.route('/login/google/about/get')
def get_artsapi1():
    artsapi = []
    try:
        conn = database_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM artsapi")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            item = {}
            item["art_id"] = i["art_id"]
            item["artname"] = i["artname"]
            item["artistname"] = i["artistname"]
            item["desc"] = i["desc"]
            item["link"] = i["link"]
            artsapi.append(item)

    except:
        artsapi = []

    return render_template('get1.html', m1=artsapi)

def get_by_id(art_id):
    item = {}
    try:
        conn = database_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM artsapi WHERE art_id = ?", (art_id,))
        row = cur.fetchone()
        # convert row object to dictionary
        item["art_id"] = row["art_id"]
        item["artname"] = row["artname"]
        item["artistname"] = row["artistname"]
        item["desc"] = row["desc"]
        item["link"] = row["link"]
    except:
        item = {}
    return item


def update_art(item):
    try:
        conn = database_conn()
        cur = conn.cursor()
        cur.execute("UPDATE artsapi SET artname = ?, artistname = ?, desc = ?, link = ? WHERE art_id =?", (item['artname'], item['artistname'], item['desc'], item['link'], item["art_id"],))
        conn.commit()
        # return the user
        updated_art = get_by_id(item["art_id"])
        print(updated_art)
    except:
        conn.rollback()
        updated_art = {}
    finally:
        conn.close()
    return updated_art


def delete_item(art_id):
    message = {}
    try:
        conn = database_conn()
        conn.execute("DELETE from artsapi WHERE art_id = ?", (art_id, ))
        conn.commit()
        message["status"] = "Art deleted successfully!"
    except:
        conn.rollback()
        message["status"] = "Cannot delete art."
    finally:
        conn.close()

    return message

artsapi = []
item0 = {
    "artname": "Sloths",
    "artistname": "Camila Venegas",
    "desc": "Sloths in a forest 3D illustration",
    "link": "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/af916e92251849.5e465679772bd.jpg",
}

item1 = {
    "artname": "An evening at the airport",
    "artistname": "Charlie Davis",
    "desc": "A warm delight of colours painting the evening, an illustration",
    "link": "https://mir-s3-cdn-cf.behance.net/project_modules/fs/e793f963077923.5aa5756c707c6.jpg",
}

item2 = {
    "artname": "Bear 3D art",
    "artistname": "Maxim",
    "desc": "Paper like Bear 3D art in pastel colours",
    "link": "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/eb362f75010615.5c4087a578489.png",
}

item3 = {
    "artname": "Mochi-The corgi",
    "artistname": "Lyn Chen",
    "desc": "Mochi - The playful corgi illustration art ",
    "link": "https://mir-s3-cdn-cf.behance.net/project_modules/fs/c41dca61109577.5a63c3f774738.jpg",
}

artsapi.append(item0)
artsapi.append(item1)
artsapi.append(item2)
artsapi.append(item3)

table_creation()

for row in artsapi:
    print(insert_art(row))


# @app.route('/artsapi', methods=['GET'])
# def get_all_artsapi():
#     return jsonify(get_artsapi())


# @app.route('/artsapi/<int:art_id>', methods=['GET'])
# def get_specific_item(art_id):
#     return jsonify(get_by_id(art_id))


# @app.route('/artsapi/add/<string:artname>/<string:artistname>/<string:desc>/<string:link>',
#            methods=['GET', 'POST'])
# def add_item(artname, artistname, desc, link):
#     item = {
#         "artname": artname,
#         "artistname": artistname,
#         "desc": desc,
#         "link": link
#     }
#     return jsonify(insert_art(item))



# @app.route('/artsapi/postart', methods=['POST'])
# def post_arts():
#     artinfo1 = request.get_json()
#     return jsonify(insert_art(artinfo1))

@app.route('/login/google/about/post', methods=['POST','GET'])
def web_post():
    add1={}
    request_method = request.method
    if request.method =='POST':
        a1=request.form['artname']
        a2=request.form['artistname']
        a3=request.form['desc']
        a4=request.form['link']
        add1 = {
            "artname": a1,
            "artistname": a2,
            "desc": a3,
            "link": a4
        }
        jsonify(insert_art(add1))
        return redirect(url_for('web_about'))
    else:
        return render_template('post1.html')

@app.route('/login/google/about/put', methods=['POST','GET'])
def web_put():
    add1={}
    request_method = request.method
    if request.method =='POST':
        a0 = request.form['art_id']
        a1=request.form['artname']
        a2=request.form['artistname']
        a3=request.form['desc']
        a4=request.form['link']
        add1 = {
            "art_id": a0,
            "artname": a1,
            "artistname": a2,
            "desc": a3,
            "link": a4
        }
        jsonify(update_art(add1))
        return redirect(url_for('web_about'))
    else:
        return render_template('put1.html')



@app.route('/artsapi/update/<int:itemid>/<string:artname>/<string:artistname>/<string:desc>/<string:link>',
           methods=['GET', 'POST'])
def update_an_item(itemid, artname, artistname, desc, link):
    item = {
        "art_id": itemid,
        "artname": artname,
        "artistname": artistname,
        "desc": desc,
        "link": link
    }
    return jsonify(update_art(item))


# @app.route('/artsapi/updateart',  methods = ['PUT'])
# def api_update_user():
#     obj = request.get_json()
#     return jsonify(update_art(obj))

@app.route('/login/google/about/delete', methods=['POST','GET'])
def web_delete():
    add2={}
    request_method = request.method
    if request.method =='POST':
        a0=request.form['art_id']

        jsonify(delete_item(a0))
        return redirect(url_for('web_about'))
    else:
        return render_template('delete1.html')

@app.route('/artsapi/delete/<int:art_id>', methods=['GET', 'DELETE'])
def delete_an_item(art_id):
    return jsonify(delete_item(art_id))


#webcrawler content
@app.route('/login/google/webcrlr')
def getCrawledData():

    results = getCompetitions('https://www.infodesigners.eu/illustration-competitions/1')
    print('-----------------------------------------------------We are printing data-------------------------------------')
    print(results)
    
    return render_template('webcrawler1.html', results=results)




if __name__ == '__main__':
  app.run(debug=True)
