#! /usr/local/Cellar/python3/3.5.2/bin/python3
from app import app

app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=app.config['PORT'], threaded=True)
