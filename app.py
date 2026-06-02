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
    
@app.route('/')
def view():
    users = User.query.all()
    return render_template('view.html', users=users) 

@app.route('/<int:id>/edit', methods=['POST','GET'])      
def edit(id):
    user = User.query.get(id)
    form = MyForm(obj=user)
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("এই ইমেইল ইতিমধ্যে ব্যৱহাৰ কৰা হৈছে!")
            return render_template('edit.html', form=form, user=user)
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        flash("আপোনাৰ তথ্য সফলভাবে সম্পাদনা কৰা হৈছে!")
        return redirect(url_for('view'))
    return render_template('edit.html', form=form , user=user)
@app.route('/<int:id>/delete', methods=['POST','GET'])
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash("আপোনাৰ তথ্য সফলভাবে মচা হৈছে!")
    return redirect(url_for('view'))    

@app.route('/<int:id>/show')
def show(id):   
    user = User.query.get(id)
    return render_template('show.html', user=user) 
    
@app.route('/login', methods=['POST','GET'])
def login():
    form=MyForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("এই ইমেইল ইতিমধ্যে ব্যৱহাৰ কৰা হৈছে!")
            return render_template('login.html', form=form)
        else:
            new_user = User(name=form.name.data, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
            flash("আপনাৰ তথ্য সফলভাবে সংৰক্ষণ কৰা হৈছে!")
            return redirect(url_for('login'))
    else:
        return render_template('login.html' , form=form)



if __name__ == '__main__':
    app.run(debug=True)
