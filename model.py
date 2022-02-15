from extensions import db

tags = db.Table("tags",
    db.Column("date_id", db.Integer, db.ForeignKey("date.id"), primary_key=True),
    db.Column("food_id", db.Integer, db.ForeignKey("food.id"), primary_key=True)
    )


class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    foods = db.relationship("Food", secondary="tags", lazy="subquery", backref=db.backref("dates", lazy=True))


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbohydrate = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)


