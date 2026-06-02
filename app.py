from flask import Flask, render_template, request

app = Flask(__name__)

projects_list = []

@app.route('/')
def index():
    return render_template('index.html', our_projects=projects_list)

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
        description = request.form['description'][:150]
        full_description = request.form['full_description']
        link = request.form['link']
        project_status = request.form.get('project_status', 'open')

        new_created_project = {
            'id': len(projects_list),
            'title': title,
            'description': description,
            'full_description': full_description,
            'link': link,
            'project_status': project_status
        }
        projects_list.append(new_created_project)
        return render_template(
            'success.html',

            title='პროექტი დაემატა',

            message='თქვენი პროექტი წარმატებით გამოქვეყნდა Gzaari.ge-ზე.',

            button_text='მთავარ გვერდზე დაბრუნება',

            redirect_url='/'
        )
    return render_template('new_project.html')


@app.route('/current-projects')
def current_projects():
    return render_template('current_projects.html', projects=projects_list)


@app.route('/project/<int:project_id>')
def project_details(project_id):

    project = projects_list[project_id]

    return render_template(
        'project_details.html',
        project=project
    )

if __name__ == '__main__':
    app.run()