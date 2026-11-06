import os
from datetime import date
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from config import Config
from forms import REPAIR_STATUSES, optional_text, parse_date, parse_decimal
from models import Car, Client, Repair, User, db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_demo_data()

    register_routes(app)
    return app


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user_id"):
            flash("Te rugam sa te autentifici.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def seed_demo_data():
    if not User.query.filter_by(username="admin").first():
        user = User(username="admin")
        user.set_password("admin123")
        db.session.add(user)

    if Client.query.first():
        db.session.commit()
        return

    client_1 = Client(
        name="Andrei Popescu",
        phone="0722 111 222",
        email="andrei.popescu@example.com",
        notes="Prefera programari dimineata.",
    )
    client_2 = Client(
        name="Maria Ionescu",
        phone="0744 333 444",
        email="maria.ionescu@example.com",
    )
    client_3 = Client(
        name="SC Livrari Rapid SRL",
        phone="0730 555 888",
        notes="Flota mica, facturare pe firma.",
    )

    car_1 = Car(
        client=client_1,
        make="Volkswagen",
        model="Golf",
        year=2015,
        license_plate="B123ABC",
        vin="WVWZZZAUZFW000001",
        engine="1.6 TDI",
    )
    car_2 = Car(
        client=client_2,
        make="Ford",
        model="Focus",
        year=2018,
        license_plate="IF45MIA",
        engine="1.0 EcoBoost",
    )
    car_3 = Car(
        client=client_3,
        make="Dacia",
        model="Dokker",
        year=2020,
        license_plate="B77RPD",
        engine="1.5 dCi",
    )

    repairs = [
        Repair(
            car=car_1,
            entry_date=date(2026, 5, 10),
            problem="Martor motor aprins si pornire greoaie.",
            diagnosis="Injector murdar si filtru combustibil infundat.",
            work_done="Curatare injector si inlocuire filtru combustibil.",
            parts_changed="Filtru combustibil",
            parts_cost=180,
            labor_cost=220,
            status="Finalizat",
            completion_date=date(2026, 5, 11),
        ),
        Repair(
            car=car_2,
            entry_date=date(2026, 6, 18),
            problem="Zgomot la franare.",
            diagnosis="Placutelor fata uzate peste limita.",
            work_done="Inlocuire placute frana fata.",
            parts_changed="Placute frana fata",
            parts_cost=260,
            labor_cost=160,
            status="In lucru",
        ),
        Repair(
            car=car_3,
            entry_date=date(2026, 6, 20),
            problem="Revizie periodica si verificare directie.",
            diagnosis="Se asteapta confirmarea pentru bielete.",
            parts_changed="Ulei, filtru ulei, filtru aer",
            parts_cost=390,
            labor_cost=250,
            status="Asteapta piese",
        ),
    ]

    db.session.add_all([client_1, client_2, client_3, car_1, car_2, car_3, *repairs])
    db.session.commit()


def register_routes(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                session.clear()
                session["user_id"] = user.id
                session["username"] = user.username
                flash("Autentificare reusita.", "success")
                return redirect(url_for("dashboard"))

            flash("Username sau parola incorecta.", "danger")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Ai iesit din cont.", "info")
        return redirect(url_for("login"))

    @app.route("/")
    @login_required
    def dashboard():
        latest_repairs = Repair.query.order_by(Repair.entry_date.desc(), Repair.id.desc()).limit(5).all()
        active_repairs = (
            Repair.query.filter(Repair.status == "In lucru")
            .order_by(Repair.entry_date.desc(), Repair.id.desc())
            .all()
        )
        return render_template(
            "dashboard.html",
            clients_count=Client.query.count(),
            cars_count=Car.query.count(),
            repairs_count=Repair.query.count(),
            active_repairs=active_repairs,
            latest_repairs=latest_repairs,
            statuses=REPAIR_STATUSES,
        )

    @app.route("/clients")
    @login_required
    def clients():
        items = Client.query.order_by(Client.name.asc()).all()
        return render_template("clients.html", clients=items)

    @app.route("/clients/add", methods=["GET", "POST"])
    @login_required
    def add_client():
        return save_client()

    @app.route("/clients/<int:client_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_client(client_id):
        client = Client.query.get_or_404(client_id)
        return save_client(client)

    def save_client(client=None):
        if request.method == "POST":
            if client is None:
                client = Client()

            client.name = request.form["name"].strip()
            client.phone = request.form["phone"].strip()
            client.email = optional_text(request.form.get("email"))
            client.notes = optional_text(request.form.get("notes"))

            db.session.add(client)
            db.session.commit()
            flash("Clientul a fost salvat.", "success")
            return redirect(url_for("clients"))

        return render_template("client_form.html", client=client)

    @app.route("/clients/<int:client_id>/delete", methods=["POST"])
    @login_required
    def delete_client(client_id):
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        flash("Clientul si datele asociate au fost sterse.", "info")
        return redirect(url_for("clients"))

    @app.route("/cars")
    @login_required
    def cars():
        items = Car.query.join(Client).order_by(Car.license_plate.asc()).all()
        return render_template("cars.html", cars=items)

    @app.route("/cars/add", methods=["GET", "POST"])
    @login_required
    def add_car():
        return save_car()

    @app.route("/cars/<int:car_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_car(car_id):
        car = Car.query.get_or_404(car_id)
        return save_car(car)

    def save_car(car=None):
        clients_list = Client.query.order_by(Client.name.asc()).all()
        if not clients_list:
            flash("Adauga mai intai un client.", "warning")
            return redirect(url_for("add_client"))

        if request.method == "POST":
            if car is None:
                car = Car()

            car.client_id = int(request.form["client_id"])
            car.make = request.form["make"].strip()
            car.model = request.form["model"].strip()
            car.year = int(request.form["year"])
            car.license_plate = request.form["license_plate"].strip().upper()
            car.vin = optional_text(request.form.get("vin"))
            car.engine = optional_text(request.form.get("engine"))

            db.session.add(car)
            try:
                db.session.commit()
                flash("Masina a fost salvata.", "success")
                return redirect(url_for("cars"))
            except Exception:
                db.session.rollback()
                flash("Numarul de inmatriculare exista deja sau datele nu sunt valide.", "danger")

        return render_template("car_form.html", car=car, clients=clients_list)

    @app.route("/cars/<int:car_id>/delete", methods=["POST"])
    @login_required
    def delete_car(car_id):
        car = Car.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        flash("Masina si istoricul ei au fost sterse.", "info")
        return redirect(url_for("cars"))

    @app.route("/cars/<int:car_id>")
    @login_required
    def car_details(car_id):
        car = Car.query.get_or_404(car_id)
        repairs = Repair.query.filter_by(car_id=car.id).order_by(Repair.entry_date.desc(), Repair.id.desc()).all()
        return render_template("car_details.html", car=car, repairs=repairs, statuses=REPAIR_STATUSES)

    @app.route("/repairs")
    @login_required
    def repairs():
        items = Repair.query.join(Car).order_by(Repair.entry_date.desc(), Repair.id.desc()).all()
        return render_template("repairs.html", repairs=items, statuses=REPAIR_STATUSES)

    @app.route("/repairs/add", methods=["GET", "POST"])
    @login_required
    def add_repair():
        return save_repair()

    @app.route("/repairs/<int:repair_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_repair(repair_id):
        repair = Repair.query.get_or_404(repair_id)
        return save_repair(repair)

    def save_repair(repair=None):
        cars_list = Car.query.order_by(Car.license_plate.asc()).all()
        if not cars_list:
            flash("Adauga mai intai o masina.", "warning")
            return redirect(url_for("add_car"))

        if request.method == "POST":
            if repair is None:
                repair = Repair()

            repair.car_id = int(request.form["car_id"])
            repair.entry_date = parse_date(request.form.get("entry_date")) or date.today()
            repair.problem = request.form["problem"].strip()
            repair.diagnosis = optional_text(request.form.get("diagnosis"))
            repair.work_done = optional_text(request.form.get("work_done"))
            repair.parts_changed = optional_text(request.form.get("parts_changed"))
            repair.parts_cost = parse_decimal(request.form.get("parts_cost"))
            repair.labor_cost = parse_decimal(request.form.get("labor_cost"))
            repair.status = request.form["status"]
            repair.completion_date = parse_date(request.form.get("completion_date"))
            repair.notes = optional_text(request.form.get("notes"))

            if repair.status == "Finalizat" and not repair.completion_date:
                repair.completion_date = date.today()

            db.session.add(repair)
            db.session.commit()
            flash("Lucrarea a fost salvata.", "success")
            return redirect(url_for("repairs"))

        return render_template("repair_form.html", repair=repair, cars=cars_list, statuses=REPAIR_STATUSES)

    @app.route("/repairs/<int:repair_id>/delete", methods=["POST"])
    @login_required
    def delete_repair(repair_id):
        repair = Repair.query.get_or_404(repair_id)
        db.session.delete(repair)
        db.session.commit()
        flash("Lucrarea a fost stearsa.", "info")
        return redirect(request.referrer or url_for("repairs"))

    @app.route("/repairs/<int:repair_id>/status", methods=["POST"])
    @login_required
    def update_repair_status(repair_id):
        repair = Repair.query.get_or_404(repair_id)
        status = request.form.get("status")
        if status in REPAIR_STATUSES:
            repair.status = status
            if status == "Finalizat" and not repair.completion_date:
                repair.completion_date = date.today()
            if status != "Finalizat":
                repair.completion_date = None
            db.session.commit()
            flash("Statusul lucrarii a fost actualizat.", "success")
        return redirect(request.referrer or url_for("repairs"))

    @app.route("/search")
    @login_required
    def search():
        plate = request.args.get("plate", "").strip()
        car = None
        repairs_list = []
        if plate:
            car = Car.query.filter(Car.license_plate.ilike(f"%{plate}%")).first()
            if car:
                repairs_list = (
                    Repair.query.filter_by(car_id=car.id)
                    .order_by(Repair.entry_date.desc(), Repair.id.desc())
                    .all()
                )
            else:
                flash("Nu am gasit nicio masina cu acest numar.", "warning")

        return render_template("search_results.html", plate=plate, car=car, repairs=repairs_list, statuses=REPAIR_STATUSES)


app = create_app()


if __name__ == "__main__":
    debug_enabled = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_enabled)
