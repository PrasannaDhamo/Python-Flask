from flask import Flask, request, render_template, url_for, redirect
from pymongo import MongoClient
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient("mongodb://prasanna1411:mathan100@prasanna-mongodb-shard-00-00.wfmy0.gcp.mongodb.net:27017,prasanna-mongodb-shard-00-01.wfmy0.gcp.mongodb.net:27017,prasanna-mongodb-shard-00-02.wfmy0.gcp.mongodb.net:27017/user-db?ssl=true&replicaSet=atlas-1g0i65-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.get_database('user-db')
cl = db.get_collection('user-details')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    return render_template('registration.html')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        uname = request.form['name']
        doc = {"username" : uname,"password" : request.form['password'],"email" : request.form['email']}
        cl.insert_one(doc)
        return redirect(url_for('movie', name = uname))


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/lg', methods=['GET', 'POST'])
def lg():
    if request.method == 'POST': 

        validate = cl.find_one({"username": request.form['name'], "password": request.form['password']})
    
        if validate == None:
            return redirect(url_for('invalid'))
        else:
            return redirect(url_for('movie', name = request.form['name']))


@app.route('/success/<name>')
def success(name):
    return "Welcome %s....!" %name

@app.route('/invalid')
def invalid():
    return "Invalid Username/Password....!"

@app.route('/', methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':
        return redirect(url_for('movie_details', name = request.form['name']))
    return render_template('movie.html')

@app.route('/movie-details', methods=['GET', 'POST'])
def movie_details():
    if request.method == 'POST': 
        return redirect(url_for('details', name = request.form['name']))

@app.route('/details/<name>', methods=['GET', 'POST'])
def details(name):
    api_key_1 = 'k_T9X2nfj1'
    api_key_2 = 'k_ehGQ0TV0'
    api_key_3 = 'k_hR58y7Qi'
    id_url = 'https://imdb-api.com/en/API/SearchMovie/'
    movie_url = 'https://imdb-api.com/en/API/Title/'
    title = str(name)
    url = id_url + api_key_1 + '/' + title
    try:
        title_response = requests.get(url)
        title_jsonResponse = title_response.json()
        id_no = (title_jsonResponse['results'][0]['id'])
        details_url = movie_url + api_key_2 + '/' + id_no
        movie_response = requests.get(details_url)
        movie_jsonResponse = movie_response.json()
    except:
        return abort(404)

    title_name = (movie_jsonResponse['title'])
    movie_runtime = (movie_jsonResponse['runtimeStr'])
    Release_Date = (movie_jsonResponse['releaseDate'])
    movie_image = (movie_jsonResponse['image'])
    movie_plot = (movie_jsonResponse['plot'])
    movie_awards = (movie_jsonResponse['awards'])
    director_name = (movie_jsonResponse['directors'])
    writer_name = (movie_jsonResponse['writers'])
    star_name = (movie_jsonResponse['stars'])
    genre_list = (movie_jsonResponse['genres'])
    movie_company = (movie_jsonResponse['companies'])
    imdb_rating = (movie_jsonResponse['imDbRating'])
    #movie_budget = (title_jsonResponse['boxOffice'][0]['budget'])
    #movie_worldgross = (title_jsonResponse['boxOffice'][0]['cumulativeWorldwideGross'])
    
    return render_template("movie_details.html", tname = title_name, dname = director_name, mimg = movie_image, plot = movie_plot, rdate = Release_Date, rtime = movie_runtime, glist = genre_list, cname = star_name, wname = writer_name, mov_company = movie_company, imdb_r = imdb_rating)


@app.route('/covid',methods=['POST','GET'])
def covid():
    world_url= str("https://www.worldometers.info/coronavirus")
    india_url = str("https://www.worldometers.info/coronavirus/country/india/")

    soup = BeautifulSoup(requests.get(world_url).text, "html.parser")
    soup1 = BeautifulSoup(requests.get(india_url).text, "html.parser")

    value = soup.findAll("div", {"class": "maincounter-number"})
    value += soup.findAll("div", {"class": "number-table-main"})

    value1 = soup1.findAll("div", {"class": "maincounter-number"})
    value1 += soup1.findAll("div", {"class": "number-table-main"})

    values = list()
    values1 = list()

    for x in value:
        values.append(x.text.strip())

    tot_cases = str(values[0])
    tot_deaths = str(values[1])
    tot_recovered = str(values[2])
    active_cases = str(values[3])
    closed_cases = str(values[4])

    for x in value1:
        values1.append(x.text.strip())

    tot_cases1 = str(values1[0])
    tot_deaths1 = str(values1[1])
    tot_recovered1 = str(values1[2])
    active_cases1 = str(values1[3])
    
    return render_template('covid.html',tot_cases=tot_cases, tot_deaths=tot_deaths, tot_recovered=tot_recovered, active_cases= active_cases, closed_cases=closed_cases, tot_cases1=tot_cases1, tot_deaths1=tot_deaths1, tot_recovered1=tot_recovered1, active_cases1= active_cases1)

@app.route('/horoscope', methods=['GET', 'POST'])
def horoscope():
    if request.method == "POST":
        zodiac_sign = request.form["sign"]
        print(zodiac_sign)
        day = request.form["day"]
        if day == "today":
            day = "daily-" + day
        if day == "tomorrow":
            day = "daily-" + day
        if day == "yesterday":
            day = "daily-" + day

        url = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-{day}.aspx?sign={zodiac_sign}"
        )
        print(url)
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        data = (soup.find("div", class_="main-horoscope").p.text)
        return render_template('horoscope.html', data = data)
    else:
        return render_template('horoscope.html')

if __name__ == "__main__":
    app.run(debug=True)
