from flask import Flask, render_template, request, redirect, url_for
from extensions import db, migrate
from model import Food, Date
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate.init_app(app, db)


@app.context_processor
def utility():
    def covert_date_to_text(date):
        text = date.strftime("%B %d, %Y")
        return text
    return dict(convert_date_to_text=covert_date_to_text)


@app.context_processor
def utility_1():
    def sum_of_food_class(attribute, list_of_food):
        total = sum([getattr(x, attribute)for x in list_of_food])
        if total != 0:
            return total
        return None

    return dict(sum_of_food_class=sum_of_food_class)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        date_list = Date.query.order_by(Date.date.desc()).all()

        return render_template("home.html", date_list=date_list)

    else:
        day = request.form.get("new-day")
        new_date = Date(date=day)
        db.session.add(new_date)
        db.session.commit()

    return redirect(url_for("home"))


@app.route("/day/<int:date_id>", methods=["GET", "POST"])
def day(date_id):
    if request.method == "GET":
        date = Date.query.filter_by(id=date_id).first()
        list_of_food = Food.query.all()
        # protein = sum([food.protein for food in date.foods])
        # print(protein)
        return render_template("day.html", date=date, list_of_food=list_of_food)
    else:
        food_id = request.form.get("food")
        food_item = Food.query.filter_by(id=food_id).first()
        date = Date.query.filter_by(id=date_id).first()
        date.foods.append(food_item)
        db.session.commit()
        return redirect(url_for('day', date_id=date_id))


@app.route("/food", methods=["GET", "POST"])
def food():
    if request.method == "GET":
        foods = Food.query.all()
        return render_template("add_food.html", foods=foods)

    else:
        food_name = request.form.get("food-name")
        protein = float(request.form.get("protein"))
        carb = float(request.form.get("carbohydrates"))
        fat = float(request.form.get("fat"))

        calories = (protein * 4) + (carb * 4) + (fat * 9)
        new_food = Food(name=food_name.lower(), protein=protein, carbohydrate=carb, fat=fat, calories=calories)
        db.session.add(new_food)
        db.session.commit()
        return redirect(url_for("food"))


if __name__ == '__main__':
    app.run(debug=True)