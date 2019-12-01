from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from wtforms import BooleanField

from studentportal.frontend import bp
from studentportal.models import mongo
from studentportal.frontend.forms import CreateProfileForm, FilterModulesForm


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


@bp.route('/modules', methods=['GET', 'POST'])
def modules():
    filter_form = FilterModulesForm()

    # Add all possible filter options (possibly should be curated in the future
    for one_school in sorted(mongo.db.modules.distinct('school')):
        if not one_school:
            continue
        filter_form.school.choices.append((one_school.replace(" ", "_").lower(), one_school))

    for one_subject in sorted(mongo.db.modules.distinct('subject_area_group')):
        if not one_subject:
            continue
        filter_form.subject.choices.append((one_subject.replace(" ", "_").lower(), one_subject))

    for one_scqf_level in sorted(mongo.db.modules.distinct('scqf_level')):
        if not one_scqf_level:
            continue
        filter_form.scqf_level.choices.append((one_scqf_level.replace(" ", "_").lower(), one_scqf_level))

    for one_delivery_loc in sorted(mongo.db.modules.distinct('teaching_instances.delivery_location')):
        if not one_delivery_loc:
            continue
        filter_form.delivery_location.choices.append((one_delivery_loc.replace(" ", "_").lower(), one_delivery_loc))

    for one_trimester in sorted(mongo.db.modules.distinct('teaching_instances.trimester')):
        if not one_trimester:
            continue
        filter_form.trimester.choices.append((one_trimester.replace(" ", "_").lower(), one_trimester))

    for one_term in sorted(mongo.db.modules.distinct('teaching_instances.term')):
        if not one_term:
            continue
        filter_form.term.choices.append((one_term.replace(" ", "_").lower(), one_term))

    for one_delivery_mode in sorted(mongo.db.modules.distinct('teaching_instances.delivery_mode')):
        if not one_delivery_mode:
            continue
        filter_form.delivery_mode.choices.append((one_delivery_mode.replace(" ", "_").lower(), one_delivery_mode))

    # If filter form was submitted apply filters
    query = {}
    if filter_form.is_submitted():
        if filter_form.school.data:
            query['school'] = {'$in': filter_form.school.data}
        if filter_form.subject.data:
            query['subject_area_group'] = {'$in': filter_form.subject.data}
        if filter_form.scqf_level.data:
            query['scqf_level'] = {'$in': filter_form.scqf_level.data}
        if filter_form.delivery_location.data:
            query['teaching_instances.delivery_location'] = {'$in': filter_form.delivery_location.data}
        if filter_form.trimester.data:
            query['teaching_instances.trimester'] = {'$in': filter_form.trimester.data}
        if filter_form.term.data:
            query['teaching_instances.term'] = {'$in': filter_form.term.data}
        if filter_form.delivery_mode.data:
            query['teaching_instances.delivery_mode'] = {'$in': filter_form.delivery_mode.data}

    page = request.args.get('page', 1, type=int)
    skips = (page - 1) * 20
    module_data = list(mongo.db.modules.find(query).skip(skips).limit(20))

    return render_template('module-list.html', data=module_data, form=filter_form)


@bp.route('/my/modules')
def my_modules():
    return render_template('base.html')

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
