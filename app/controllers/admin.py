from flask import Blueprint, render_template, request, redirect, flash, url_for,abort
from flask_login import login_required, current_user
from app.models import Link, User
import random
import string
from app import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

CHAR_POOL = string.digits + string.ascii_lowercase + string.ascii_uppercase  # + ['-','_','+']

@admin.route('/', methods=['GET','POST'])
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
            return redirect(url_for('admin.admin_dashboard'))

        # ========= UPDATE MODE (ALREADY EXISTING) =========
        if edit_id:
            try:
                link = Link.query.get_or_404(edit_id)

                link.original_url = original_url
                link.clicks = 0   # reset clicks on update

                db.session.commit()
                flash("Short link updated successfully!", "success")
                return redirect(url_for('admin.admin_dashboard'))

            except Exception as e:
                db.session.rollback()
                flash("Error updating URL", "error")
                return redirect(url_for('admin.admin_dashboard'))

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
            return redirect(url_for('admin.admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            print(e)
            flash(f"Error saving URL {e}",'error')
            return redirect(url_for('admin.admin_dashboard'))

    links = (
        Link.query
        .filter_by(user_id=current_user.id)
        .order_by(Link.created_at.desc())
        .all()
    )
    return render_template('admin_dashboard.html', links=links)

# ====> ADMIN: VIEW ALL USERS & THEIR LINKS <==== 
@admin.route('/users', methods=['GET'])
@login_required
def admin_user_links():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('main.dashboard'))

    try:
        # Get user_id from query string and convert to int
        select_user_id = request.args.get('user_id', type=int)
        all_users = User.query.all()

        # Query user by id if provided, else get all users
        if select_user_id:
            users = User.query.filter(User.id == select_user_id).all()
        else:
            users = all_users

        return render_template(
            'admin_user_links.html',
            users=users,
            all_users=all_users,
            select_user_id=select_user_id
        )
    except Exception as e:
        print(f"Error fetching users: {e}")
        return abort(404)
