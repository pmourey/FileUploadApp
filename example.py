from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.debug=True
app.config['SECRET_KEY'] = 'DontTellAnyone'

toolbar = DebugToolbarExtension(app)

@app.route("/",methods=["GET"])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()