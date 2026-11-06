from datetime import date

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(150))
    notes = db.Column(db.Text)

    cars = db.relationship("Car", back_populates="client", cascade="all, delete-orphan")


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(30), unique=True, nullable=False, index=True)
    vin = db.Column(db.String(50))
    engine = db.Column(db.String(100))

    client = db.relationship("Client", back_populates="cars")
    repairs = db.relationship("Repair", back_populates="car", cascade="all, delete-orphan")

    @property
    def display_name(self):
        return f"{self.license_plate} - {self.make} {self.model}"


class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=False)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    problem = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text)
    work_done = db.Column(db.Text)
    parts_changed = db.Column(db.Text)
    parts_cost = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    labor_cost = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    status = db.Column(db.String(40), nullable=False, default="In asteptare")
    completion_date = db.Column(db.Date)
    notes = db.Column(db.Text)

    car = db.relationship("Car", back_populates="repairs")

    @property
    def total_cost(self):
        return (self.parts_cost or 0) + (self.labor_cost or 0)
