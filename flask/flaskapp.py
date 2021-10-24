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

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = maria_db
db = SQLAlchemy(app)

gifmood = db.Table('GifMood', db.metadata, autoload=True, autoload_with=db.engine)

results = db.session.query(gifmood).all()

ids, moods = zip(*results)

moods = list(set(moods))
moods.append('All')
moods.sort()
ids = list(set(ids))
ids.sort()
preview_gifs = [] # links for preview gifs used on the webpage
gifs = [] # links for copy of high quality gif versions

# Create a list for each id
# containing list of moods with that mood
# transformed into string
id_moods = []

for idx,id in enumerate(ids):
    moods_for_this_id = ['All']
    for (gif_id, mood) in results:
        if (id == gif_id):
            moods_for_this_id.append(mood)

    mood_data = ("-").join(moods_for_this_id)
    id_moods.append(mood_data)
    

# Maximally 50 GIFs can be fetched from Tenor with a single API call
tenor_limit = 50
iterations  = math.ceil(len(ids) / tenor_limit)
for i in range(iterations):
    # 1. [1, 2, 3, ...] (ids)
    # 2. ["1","2","3",...] (str list comprehension)
    # 3. "1,2,3,..." (join)
    id_strings = ",".join([str(id_no) for id_no in ids[i*tenor_limit:(i+1)*tenor_limit]])
    request_string = 'https://g.tenor.com/v1/gifs?media_filter=minimal&key=' + key + '&ids=' + str(id_strings)
    response = requests.get(request_string).json()

    for result in response['results']:
        preview_gifs.append(result['media'][0]['tinygif']['url'])
        gifs.append(result['url'])

# Reverse list so newest gifs are at the top
preview_gifs.reverse()
gifs.reverse()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', preview_gifs=preview_gifs, moods=moods, gifs=gifs, ids=ids, id_moods=id_moods)

if __name__ == '__main__':
    app.run(debug=True)