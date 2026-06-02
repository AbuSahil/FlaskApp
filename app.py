from flask import Flask , render_template,request, url_for, redirect , flash
from form import MyForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Blog('{self.title}', '{self.date_posted}')"
    


@app.route('/')
def view():
    users = User.query.all()
    return render_template('view.html', users=users) 

@app.route('/<int:id>/edit', methods=['POST','GET'])      
def edit(id):
    user = User.query.get(id)
    form = MyForm(obj=user)
    if form.validate_on_submit():
        user.id = form.id.data
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

#blogs
@app.route('/blogs')
def blogs():
    blogs = Blog.query.order_by(Blog.date_posted.desc()).all()
    return render_template('Blogs/blogs.html', blogs=blogs)

@app.route('/blogs/create', methods=['POST', 'GET'])
def create_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_blog = Blog(title=title, content=content)
        db.session.add(new_blog)
        db.session.commit()
        flash("বলগ সফলভাবে তৈয়াৰ কৰা হৈছে!")
        return redirect(url_for('blogs'))
    return render_template('Blogs/create.html')

@app.route('/blogs/<int:blog_id>/edit', methods=['POST', 'GET'])
def edit_blog(blog_id):  
    blog = Blog.query.get(blog_id)
    if request.method == 'POST':
        blog.title = request.form['title']
        blog.content = request.form['content']
        
        db.session.commit()
        flash("বলগ সফলভাবে সম্পাদনা কৰা হৈছে!")
        return redirect(url_for('blogs'))
    return render_template('Blogs/editblog.html', blog=blog)    

if __name__ == '__main__':
    with app.app_context():  
        db.create_all()
    app.run(debug=True)
