from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import sys

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

results = db.session.execute(GifMood).all()

ids, moods = zip(*results)


# TODO: Fetch GIFs from database
gifs = ['https://c.tenor.com/54UdL_zUuG0AAAAC/bo-bech-med-kniven-for-struben.gif', 'https://c.tenor.com/0yhDLNgdffIAAAAC/med-kniven-for-struben-bo-bech.gif', 'https://c.tenor.com/OQyn2OuUrx4AAAAd/bo-bech-med-kniven-for-struben.gif', 
        'https://c.tenor.com/xrT1B6ZMI44AAAAd/bo-bech-med-kniven-for-struben.gif', 'https://c.tenor.com/xleCMjEzHOUAAAAC/med-kniven-for-struben-bo-bech.gif', 'https://c.tenor.com/DMumjMaVEO0AAAAd/bo-bech-med-kniven-for-struben.gif']
# TODO: Fetch moods from database
# moods = ['angry', 'annoyed', 'cheerful', 'disappointed', 'disgusted', 'funny', 'happy', 'negative', 'romantic', 'sad', 'serious', 'surprised']

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', gifs=gifs, moods=moods)

if __name__ == '__main__':
    app.run(debug=True)