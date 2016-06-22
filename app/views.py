import datetime

from flask import render_template, redirect, url_for, g, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import login_required, roles_accepted
from flask_security.utils import encrypt_password

from app import app, db, models, forms
from config import MAX_SEARCH_RESULTS, ITEMS_PER_PAGE


@app.before_first_request
def create_user():
    if not models.User.query.first():
        models.user_datastore.create_user(
            id='1',
            email='rus.y2k@gmail.com',
            password=encrypt_password('gfhjkm'))
        db.session.commit()

    if not models.Role.query.first():
        models.user_datastore.create_role(
            id=1,
            name='admin',
            description='admin')
        models.user_datastore.create_role(
            id=2,
            name='manager',
            description='Менеджер'
        )
        models.user_datastore.create_role(
            id=3,
            name='logist',
            description='Логист'
        )
        models.user_datastore.add_role_to_user(
            user='rus.y2k@gmail.com',
            role='admin')
        db.session.commit()

@app.before_request
def before_request():
    g.search_form = forms.SearchForm()


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html', title="Заявки",
                           content=models.Rates.query.order_by(models.Rates.id.desc()).all())


@app.route('/search', methods=('GET', 'POST'))
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('search_results', query='all', page=1))
    return redirect(url_for('search_results', query=g.search_form.search.data, page=1))


@app.route('/search/<query>/<int:page>')
def search_results(query, page=1):
    if query == 'all':
        results = models.Rates.query.order_by(models.Rates.id.desc()).paginate(page, ITEMS_PER_PAGE, False)
    else:
        results = models.Rates.query.whoosh_search(query, MAX_SEARCH_RESULTS).order_by(models.Rates.id.desc()).paginate(
            page, ITEMS_PER_PAGE, False)
    return render_template('search.html',
                           query=query,
                           results=results)


@app.route('/create', methods=('GET', 'POST'))
def create():
    form = forms.CreateForm()

    if form.validate_on_submit():
        request = models.Rates(date=datetime.datetime.now(), client=form.client.data,
                               origin=form.origin.data, destination=form.destination.data,
                               capacity=form.capacity.data, type=form.type.data, comments=form.comments.data,
                               is_new=True)
        db.session.add(request)
        db.session.commit()
        flash('Успешно добавлено!')
        return redirect(url_for('rates'))

    return render_template('create.html', title='Создать заявку', form=form)


@app.route('/rates')
@app.route('/rates/<int:page>', methods=['GET', 'POST'])
def rates(page=1):
    # results = models.Rates.query.whoosh_search('*').all()
    content = models.Rates.query.order_by(models.Rates.id.desc()).paginate(page, ITEMS_PER_PAGE, False)

    return render_template('rates.html', title='Котировки', results=content)


@app.route('/edit/<int:item_id>', methods=('GET', 'POST'))
def edit(item_id):
    item = models.Rates.query.get(item_id)
    form = forms.EditForm()

    if form.validate_on_submit():
        item.rate = form.rate.data
        item.terms = form.terms.data
        item.comments = form.comments.data
        item.manager = form.manager.data
        db.session.commit()
        flash('Good')
        return redirect(url_for('rates'))

    if item:
        form.client.data = item.client
        form.origin.data = item.origin
        form.destination.data = item.destination
        form.capacity.data = item.capacity
        form.type.data = item.type
        form.rate.data = item.rate
        form.terms.data = item.terms
        form.manager.data = item.manager
        form.comments.data = item.comments

    return render_template('edit.html', form=form, id=str(item.id))


@app.route('/users')
@app.route('/users/<int:page>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def users(page=1):
    users_list = models.User.query.order_by(models.User.last_name.asc()).paginate(page, ITEMS_PER_PAGE, False)
    return render_template('users.html', title='Пользователи', users=users_list)


@app.route('/create_user', methods=('POST', 'GET'))
@login_required
@roles_accepted('admin')
def create_user():
    roles = []
    for item in models.Role.query.all():
        roles.append((item.name, item.description))

    form = forms.CreateUserForm()
    form.role.choices = roles

    if form.validate_on_submit():
        password = encrypt_password(form.password.data)
        models.user_datastore.create_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=password)
        models.user_datastore.add_role_to_user(form.email.data, form.role.data)
        db.session.commit()
        return redirect(url_for('create_user'))
    else:
        return render_template('create_u.html', title='Создать пользователя', form=form)


@app.route('/edit_user/<int:user_id>', methods=('POST', 'GET'))
def edit_user(user_id):
    roles = []
    for item in models.Role.query.all():
        roles.append((item.name, item.description))

    form = forms.EditUserForm()
    form.role.choices = roles

    user = models.user_datastore.get_user(user_id)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        if form.password.data:
            user.password = encrypt_password(form.password.data)
        if form.role.data not in user.roles:
            models.user_datastore.remove_role_from_user(user_id, user.roles)
            models.user_datastore.add_role_to_user(user_id, form.role.data)

        if form.active.data:
            models.user_datastore.activate_user(user)
        else:
            models.user_datastore.deactivate_user(user)
        db.session.commit()
        flash('Good')
        return redirect(url_for('users'))

    if user:
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        if user.is_active:
            form.active.data = True
        else:
            form.active.data = False
        return render_template('edit_user.html', form=form, id=str(user_id))





admin = Admin(app, name='Справочник', template_mode='bootstrap3')
admin.add_view(ModelView(models.Rates, db.session))
