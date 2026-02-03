from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
import random
import string
from app import db

bp = Blueprint('main', __name__)

# Pool for available character like IPs in DHCP Pool
CHAR_POOL = string.digits + string.ascii_lowercase + string.ascii_uppercase

# ===== DASHBAORD ROUTE ======
@bp.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    from app.models import Link
    short_url = None

    if request.method == 'POST':
        original_url = request.form.get('url')
        if not original_url:
            flash('URL is required', 'error')
            return redirect(url_for('main.dashboard'))
        
        #generate random short_code
        short_code = ''.join(random.choice(CHAR_POOL) for _ in range(3))

        #ensure unique short_code
        while Link.query.filter_by(short_code=short_code).first():
            short_code = ''.join(random.choice(CHAR_POOL) for _ in range(3))

        #save link with current user
        try:
            link = Link(short_code=short_code, original_url=original_url, user_id=current_user.id)
            db.session.add(link)
            db.session.commit()
            short_url = url_for("main.redirect_to_url", short_code=short_code, _external=True) #new code added
            flash(f"Short link created: {short_url}", 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash("Error saving URL", 'error')
            
    links = Link.query.filter_by(user_id=current_user.id).order_by(Link.created_at.desc()).all()
    return render_template('dashboard.html', links=links)


# @bp.route('/', methods=['GET', 'POST'])
# def home():
#     from models import Link
#     short_url = None

#     if request.method == 'POST':
#         original_url = request.form.get('url')

#         if not original_url:
#             flash("URL is required!", "error")
#             return redirect('/')

#         # generate 3-char short code (temporary simple version)
#         import random
#         short_code = ''.join(random.choice(CHAR_POOL) for _ in range(3))

#         try:
#             link = Link(short_code=short_code, original_url=original_url)
#             db.session.add(link)
#             db.session.commit()
#             short_url = short_code

#         except Exception as e:
#             db.session.rollback()
#             flash("Something went wrong while saving URL", "error")

#     return render_template('index.html', short_url=short_url)


# ===> Redirect Logic

@bp.route('/<short_code>')
def redirect_to_url(short_code):
    from app.models import Link
    # Search the database for this specific 1-char code
    # .first() bcz 'short_code'=unique

    link = Link.query.filter_by(short_code=short_code).first()

    if link:
        # if found, then redirect to original_orl
        # Link.times_visited += 1
        link.clicks +=1
        db.session.commit()
        return redirect(link.original_url)
    
    #if not, then don't exist
    flash("Sorry, that short link doesn't exist!", "error")
    return redirect('/')
