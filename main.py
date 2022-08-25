from api_handler import app


@app.route('/')
def hello():
    return "<h1>API for Fact Checker</h1>"


if __name__ == '__main__':
    app.run()
