from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)



@app.route('/')
def index():
    conn = sqlite3.connect('project_booking.db')
    c = conn.cursor()

    projects = c.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    ).fetchall()

    our_projects = [{'id': row[0], 'title': row[1], 'short_description': row[2], 'image_link': row[4], 'project_status': row[5]} for row in projects]

    conn.close()

    return render_template(
        'index.html',
        our_projects=our_projects
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

        conn = sqlite3.connect('project_booking.db')
        c = conn.cursor()

        c.execute("""
            INSERT INTO projects (
                title,
                short_description,
                full_description,
                image_link,
                project_status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            description,
            full_description,
            link,
            project_status
        ))

        conn.commit()
        conn.close()

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

    conn = sqlite3.connect('project_booking.db')
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    projects = c.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        'current_projects.html',
        projects=projects
    )


@app.route('/project/<int:project_id>')
def project_details(project_id):

    conn = sqlite3.connect('project_booking.db')
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    project = c.execute(
        "SELECT * FROM projects WHERE id = ?",
        (project_id,)
    ).fetchone()

    conn.close()

    if project is None:
        return "Project not found", 404

    return render_template(
        'project_details.html',
        project=project
    )


if __name__ == '__main__':
    app.run()