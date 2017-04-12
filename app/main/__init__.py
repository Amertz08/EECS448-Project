from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, render_template

from forms import SearchForm

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        print('Search')
    return render_template('index.html', form=form)
