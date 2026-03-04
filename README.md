# 🔗 Bitly Clone – URL Shortener with Authentication 

A full-stack URL shortener web application inspired by Bitly, built using **Python, Flask, PostgreSQL, SQLAlchemy, Jinja2, and Tailwind CSS**.  
The app supports **user authentication**, **short-link tracking**, and a **personal dashboard** to manage URLs.

---

## TODOs

- pagination
    - server based
        - cursor based
        - normal
    - client based
- super admin
- admin (ORG) i.e CDA
    - Haron
    - Usman 
- RBAC / ABAC
- flask compress and minify 
- middleware
- regex 
- sort by: (filter on table headers)



## 🚀 Features

- 🔐 User Authentication (Sign up / Login / Logout)
- ✉️ Email-based user accounts
- 🔗 Short URL generation (3-character - Random based)
- 📊 Click tracking for each shortened link
- 👤 User-specific dashboards
- 🔒 Protected routes (only logged-in users can manage links)
- 🎨 Responsive UI using Tailwind CSS
- 🗄 PostgreSQL database with Alembic migrations

---

## 🧱 Tech Stack

| Layer        | Technology |
|-------------|------------|
| Backend     | Python, Flask |
| Database    | PostgreSQL |
| ORM         | SQLAlchemy |
| Migrations  | Flask-Migrate (Alembic) |
| Frontend    | HTML, Jinja2, Tailwind CSS |
| Auth        | Flask-Login |
| Versioning  | Git & GitHub |

---

## 📁 Project Structure

```
bitly_clone/
│
├── app/
│   ├── controllers/
│   │   ├── __init__.py      # App factory (controllers)
│   │   ├── admin.py         # Admin routes
│   │   ├── auth.py          # Authentication routes
│   │   └── routes.py        # Dashboard & redirect routes
│   │
│   ├── templates/
│   │   ├── admin_dashboard.html
│   │   ├── admin_user_links.html
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── dashboard.html
│   │
│   ├── models.py            # User & Link models
│   ├── __init__.py          # App factory
│
├── migrations/              # Alembic migrations
├── config.py                # App configuration
├── run.py                   # Entry point
├── requirements.txt         # Project requirements
├── .gitignore
└── README.md
```

---

## 🧪 How It Works

1. User signs up using email & password
2. User logs in and accesses the dashboard
3. Shortens URLs from the dashboard
4. Each short link tracks click count
5. Redirects increment clicks uniquely per click 

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/mananurrehman/bitly_clone.git
cd bitly_clone
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment

Update `config.py` with your PostgreSQL database URL.

Example:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/bitly_clone"
```

---

### 5️⃣ Initialize Database
```bash
flask db init
flask db migrate
flask db upgrade
```

---

### 6️⃣ Run Application
```bash
python run.py
```

Visit:
```
http://127.0.0.1:5000
```

---

## 🔐 Security Notes

- Passwords are hashed securely
- Sessions manage authentication state
- Users can only view/manage their own links

---

## 📌 Future Improvements

- 🔗 Custom short URLs
- 📈 Advanced analytics (daily / monthly clicks)  
- ⏳ Link expiration  
- 📋 Copy-to-clipboard button   
- 🐳 Docker support  
- ☁️ Cloud deployment (AWS / Render / Railway)

---

## 👨‍💻 Author

Built by **Manan ur Rehman**  
Learning by building real-world backend systems.

---

## ⭐ Support

If you like this project:
- ⭐ Star the repo
- 🍴 Fork it
- 🧠 Improve it

Happy Coding! 🚀
