from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
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


app = Flask(__name__)
Talisman(app, content_security_policy=None)

app.config['SQLALCHEMY_DATABASE_URI'] = maria_db
db = SQLAlchemy(app)

#db.create_all()

gifmood = db.Table('GifMood', db.metadata, autoload=True, autoload_with=db.engine)

results = db.session.query(gifmood).all()

ids, moods = zip(*results)

moods = list(set(moods))
moods.append('All')
moods.sort()
ids = list(set(ids))
ids.sort()
preview_gifs = []
gifs = []


# Create a dictionary with mood as key
# containing list of ids with that mood
# 
moods_gif = dict() 
ids_moods = dict()

for mood in moods:
    moods_gif[mood] = []
    for (id, mood_type) in results:
        if (mood == mood_type):
            moods_gif[mood].append(id)

for id in ids:
    ids_moods[id] = []
    for (gif_id, mood_type) in results:
        if (gif_id == id):
            ids_moods[id].append(mood_type)


id_moods = []

for idx,id in enumerate(ids):
    moods_for_this_id = ['All']
    for (gif_id, mood) in results:
        if (id == gif_id):
            moods_for_this_id.append(mood)

    mood_data = ("-").join(moods_for_this_id)
    id_moods.append(mood_data)
    

# for test in id_moods:
#    print(test)


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
    return render_template('home.html', preview_gifs=preview_gifs, moods=moods, gifs=gifs, ids=ids, moods_gif=moods_gif, ids_moods=ids_moods, id_moods=id_moods)

if __name__ == '__main__':
    app.run(debug=True)