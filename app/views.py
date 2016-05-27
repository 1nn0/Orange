import datetime

from flask import render_template, redirect, url_for, g, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db, models, forms
from config import MAX_SEARCH_RESULTS, ITEMS_PER_PAGE
from .forms import CreateForm, EditForm


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
    form = CreateForm()

    if form.validate_on_submit():
        request = models.Rates(date=str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M")), client=form.client.data,
                               origin=form.origin.data, destination=form.destination.data,
                               capacity=form.capacity.data, type=form.type.data, comments=form.comments.data)
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


@app.route('/edit/<item_id>', methods=('GET', 'POST'))
def edit(item_id):
    item = models.Rates.query.get(item_id)
    form = EditForm()

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


admin = Admin(app, name='Справочник', template_mode='bootstrap3')
admin.add_view(ModelView(models.Rates, db.session))
