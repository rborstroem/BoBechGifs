from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import sys
import math
import requests

# Load env variables
load_dotenv()

# Get env variables
key = os.getenv('TENOR_KEY')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_db = os.getenv('DB_DB')
maria_db = os.getenv('JAWSDB_MARIA_URL')

'''
# Try to connect to database
# If errors occurs, set use_db to false
try: 
    conn = mariadb.connect(
        user=db_user,
        password=db_pass,
        host=db_host,
        port=3306,
        database=db_db
    )

    cur = conn.cursor()
    
    cur.execute("SELECT ID, MoodType FROM GifMood")

    ids, moods = zip(*cur)



except mariadb.Error as e:
    print(f"Error connecting to MariaDB platform: {e}")

'''

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = maria_db
db = SQLAlchemy(app)

#db.create_all()

gifmood = db.Table('GifMood', db.metadata, autoload=True, autoload_with=db.engine)

results = db.session.query(gifmood).all()

ids, moods = zip(*results)

moods = list(set(moods)).sort()
ids = list(set(ids)).sort()
preview_gifs = []
gifs = []

max_ids = 50
number_of_iterations = math.floor(len(ids) / max_ids)

for i in range(number_of_iterations):
    id_strings = ",".join([str(i) for i in ids[i*max_ids:(i+1)*max_ids]])
    response = requests.get('https://g.tenor.com/v1/gifs?media_filter=minimal&key='+key+'&ids='+str(id_strings)).json()

    for result in response['results']:
        preview_gifs.append(result['media'][0]['tinygif']['url'])
        gifs.append(result['url'])

# REMAINDER
remaining = len(ids) - max_ids * number_of_iterations
id_strings = ",".join([str(i) for i in ids[len(ids) - remaining:]])
response = requests.get('https://g.tenor.com/v1/gifs?media_filter=minimal&key='+key+'&ids='+str(id_strings)).json()
for result in response['results']:
    preview_gifs.append(result['media'][0]['tinygif']['url'])
    gifs.append(result['url'])

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', preview_gifs=preview_gifs, moods=moods, gifs=gifs)

if __name__ == '__main__':
    app.run(debug=True)