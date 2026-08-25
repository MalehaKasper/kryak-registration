import os
from functools import wraps

from flask import Flask, render_template, request, Response

import database

app = Flask(__name__)
database.init_db()

PROVID_TASKS = [
    "Точкування",
    "Економіка вишколу (ціни, податки, стипендії)",
    "Обслуговування застосунку/сервера",
    "Спонсори",
    "Супровід лекторів",
    "Інвентар",
    "Скарбник (реальний бюджет)",
    "Дизайн мерчу й коміксів",
    "Писар",
    "Координація харчування",
    "Легенда й програма — детально",
    "Фото/відеофіксація",
]

LECTURER_TALKS = [
    "Історія створення сучасних грошей",
    "Принцип роботи грошей",
    "Про інтернет-шахрайство",
    "Про «швидкий заробіток»",
    "Про заощадження",
    "Кредитні кошти та запозичення",
    "Види інвестицій",
    "Податки та державна власність",
    "Планова та ринкова економіка",
    "Планування витрат",
]


def check_auth(username, password):
    expected_user = os.environ.get("ADMIN_USER", "admin")
    expected_pass = os.environ.get("ADMIN_PASSWORD")
    if not expected_pass:
        # No credential configured on the server — fail closed, never allow open access.
        return False
    return username == expected_user and password == expected_pass


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                "Потрібна авторизація.",
                401,
                {"WWW-Authenticate": 'Basic realm="Admin"'},
            )
        return f(*args, **kwargs)

    return decorated


def _validate(name, telegram, phone):
    if not name:
        return "Вкажіть ім'я."
    if not telegram and not phone:
        return "Вкажіть хоча б один контакт — Telegram або телефон."
    return None


@app.route("/provid", methods=["GET"])
def provid_form():
    return render_template(
        "provid_form.html", tasks=PROVID_TASKS, values={}, error=None, submitted=False
    )


@app.route("/provid/submit", methods=["POST"])
def provid_submit():
    name = request.form.get("name", "").strip()
    telegram = request.form.get("telegram", "").strip()
    phone = request.form.get("phone", "").strip()
    idea = request.form.get("idea", "").strip()
    about = request.form.get("about", "").strip()
    tasks = request.form.getlist("task")

    error = _validate(name, telegram, phone)
    if error:
        values = {"name": name, "telegram": telegram, "phone": phone, "idea": idea, "about": about, "tasks": tasks}
        return render_template("provid_form.html", tasks=PROVID_TASKS, values=values, error=error, submitted=False)

    database.insert_provid_response(name, telegram, phone, tasks, idea, about)
    return render_template("provid_form.html", tasks=PROVID_TASKS, values={}, error=None, submitted=True)


@app.route("/lecturer", methods=["GET"])
def lecturer_form():
    return render_template(
        "lecturer_form.html", talks=LECTURER_TALKS, values={}, error=None, submitted=False
    )


@app.route("/lecturer/submit", methods=["POST"])
def lecturer_submit():
    name = request.form.get("name", "").strip()
    telegram = request.form.get("telegram", "").strip()
    phone = request.form.get("phone", "").strip()
    idea = request.form.get("idea", "").strip()
    about = request.form.get("about", "").strip()
    talks = request.form.getlist("task")

    error = _validate(name, telegram, phone)
    if error:
        values = {"name": name, "telegram": telegram, "phone": phone, "idea": idea, "about": about, "tasks": talks}
        return render_template("lecturer_form.html", talks=LECTURER_TALKS, values=values, error=error, submitted=False)

    database.insert_lecturer_response(name, telegram, phone, talks, idea, about)
    return render_template("lecturer_form.html", talks=LECTURER_TALKS, values={}, error=None, submitted=True)


@app.route("/provid/responses")
@requires_auth
def provid_responses():
    rows = database.get_provid_responses()
    columns = [
        ("created_at", "Час"),
        ("name", "Ім'я"),
        ("telegram", "Telegram"),
        ("phone", "Телефон"),
        ("tasks", "Завдання"),
        ("idea", "Ідея"),
        ("about", "Про себе"),
    ]
    return render_template("admin_list.html", title="Заявки в провід", columns=columns, rows=rows)


@app.route("/lecturer/responses")
@requires_auth
def lecturer_responses():
    rows = database.get_lecturer_responses()
    columns = [
        ("created_at", "Час"),
        ("name", "Ім'я"),
        ("telegram", "Telegram"),
        ("phone", "Телефон"),
        ("talks", "Гутірки"),
        ("own_topic", "Своя тема"),
        ("experience", "Досвід"),
    ]
    return render_template("admin_list.html", title="Зголошення лекторів", columns=columns, rows=rows)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
