from flask import Flask , render_template,request, url_for, redirect , flash
from form import MyForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'databases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
    
@app.route('/view')
def view():
    users = User.query.all()
    return render_template('view.html', users=users) 

@app.route('/view/<int:id>/edit', methods=['POST','GET'])      
def edit(id):
    user = User.query.get(id)
    form = MyForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        flash("User updated successfully")
        return redirect(url_for('view'))
    return render_template('edit.html', form=form, user=user)

@app.route('/', methods=['POST','GET'])
def login():
    form=MyForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash("form submitted successfully")
        return redirect(url_for('login'))
    else:
        return render_template('login.html' , form=form)



if __name__ == '__main__':
    app.run(debug=True)
