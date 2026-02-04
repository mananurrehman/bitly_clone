from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from app.models import Link, User
import random
import string
from app import db

bp = Blueprint('main', __name__)

# Pool for available character like IPs in DHCP Pool
CHAR_POOL = string.digits + string.ascii_lowercase + string.ascii_uppercase  # + ['-','_','+']

# ===== Simple User DASHBOARD ROUTE ======
@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    
    short_url = None

    if request.method == 'POST':
        original_url = request.form.get('url')
        edit_id = request.form.get('edit_id')

        if not original_url:
            flash('URL is required', 'error')
            return redirect(url_for('main.dashboard'))

        # ========= UPDATE MODE (ALREADY EXISTING) =========
        if edit_id:
            try:
                link = Link.query.get_or_404(edit_id)

                link.original_url = original_url
                link.clicks = 0   # reset clicks on update

                db.session.commit()
                flash("Short link updated successfully!", "success")
                return redirect(url_for('main.dashboard'))

            except Exception as e:
                db.session.rollback()
                flash("Error updating URL", "error")
                return redirect(url_for('main.dashboard'))

        # ========= CREATE MODE (NEW) =========

        # generate random short_code
        short_code = ''.join(random.choice(CHAR_POOL) for _ in range(3))

        # ensure unique short_code
        while Link.query.filter_by(short_code=short_code).first():
            short_code = ''.join(random.choice(CHAR_POOL) for _ in range(3))

        try:
            link = Link(
                short_code=short_code,
                original_url=original_url,
                user_id=current_user.id,
                clicks=0
            )

            db.session.add(link)
            db.session.commit()

            short_url = url_for(
                "main.redirect_to_url",
                short_code=short_code,
                _external=True
            )

            flash(f"Short link created: {short_url}", 'success')
            return redirect(url_for('main.dashboard'))

        except Exception as e:
            db.session.rollback()
            flash("Error saving URL", 'error')
            return redirect(url_for('main.dashboard'))

    links = (
        Link.query
        .filter_by(user_id=current_user.id)
        .order_by(Link.created_at.desc())
        .all()
    )

    return render_template('dashboard.html', links=links)


# ===> REDIRECT LOGIC - short_url (generated) <=====

@bp.route('/<short_code>')
def redirect_to_url(short_code):
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

# ==> Deleting short url and free the 3 char phrase against it

@bp.route('/delete/<int:id>', methods = ['POST'])
@login_required
def delete_link(id):
    link = Link.query.get_or_404(id)

    try:
        db.session.delete(link)
        db.session.commit()
        flash(f'Shrot URL Deleted & Short Code freed!', 'success')
    except:
        db.session.rollback()
        flash(f'Unable to delete short url', 'error')
    return redirect(url_for('main.dashboard'))

# ==> ADMIN DASHBOARD 
@bp.route('/admin', methods=['GET'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Access denied", 'error')
        return redirect(url_for('main.dashboard'))

    short_url = None

    if request.method == 'POST':
        original_url = request.form.get('url')
        edit_id = request.form.get('edit_id')

        if not original_url:
            flash('URL is required', 'error')
            return redirect(url_for('main.admin_dashboard'))

        # ========= UPDATE MODE (ALREADY EXISTING) =========
        if edit_id:
            try:
                link = Link.query.get_or_404(edit_id)

                link.original_url = original_url
                link.clicks = 0   # reset clicks on update

                db.session.commit()
                flash("Short link updated successfully!", "success")
                return redirect(url_for('main.admin_dashboard'))

            except Exception as e:
                db.session.rollback()
                flash("Error updating URL", "error")
                return redirect(url_for('main.admin_dashboard'))

        # ========= CREATE MODE (NEW) =========

        # generate random short_code
        short_code = ''.join(random.choice(CHAR_POOL) for _ in range(3))

        # ensure unique short_code
        while Link.query.filter_by(short_code=short_code).first():
            short_code = ''.join(random.choice(CHAR_POOL) for _ in range(3))

        try:
            link = Link(
                short_code=short_code,
                original_url=original_url,
                user_id=current_user.id,
                clicks=0
            )

            db.session.add(link)
            db.session.commit()

            short_url = url_for(
                "main.redirect_to_url",
                short_code=short_code,
                _external=True
            )

            flash(f"Short link created: {short_url}", 'success')
            return redirect(url_for('main.admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            flash("Error saving URL", 'error')
            return redirect(url_for('main.admin_dashboard'))

    links = (
        Link.query
        .filter_by(user_id=current_user.id)
        .order_by(Link.created_at.desc())
        .all()
    )
    return render_template('admin_dashboard.html', links=links)

# ====> ADMIN: VIEW ALL USERS & THEIR LINKS <==== 
@bp.route('/admin/users', methods=['GET'])
@login_required
def admin_user_links():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('main.dashboard'))
    
    users = User.query.filter(User.role != 'main').all()

    select_user_id = request.args.get('user_id')
    link = []

    if select_user_id:
        links = Link.query.filter_by(user_id=select_user_id).all()

    return render_template(
        'admin_user_links.html',
        users=users,
        links=links,
        select_user_id=select_user_id
    )