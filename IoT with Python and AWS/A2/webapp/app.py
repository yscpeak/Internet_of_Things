from flask import Flask, render_template

app = Flask(__name__)

# Use "http://107.23.225.26:80/" to access this route.
# After restart EC2 instance, HostName 107.23.225.26 in config file
# and the route will change.
# config file is located at C:\Users\USER\.ssh
@app.route('/')
def index():
    return render_template('index.html')

# Use "http://127.0.0.1/cakes" to access this route.
# Above route won't change.
@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'

@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    #app.run(debug=True, host='0.0.0.0', port=5000)
    #app.run(debug=True)