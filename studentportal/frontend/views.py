from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user

from studentportal.frontend import bp
from studentportal.models import mongo
from studentportal.frontend.forms import CreateProfileForm


@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.dashboard'))
    return render_template('guest_home.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@bp.route('/feed')
@login_required
def feed():
    return render_template('feed.html')


@bp.route('/todo')
@login_required
def todo():
    return render_template('todo-list.html')


@bp.route('/u/<username>', methods=['GET', 'POST'])
def profile(username):
    profile_data = mongo.db.profiles.find_one({"_id": username})
    if profile_data is None:
        if current_user.is_authenticated and current_user.get_id() == username:
            form = CreateProfileForm()
            if form.validate_on_submit():
                profile_json = {
                    "_id": username,
                    "first_name": form.first_name.data,
                    "last_name": form.last_name.data,
                    "skills": form.skills.data,
                    "location": form.location.data,
                    "home_location": form.home_location.data,
                    "company": form.company.data,
                    "website": form.website.data,
                    "linked_in": form.linked_in.data,
                    "twitter": form.twitter.data,
                    "instagram": form.instagram.data,
                    "about": form.about.data,
                    "profile_picture_url": 'todo'
                }
                mongo.db.profiles.insert_one(profile_json)
                return redirect(url_for('frontend.profile', username=username))
            return render_template('create_profile.html', form=form)
        else:
            return redirect(url_for('auth.login'))
    return render_template('profile.html', profile=profile_data)


@bp.route('/calendar')
def calendar():
    return render_template('calendar.html')


@bp.route('/projects')
def projects():
    return render_template('project-list.html')


@bp.route('/project/<project_slug>')
def project_page(project_slug):
    return render_template('project.html')


@bp.route('/modules')
def modules():
    filter = request.args.get('filter')
    if filter == 'enrolled':
        print('Enrolled filter not implemented yet')
        # TODO: Get enrolled modules, apply filter in mongo query
    page = request.args.get('page', 1, type=int)
    skips = (page - 1) * 20
    module_data = list(mongo.db.modules.find().skip(skips).limit(20))
    return render_template('module-list.html', data=module_data)


@bp.route('/module/<module_code>')
def module_page(module_code):
    module_data = mongo.db.modules.find_one({"_id": module_code})
    if not module_data:
        abort(404)
    return render_template('module.html', data=module_data).encode('utf-8')


@bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
