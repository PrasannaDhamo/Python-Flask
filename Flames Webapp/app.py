from flask import Flask, request, render_template, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://prasanna1411:mathan100@prasanna-mongodb-shard-00-00.wfmy0.gcp.mongodb.net:27017,prasanna-mongodb-shard-00-01.wfmy0.gcp.mongodb.net:27017,prasanna-mongodb-shard-00-02.wfmy0.gcp.mongodb.net:27017/flames-db?ssl=true&replicaSet=atlas-1g0i65-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.get_database('flames-db')
cl = db.get_collection('flames-details')

@app.route('/')
def hello():
    return render_template('flames.html')

@app.route('/relation', methods=['POST', 'GET'])
def relation():
    if request.method == "POST":
        text1 = request.form['name1']
        text2 = request.form['name2']
        
        f = flame(text1,text2)

        doc = {"fname" : text1,"sname" : text2, "relation" : f}
        cl.insert_one(doc)

        if f == 'friends':
            out = text1+" and "+ text2
            out2 = "are "+f
        elif f == 'married':
            out = text1+" and "+text2
            out2 = "will get "+f
        elif f == 'siblings':
            out = text1+" and "+text2
            out2 = "are "+f
        elif f == 'affection':
            out = text1+" and "+text2
            out2 = "have "+f+" towards eachother"
        elif f == 'enemies':
            out = text1+" and "+text2
            out2 = "are "+f
        elif f == 'love':
            out = text1+" and "+text2
            out2 = "are in "+f
        else:
            out = "Invalid Data Provided"

        return render_template("relation.html", output = out, output2 = out2)
    else:
        return render_template("relation.html")

@app.route('/contact')
def contact():
    email = "prasanna.dhamodharan@gmail.com"
    return ('Email : ' + email)

def flame(person1,person2):
    values = {
        0:'No Match',        
        1:'siblings',
        2:'enemies',
        3:'friends',
        4:'married',
        5:'friends',
        6:'married',
        7:'enemies',
        8:'affection',
        9:'enemies',
        10:'love',
        11:'married',
        12:'affection',
        13:'affection',
        14:'friends',
        15:'married'      
    }
    
    for x in person1:
        if (x in person1) and (x in person2):
            person1 = person1.replace(x,'',1)
            person2 = person2.replace(x,'',1)
        l = len(person1+person2)
    return values[l]

if __name__ == "__main__":
    app.run(debug=True)