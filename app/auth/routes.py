from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import authentication
from app.auth.forms import LoginForm, RegistrationForm, ScrapyForm
from app.auth.models import User
from bs4 import BeautifulSoup
from lxml import etree
import requests


@authentication.route("/register", methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        flash("You are already logged in the system")
        return redirect(url_for("authentication.homepage"))
    form = RegistrationForm()
    
    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.EMAIL.data,
            password=form.password.data,
        )
        flash("Registration successfully!!")
        return redirect(url_for("authentication.log_in_user"))
    return render_template("registration.html", form=form)

@authentication.route("/")
def index():
    return render_template("index.html")


@authentication.route("/login", methods=["GET","POST"])
def log_in_user():
    if current_user.is_authenticated:
        flash("You are already logged")
        return redirect(url_for("authentication.homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Invalid credentials")
            return redirect(url_for("authentication.log_in_user"))

        login_user(user, form.stay_loggedin.data)
        return redirect(url_for("authentication.homepage"))    
    return render_template("login.html", form=form)


@authentication.route("/homepage")
@login_required
def homepage():
    return render_template("homepage.html")


@authentication.route("/logout", methods=["GET"])
@login_required
def log_out_user():
    logout_user()
    return redirect(url_for("authentication.log_in_user"))
    

@authentication.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@authentication.route("/scrapy_data", methods=["GET","POST"])
@login_required
def scrapy_data():
    form = ScrapyForm()
    if form.validate_on_submit():
        search = form.search_article.data
        url = f"https://listado.mercadolibre.com.co/{search}#D[A:{search}]"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dom = etree.HTML(str(soup))
        # articles_data = dom.xpath("//ol[@class='ui-search-layout ui-search-layout--stack shops__layout']//div[@role='group']//a/@href")
        articles_data = dom.xpath("//ol[@class='ui-search-layout ui-search-layout--stack shops__layout']//div[@role='group']//a")
        links = []
        for article in articles_data:
            links.append({ "title": article.attrib.get('title', 'no'), "link": article.attrib.get('href', 'https://www.mercadolibre.com.co/')})
        
        data = {"links": links}
        return render_template("scrapy_data.html", **data)
    return render_template("scrapy_data.html", form=form)
