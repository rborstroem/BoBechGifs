from flask import Flask, render_template
from dotenv import load_dotenv
import os
import sys

# Load env variables
load_dotenv()

token = os.getenv('TEST')
print('TOKEN: ' + token, file=sys.stderr)

app = Flask(__name__)

# TODO: Fetch GIFs from database
gifs = ['https://c.tenor.com/54UdL_zUuG0AAAAC/bo-bech-med-kniven-for-struben.gif', 'https://c.tenor.com/0yhDLNgdffIAAAAC/med-kniven-for-struben-bo-bech.gif', 'https://c.tenor.com/OQyn2OuUrx4AAAAd/bo-bech-med-kniven-for-struben.gif', 
        'https://c.tenor.com/xrT1B6ZMI44AAAAd/bo-bech-med-kniven-for-struben.gif', 'https://c.tenor.com/xleCMjEzHOUAAAAC/med-kniven-for-struben-bo-bech.gif', 'https://c.tenor.com/DMumjMaVEO0AAAAd/bo-bech-med-kniven-for-struben.gif']
# TODO: Fetch moods from database
moods = ['angry', 'annoyed', 'cheerful', 'disappointed', 'disgusted', 'funny', 'happy', 'negative', 'romantic', 'sad', 'serious', 'surprised']

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', gifs=gifs, moods=moods)

if __name__ == '__main__':
    app.run(debug=True)