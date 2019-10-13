from flask import Flask, render_template, jsonify

subscriptions = ['Crime Junkie', 'Swindled', 'The Dollop']

app = Flask(__name__,
    static_folder = "./dist/static",
    template_folder = "./dist"
)

@app.route('/')
def index():
    """
    Serve Vue App
    """
    return (render_template('index.html'))

@app.route('/subscriptions', methods=['GET'])
def serve_all_subscriptions():
    return jsonify({'items': subscriptions})

@app.after_request
def add_header(req):
    """
    Clear Cache for hot-reloading
    """
    req.headers["Cache-Control"] = "no-cache"
    return req

if __name__ == "__main__":
    app.run(debug=True)