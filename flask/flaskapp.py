from flask import Flask, render_template, request, Response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from dotenv import load_dotenv
from collections import Counter
import os
import sys
import math
import requests
import json

# Load environment variables
load_dotenv()
tenor_key = os.getenv('TENOR_KEY')
jawsdb_maria_url = os.getenv('JAWSDB_MARIA_URL')

# Configure application
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = jawsdb_maria_url

talisman = Talisman(app, content_security_policy=None)

# Establish DB connection and fetch content
db = SQLAlchemy(app)
gifmood = db.Table('GifMood', db.metadata, autoload=True, autoload_with=db.engine)
results = db.session.query(gifmood).all()
ids, moods = zip(*results)
ids = list(set(ids))
ids.sort()
# Get Mood translations
moods_translated = db.Table('Mood', db.metadata, autoload=True, autoload_with=db.engine)
translated_results = db.session.query(moods_translated).all()
translated_results.sort(key=lambda x:x[1])
translated_results = [('All', 'Alle')] + translated_results
translated_moods = dict(translated_results)
mood_set = list(translated_moods.keys())

category_counts = Counter(moods) # Number of GIFs of each mood
category_counts['All'] = len(ids)

# Get which gifs have text
gif_db = db.Table('Gif', db.metadata, autoload=True, autoload_with=db.engine)
has_text = [(i[0], i[4]) for i in db.session.query(gif_db).all()]
has_text = dict(has_text)

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
    request_string = 'https://g.tenor.com/v1/gifs?media_filter=minimal&key=' + tenor_key + '&ids=' + str(id_strings)
    response = requests.get(request_string).json()

    for result in response['results']:
        preview_gifs.append(result['media'][0]['tinygif']['url'])
        gifs.append(result['url'])

# Reverse lists so newest gifs are at the top
ids.reverse()
id_moods.reverse()
preview_gifs.reverse()
gifs.reverse()

# GOT ERRORS ON SQL
# SO FOR NOW, THE VALUES ARE HARDCODED HERE!
moods_emojies = dict()
moods_emojies['All'] = "\U0001F468" + u'\u200d' + "\U0001F373"
moods_emojies['Angry'] = "\U0001F621"
moods_emojies['Annoyed'] = "\U0001F644"
moods_emojies['Cheerful'] = "\U0001F917"
moods_emojies['Confused'] = "\U0001F635"
moods_emojies['Disappointed'] = "\U0001F612"
moods_emojies['Disgusted'] = "\U0001F922"
moods_emojies['Funny'] = "\U0001F602"
moods_emojies['Happy'] = "\U0001F603"
moods_emojies['Negative'] = "\U0001F44E"
moods_emojies['Positive'] = "\U0001F44D"
moods_emojies['Romantic'] = "\U0001F970"
moods_emojies['Sad'] = "\U0001F614"
moods_emojies['Scared'] = "\U0001F630"
moods_emojies['Serious'] = "\U0001F611"
moods_emojies['Surprised'] = "\U0001F62F"


@app.route('/')
def home():
    return render_template('home.html', preview_gifs=preview_gifs, 
                                        moods=mood_set,
                                        category_counts=category_counts, 
                                        gifs=gifs, 
                                        ids=ids, 
                                        id_moods=id_moods,
                                        translated_moods=translated_moods,
                                        has_text=has_text,
                                        moods_emojies=moods_emojies)

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

# Setting content-type for served JavaScript
@app.route('/static/script.js')
def script():
    return send_from_directory(app.static_folder, 'script.js', mimetype='text/javascript')

if __name__ == '__main__':
    app.run(debug=True)