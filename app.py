from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "rttTbFgKzuS7EQdh-2zpovltcAgvtDRJ"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/melano/Desktop/Project Booking/instance/project_booking.db'

db = SQLAlchemy(app)

with app.app_context():
    print(db.engine.url)

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    short_description = db.Column(db.String)
    full_description = db.Column(db.String)
    image_link = db.Column(db.String)
    project_status = db.Column(db.String)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:

            session['logged_in'] = True

            return redirect('/admin')

    return render_template('login.html')

@app.route('/admin')
def admin():

    if not session.get('logged_in'):
        return redirect('/login')

    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/')
def index():
    projects = Project.query.order_by(
        Project.id.desc()
    ).all()

    return render_template(
        'index.html',
        our_projects=projects
    )


@app.route('/about-us')
def about_us():
    return render_template('about_us.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        full_description = request.form['full_description']
        link = request.form['image_link']
        project_status = request.form.get('project_status', 'open')

        project = Project(
            title=title,
            short_description=description,
            full_description=full_description,
            image_link=link,
            project_status=project_status
        )

        db.session.add(project)
        db.session.commit()

        return render_template(
            'success.html',
            title="პროექტი დაემატა",
            message="თქვენი პროექტი წარმატებით გამოქვეყნდა.",
            button_text="პროექტების ნახვა",
            redirect_url="/current-projects"
        )

    return render_template('new_project.html')


@app.route('/current-projects')
def current_projects():
    projects = Project.query.order_by(
        Project.id.desc()
    ).all()

    return render_template(
        'current_projects.html',
        projects=projects
    )


@app.route('/project/<int:project_id>')
def project_details(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found", 404

    return render_template(
        'project_details.html',
        project=project
    )


if __name__ == '__main__':
    app.run()