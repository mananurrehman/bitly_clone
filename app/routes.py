import string
from flask import Blueprint, render_template, request, redirect, flash
from app import db
from app.models import Link

bp = Blueprint('main', __name__)

# Pool for available character like IPs in DHCP Pool
CHAR_POOL = string.digits + string.ascii_lowercase + string.ascii_uppercase

@bp.route('/', methods=['GET', 'POST'])
def home():
    short_url = None

    if request.method == 'POST':
        original_url = request.form.get('url')

        if not original_url:
            flash("URL is required!", "error")
            return redirect('/')

        # generate 3-char short code (temporary simple version)
        import random
        short_code = ''.join(random.choice(CHAR_POOL) for _ in range(3))

        try:
            link = Link(short_code=short_code, original_url=original_url)
            db.session.add(link)
            db.session.commit()
            short_url = short_code

        except Exception as e:
            db.session.rollback()
            flash("Something went wrong while saving URL", "error")

    return render_template('index.html', short_url=short_url)


# ===> Redirect Logic

@bp.route('/<short_code>')
def redirect_to_url(short_code):
    # Search the database for this specific 1-char code
    # .first() bcz 'short_code'=unique

    link = Link.query.filter_by(short_code=short_code).first()

    if link:
        # if found, then redirect to original_orl
        # Link.times_visited += 1

        return redirect(link.original_url)
    
    #if not, then don't exist
    flash("Sorry, that short link doesn't exist!", "error")
    return redirect('/')
