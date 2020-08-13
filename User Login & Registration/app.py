from flask import Flask, request, render_template, url_for, redirect
from pymongo import MongoClient

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
        uname = request.form['uname']
        doc = {"username" : uname,"password" : request.form['pwd'],"email" : request.form['email']}
        cl.insert_one(doc)
        return redirect(url_for('success', name = uname))


@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def lg():
    if request.method == 'POST': 

        validate = cl.find_one({"username": request.form['un'], "password": request.form['psw']})
        
        if validate == None:
            return redirect(url_for('invalid'))
        else:
            return redirect(url_for('success', name = request.form['un']))


@app.route('/success/<name>')
def success(name):
    return "Welcome %s....!" %name

@app.route('/invalid')
def invalid():
    return "Invalid Username/Password....!"


if __name__ == "__main__":
    app.run(debug=True)