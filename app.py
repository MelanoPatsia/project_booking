from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import re

app = Flask(__name__)
app.secret_key = "rttTbFgKzuS7EQdh-2zpovltcAgvtDRJ"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:////Users/melano/Desktop/Project Booking/instance/project_booking.db'
)

db = SQLAlchemy(app)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper



class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    short_description = db.Column(db.String)
    full_description = db.Column(db.String)
    image_link = db.Column(db.String)
    project_status = db.Column(db.String)
    additional_info = db.Column(db.String)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.template_filter('linkify')
def linkify(text):

    if not text:
        return ""

    url_pattern = r'(https?://[^\s]+)'

    text = re.sub(
        url_pattern,
        r'<a href="\1" target="_blank">\1</a>',
        text
    )

    return text

@app.route('/')
def index():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('index.html', our_projects=projects)


@app.route('/about-us')
def about_us():
    return render_template('about_us.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        new_contact = Contact(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )

        db.session.add(new_contact)
        db.session.commit()

        return render_template(
            'success.html',
            base_template="base.html",
            title="შეტყობინება გაიგზავნა",
            message="თქვენი შეტყობინება წარმატებით გაიგზავნა.",
            button_text="მთავარ გვერდზე დაბრუნება",
            redirect_url="/"
        )

    return render_template('contact.html')


@app.route('/current-projects')
def current_projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('current_projects.html', projects=projects)


@app.route('/project/<int:project_id>')
def project_details(project_id):

    project = db.session.get(Project, project_id)

    if not project:
        return "Project not found", 404

    return render_template('project_details.html', project=project)



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        user = User.query.filter_by(
            email=request.form['email'],
            password=request.form['password']
        ).first()

        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for('admin'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')



@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('admin_projects.html', projects=projects)


@app.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():

    if request.method == 'POST':

        project = Project(
            title=request.form['title'],
            short_description=request.form['description'],
            full_description=request.form['full_description'],
            image_link=request.form['image_link'],
            project_status=request.form.get('project_status', 'open'),
            additional_info = request.form['additional_info']
        )

        db.session.add(project)
        db.session.commit()

        return render_template(
            'success.html',
            base_template="admin_base.html",
            title="პროექტი დაემატა",
            message="პროექტი წარმატებით შეიქმნა.",
            button_text="ადმინ პანელი",
            redirect_url=url_for('admin_projects')
        )

    return render_template('new_project.html')


@app.route('/admin/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):

    project = db.session.get(Project, project_id)

    if not project:
        return "Project not found", 404

    if request.method == 'POST':

        project.title = request.form['title']
        project.short_description = request.form['short_description']
        project.full_description = request.form['full_description']
        project.image_link = request.form['image_link']
        project.project_status = request.form['project_status']
        project.additional_info = request.form.get('additional_info', '')

        db.session.commit()

        return redirect(url_for('admin_projects'))

    return render_template('edit_project.html', project=project)


@app.route('/admin/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):

    project = db.session.get(Project, project_id)

    if not project:
        return "Project not found", 404

    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('admin_projects'))



@app.route('/admin/contacts')
@login_required
def admin_contacts():

    contacts = Contact.query.order_by(Contact.id.desc()).all()
    return render_template('admin_contacts.html', contacts=contacts)


@app.route('/admin/contacts/delete/<int:contact_id>', methods=['POST'])
@login_required
def delete_contact(contact_id):

    contact = db.session.get(Contact, contact_id)

    if not contact:
        return "Not found", 404

    db.session.delete(contact)
    db.session.commit()

    return redirect(url_for('admin_contacts'))



if __name__ == '__main__':
    app.run(debug=True)