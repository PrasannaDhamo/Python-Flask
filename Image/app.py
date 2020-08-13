import os
from flask import Flask, render_template, request
from PIL import Image
import datetime
import shutil
import requests


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['GET','POST'])
def upload():
    path = os.path.join(APP_ROOT, 'images/')

    if not os.path.isdir(path):
        os.mkdir(path)

    dates = set()
    i = 1
    print(request.files.getlist("file"))

    for x in request.files.getlist("file"):
        age = Image.open(x)
        EXIF_data = age._getexif()
        if EXIF_data == None:
            print("No Data Found for " + x)
            age.close()
        else:
            dt = EXIF_data[306]
            dat = dt[0:10]
            dates_dash = dat.replace(":", "-")
            dates.add(dates_dash)
            rname = dates_dash+"("+ str(i) +")"+'.jpg'
            destination = "/".join([path, rname])
            x.save(destination)
            if not os.path.isdir("images/" + dates_dash):
                os.mkdir("images/" + dates_dash)
                
            i+=1
    path1 = os.listdir(path)            
    for y in path1:
        for d in dates:
            if y.startswith(d):
                mov_dir = os.getcwd() + "\images" +"\\" + d
                current_dir = os.getcwd() + "\images" + "\\" + y
                shutil.move(current_dir, mov_dir)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)



