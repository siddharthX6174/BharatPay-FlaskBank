from app import app
from flask import render_template
from app.utils.stats import get_global_stats

@app.route('/services')
def services_page():
    stats = get_global_stats()
    return render_template('root/services.html', stats=stats)


