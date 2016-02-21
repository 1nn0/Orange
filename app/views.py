from flask import render_template, redirect, url_for, g
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app import app, db, models, forms
from config import MAX_SEARCH_RESULTS


@app.before_request
def before_request():
    g.search_form = forms.SearchForm()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Test", content=models.Sprav.query.all())

@app.route('/search', methods=('GET', 'POST'))
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('search_results', query='*'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search/<query>')
def search_results(query):
    results = models.Sprav.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search.html',
                           query=query,
                           results=results)

admin = Admin(app, name='Справочник', template_mode='bootstrap3')
admin.add_view(ModelView(models.Sprav, db.session))