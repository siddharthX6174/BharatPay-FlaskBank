from app import app
from flask import render_template
from app.utils.stats import get_global_stats

@app.route('/about')
def about_page():
    stats = get_global_stats()
    return render_template('root/about.html', stats=stats)

