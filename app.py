from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Images'

if __name__ == "__main__":
    from api import *
    app.run(debug=True,use_reloader=True,port=5000)