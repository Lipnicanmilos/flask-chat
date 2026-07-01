from datetime import datetime

from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from models import User, Post, Comment  # noqa: E402  (musí byť po vytvorení 'db')

with app.app_context():
    db.create_all()


def current_user_id():
    return session.get("id")


def login_required(view_func):
    from functools import wraps

    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "id" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped


@app.route("/")
def index():
    posts = Post.query.order_by(Post.created.desc()).paginate(per_page=5)
    return render_template("index.html", posts=posts)


@app.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    if request.method == "POST":
        post = Post(
            code=request.form.get("code"),
            text=request.form.get("text"),
            user_id=current_user_id(),
            created=datetime.now(),
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("new_post.html")


@app.route("/post/<int:id>", methods=["GET", "POST"])
def show_post(id):
    post = Post.query.filter_by(id=id).first_or_404()

    if request.method == "POST":
        if "id" not in session:
            return redirect(url_for("login"))

        text = request.form.get("text")
        if text:
            comment = Comment(
                text=text,
                user_id=current_user_id(),
                post_id=post.id,
                created=datetime.now(),
            )
            db.session.add(comment)
            db.session.commit()
        return redirect(url_for("show_post", id=post.id))

    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.created.desc()).all()
    return render_template("post.html", post=post, comments=comments)


@app.route("/post/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first_or_404()

    if post.user_id != current_user_id():
        return redirect(url_for("show_post", id=post.id))

    if request.method == "POST":
        post.text = request.form.get("text")
        post.code = request.form.get("code")
        db.session.commit()
        return redirect(url_for("show_post", id=post.id))

    return render_template("edit_post.html", post=post)


@app.route("/logout")
def logout():
    session.pop("name", None)
    session.pop("id", None)
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "id" in session:
        return redirect(url_for("index"))

    error = None

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["name"] = user.name
            session["id"] = user.id
            return redirect(url_for("index"))
        error = "Email alebo heslo je nesprávne."

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        existing = User.query.filter_by(email=email).first()

        if not name or not email or not password:
            error = "Vyplň všetky polia."
        elif password != password2:
            error = "Heslá nie sú rovnaké."
        elif len(password) < 6:
            error = "Heslo je príliš krátke (min. 6 znakov)."
        elif existing is not None:
            error = "Tento email je už registrovaný."
        else:
            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            session["name"] = user.name
            session["id"] = user.id
            return redirect(url_for("index"))

    return render_template("register.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)
