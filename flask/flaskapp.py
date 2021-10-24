from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from dotenv import load_dotenv
from collections import Counter
import os
import sys
import math
import requests

# Load env variables
load_dotenv()

# Get env variables
tenor_key = os.getenv('TENOR_KEY')
jawsdb_maria_url = os.getenv('JAWSDB_MARIA_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = jawsdb_maria_url

Talisman(app, content_security_policy=None)

db = SQLAlchemy(app)
gifmood = db.Table('GifMood', db.metadata, autoload=True, autoload_with=db.engine)
results = db.session.query(gifmood).all()

ids, moods = zip(*results)
ids = list(set(ids))
ids.sort()
mood_set = list(set(moods))
mood_set.append('All')
mood_set.sort()

category_counts = Counter(moods) # Number of GIFs of each mood
category_counts['All'] = len(ids)

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

# Reverse list so newest gifs are at the top
preview_gifs.reverse()
gifs.reverse()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', preview_gifs=preview_gifs, 
                                        moods=mood_set,
                                        category_counts=category_counts, 
                                        gifs=gifs, 
                                        ids=ids, 
                                        id_moods=id_moods)

if __name__ == '__main__':
    app.run(debug=True)