from flask import Flask,render_template,request,abort
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
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

if __name__ == "__main__":
    app.run(debug=True)
