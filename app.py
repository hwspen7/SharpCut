from flask import Flask, send_file
from routes import upload_routes, download_routes, feedback_routes

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(upload_routes.bp)
app.register_blueprint(download_routes.bp)
app.register_blueprint(feedback_routes.bp)

# Safer: directly serve the file using send_file
@app.route('/')
def index():
    return send_file('index.html')

@app.route('/main.js')
def serve_js():
    return send_file('main.js')

if __name__ == '__main__':
    app.run(debug=True)


