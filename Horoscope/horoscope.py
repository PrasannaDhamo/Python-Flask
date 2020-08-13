from flask import Flask, request, render_template, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

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
        return render_template('index.html', data = data)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
