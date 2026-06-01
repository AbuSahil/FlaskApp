from flask import Flask , render_template,request


app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form['email']
        return f"Data submitted successfully! Name: {name} and Email: {email}"
    else:
        return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
