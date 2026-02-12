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
        return redirect(url_for('admin.admin_dashboard'))
    
    short_url = None

    if request.method == 'POST':
        original_url = request.form.get('url')
        edit_id = request.form.get('edit_id')

        if not original_url:
            flash('URL is required', 'error')
            return redirect(url_for('main.dashboard'))

        # ========= UPDATE MODE =========
        if edit_id:
            try:
                link = Link.query.get_or_404(edit_id)
                link.original_url = original_url
                link.clicks = 0  # reset clicks on update
                db.session.commit()
                flash("Short link updated successfully!", "success")
                return redirect(url_for('main.dashboard'))
            except Exception as e:
                db.session.rollback()
                flash("Error updating URL", "error")
                return redirect(url_for('main.dashboard'))

        # ========= CREATE MODE =========
        short_code = ''.join(random.choice(CHAR_POOL) for _ in range(3))
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

    # ===== Normal Pagination =====

    page = request.args.get("page", 1, type=int)
    per_page = 10

    # base query for current user's links
    query = Link.query.filter_by(user_id=current_user.id).order_by(Link.created_at.desc(), Link.id.desc())

    # paginate using SQLAlchemy
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    links = pagination.items

    # calculate serial number start
    start_index = (page - 1) * per_page + 1
    end_index = start_index + len(links) - 1
    total_links = pagination.total

    return render_template(
        "dashboard.html",
        links=links,
        page=page,
        total_pages=pagination.pages,
        start_index=start_index,
        end_index=end_index,
        total_links=total_links
    )
    # return render_template('dashboard.html', links=links)


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

# ==> Profile Page <== 

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
