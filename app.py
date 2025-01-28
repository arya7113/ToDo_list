from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from model import *
from datetime import datetime

app=Flask(__name__) #turns this file into a web application

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ToDodata.sqlite3"
app.config['SECRET_KEY'] = 'your-secret-key-here' 



db.init_app(app)
app.app_context().push()
    

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_login = Login.query.filter_by(username=username).first()
        print(user_login)
        
        if user_login and check_password_hash(user_login.password, password):
            
            user = User.query.filter_by(login_id=user_login.id).first()
            session['user_id'] = user.id
            print(session)
            
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template("login.html")
    
@app.route("/home",methods=["GET","POST"])
def home():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    tasks = Task.query.filter_by(user_id=user_id).all()
    categories = TaskCategory.query.all()

    return render_template('home.html', user=user,
                           tasks=tasks,
                           categories=categories)
    

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')
        

        if Login.query.filter_by(username=username).first():
            flash("Username Already Exist")
            return redirect(url_for('signup'))
            
        if User.query.filter_by(email=email).first():
            flash("Email already exist")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)

        new_login=Login(username=username,password=hashed_password)
        db.session.add(new_login)
        db.session.commit()

        new_user=User(login_id=new_login.id,
                      name=name,
                      email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("Regitered Successfully! Please Login.")
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/task',methods=["GET","POST"])
def task():
    if request.method=="POST":
        category_name=request.form.get('category')
        task_description=request.form.get('task')
        priority_value=request.form.get('priority')
        date_str = request.form.get('date')
    

        # get or create category
        category_obj = TaskCategory.query.filter_by(category=category_name).first()
        if not category_obj:
            category_obj=TaskCategory(category=category_name)
            db.session.add(category_obj)
            db.session.commit()
        
        #new task

        new_task = Task(
            category_id = category_obj.id,
            user_id = session['user_id'],
            task=task_description,
            priority=priority_value,
            status=task_status.Pending,
            date= datetime.strptime (date_str,'%Y-%m-%d')
        )
        db.session.add(new_task)
        db.session.commit()

        flash("Task Added Sccessfully! Now complete this Bitch!!!")
        return redirect(url_for('home'))
        
    categories=[cat.value for cat in category ]
    priorities=[prior.value for prior in priority ]
    status=[status.value for status in task_status]
    return render_template('task.html',categories=categories,priorities=priorities,status=status)

@app.route('/update_task/<int:task_id>', methods=["POST"])
def update_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    task=Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        flash("Unthorised Access!")
        return redirect(url_for('home'))
    
    new_status=request.form.get("status")
    task.status=task_status(new_status)
    print(task.status)
    db.session.commit()

    flash("Status updated Successfully!")
    return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('index'))


def initialize_db():
    with app.app_context():
        db.create_all()

        for cat in category:
                existing_category = TaskCategory.query.filter_by(category=cat.value).first()
                if not existing_category:
                    new_category = TaskCategory(category=cat.value)
                    db.session.add(new_category)
    db.session.commit()


if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)

