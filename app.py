from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Hello Render!</h1>
    <p>Website Python Flask đầu tiên của tôi.</p>
    <p>Update lần 1.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)