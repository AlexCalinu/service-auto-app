# Service Auto App

Aplicatie web in Python pentru evidenta unui service auto mic. Include clienti, masini, lucrari, istoric interventii, cautare rapida dupa numarul de inmatriculare si autentificare simpla.

> Web app (Flask + SQLAlchemy) for managing a small car repair shop: clients, cars, repair jobs, service history, plate search and login.

![Dashboard](screenshots/dashboard.png)

| Istoric masina | Versiune mobil |
|---|---|
| ![Istoric masina](screenshots/istoric-masina.png) | <img src="screenshots/mobil.png" width="260"> |

## Tehnologii

- Python
- Flask
- SQLAlchemy prin Flask-SQLAlchemy
- SQLite pentru rulare locala
- PostgreSQL sau alta baza cloud prin variabila `DATABASE_URL`
- HTML, CSS, Bootstrap si Jinja2

## Instalare

Intra in folderul proiectului:

```bash
cd service_auto_app
```

Creeaza un mediu virtual:

```bash
python -m venv venv
```

Activeaza mediul virtual pe Windows:

```bash
venv\Scripts\activate
```

Instaleaza dependentele:

```bash
pip install -r requirements.txt
```

## Pornire locala

```bash
python app.py
```

Aplicatia porneste pe:

```text
http://localhost:5000
```

La prima rulare se creeaza automat baza de date locala `service_auto.db`, utilizatorul demo si cateva date demonstrative.

## Date autentificare demo

```text
username: admin
parola: admin123
```

Parola este salvata hash-uit in baza de date, nu in text simplu.

## Baza de date cloud

Aplicatia foloseste `DATABASE_URL` daca variabila exista. Daca nu exista, foloseste SQLite local:

```text
sqlite:///service_auto.db
```

Exemplu pentru PostgreSQL:

```bash
set DATABASE_URL=postgresql://user:parola@host:5432/nume_baza
python app.py
```

Pe servicii cloud precum Render, Railway sau Heroku, variabila `DATABASE_URL` se seteaza in panoul de configurare al aplicatiei. Codul accepta si forma veche `postgres://`, pe care o transforma automat in `postgresql://`.

## Acces de pe telefon

Daca rulezi local pe aceeasi retea Wi-Fi, porneste aplicatia cu `python app.py`, apoi intra de pe telefon pe adresa IP a calculatorului:

```text
http://IP_CALCULATOR:5000
```

Exemplu:

```text
http://192.168.1.20:5000
```

Daca publici aplicatia online, o poti accesa direct din browserul telefonului folosind URL-ul public oferit de platforma cloud.

## Structura proiectului

```text
service_auto_app/
├── app.py
├── config.py
├── models.py
├── forms.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── clients.html
│   ├── client_form.html
│   ├── cars.html
│   ├── car_form.html
│   ├── repairs.html
│   ├── repair_form.html
│   ├── car_details.html
│   └── search_results.html
└── static/
    ├── style.css
    └── script.js
```

## Ce face fiecare parte

- `app.py` contine aplicatia Flask, rutele, autentificarea, CRUD-ul si initializarea datelor demo.
- `config.py` alege baza de date: `DATABASE_URL` pentru cloud sau SQLite local.
- `models.py` defineste modelele `User`, `Client`, `Car`, `Repair` si relatiile dintre ele.
- `forms.py` contine liste si functii simple pentru statusuri, date si costuri.
- `templates/` contine paginile HTML Jinja2.
- `static/style.css` contine designul responsive.
- `static/script.js` calculeaza costul total in formular si confirma stergerile.

## Functionalitati

- Dashboard cu total clienti, masini si lucrari.
- Afisare lucrari cu status `In lucru`.
- CRUD pentru clienti, masini si lucrari.
- Cautare rapida dupa numar de inmatriculare.
- Pagina de detalii pentru fiecare masina, cu istoricul interventiilor.
- Actualizare rapida a statusului unei lucrari.
- Interfata responsive cu Bootstrap.
- Login simplu cu parola hash-uita.
