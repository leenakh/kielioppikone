from flask import redirect, render_template, request
from app import app
from db import db
import users


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää.")
        if users.register(username, password1, 'user', first_name, last_name):
            return redirect("/")
        return render_template("error.html", message="Rekisteröinti ei onnistunut.")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")


@app.route("/logout")
def logout():
    if users.logout():
        return redirect("/")
    return render_template("error.html", message="Uloskirjautuminen ei onnistunut.")


@app.route("/profile/<int:id>")
def profile(id):
    user_id = users.user_id()
    username = users.username()
    allow = False
    if users.is_admin():
        allow = True
    elif users.user_id() == id:
        allow = True
    if not allow:
        return render_template("error.html", message="Pääsy kielletty.")
    if users.is_teacher:
        sql = "select courses.id, courses.subject, courses.description from courses where courses.teacher_id = :user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        courses = result.fetchall()
    return render_template("profile.html", user_id=user_id, username=username, courses=courses)


@app.route("/courses/")
def courses():
    sql = "select courses.id, courses.teacher_id, courses.subject, \
        users.first_name, users.last_name from courses \
        left join users on courses.teacher_id = users.id"
    result = db.session.execute(sql)
    courses_list = result.fetchall()
    return render_template("courses.html", courses=courses_list)


@app.route("/answer/<int:id>", methods=["POST"])
def answer(id):
    current_answer = request.form["answer"]
    correct = request.form["correct"]
    current_course = request.form["course"]
    is_correct = True
    user_id = users.user_id()
    if current_answer != correct:
        is_correct = False
    try:
        sql = "insert into answers (user_id, question_id, course_id, answered, correct) \
            values (:user_id, :question_id, :course_id, NOW(), :is_correct)"
        db.session.execute(sql, {"user_id": user_id, "question_id": id,
                           "course_id": current_course, "is_correct": is_correct})
        db.session.commit()
    except:
        return render_template("error.html", message='Vastauksen lähettäminen ei onnistunut.')
    return render_template("answer.html", answer=current_answer, id=id, correct=correct, course=current_course)


@app.route("/course/<int:id>")
def course(id):
    user_id = users.user_id()
    sql = "select enrollments.id from enrollments \
        where user_id = :user_id and course_id = :id"
    result = db.session.execute(sql, {"user_id": user_id, "id": id})
    enrolled = result.fetchone()
    if not enrolled:
        return render_template("error.html", message='Ilmoittaudu kurssille')
    sql = "select questions.id from questions where questions.course_id = :id"
    result = db.session.execute(sql, {"id": id})
    questions = result.fetchall()
    sql = "select question_id from answers where user_id = :user_id and correct = true"
    result = db.session.execute(sql, {"user_id": user_id})
    correct_answers = result.fetchall()
    return render_template("course.html", questions=questions, correct_answers=correct_answers)


@app.route("/course/<int:id>/edit")
def edit(id):
    user_id = users.user_id()
    sql = "select courses.teacher_id from courses where courses.id = :id"
    result = db.session.execute(sql, {"id":id})
    teacher_id = result.fetchone()[0]
    if user_id != teacher_id:
        return render_template("error.html", message='Pääsy kielletty.')
    sql = "select questions.inflection, questions.course_id, words.lemma from questions join words on questions.word_id = words.id where questions.course_id = :id"
    result = db.session.execute(sql, {"id": id})
    questions = result.fetchall()
    sql = "select words.lemma from words"
    result = db.session.execute(sql)
    words = result.fetchall()
    sql = "select definitions.definition from definitions"
    result = db.session.execute(sql)
    definitions = result.fetchall()
    if user_id == 1:
        return render_template("edit.html", questions=questions, id=id, words=words, definitions=definitions)

@app.route("/course/<int:id>/edit/add", methods=["GET", "POST"])
def add(id):
    lemma = request.form["lemma"]
    print("lemma ", lemma)
    inflection = request.form["inflection"]
    definition = request.form["definition"]
    sql = "select words.id from words where words.lemma = :lemma"
    result = db.session.execute(sql, {"lemma":lemma})
    #if not result.fetchone():
    #   sql = "insert into words (lemma) values (:lemma)"
    #    db.session.execute(sql, {"lemma":lemma})
    #    db.session.commit()
    #    sql = "select words.id from words where words.lemma = :lemma"
    #    result = db.session.execute(sql, {"lemma":lemma})
    #    lemma_id = result.fetchone()[0]
    #    print("newlemma", lemma_id)
    #elif result.fetchone():
    lemma_id = result.fetchone()[0]
    print ("lemma_id ", lemma_id)
    sql = "select definitions.id from definitions where definitions.definition = :definition"
    result = db.session.execute(sql, {"definition":definition})
    definition_id = result.fetchone()[0]
    print("definition ", definition_id)
    sql = "insert into questions (course_id, word_id, definition_id, inflection) \
        values (:id, :lemma_id, :definition_id, :inflection)"
    db.session.execute(sql, {"id":id, "lemma_id":lemma_id, "definition_id":definition_id, "inflection":inflection})
    db.session.commit()
    return redirect("/course/" + str(id) + "/edit")

@app.route("/course/<int:id>/enroll")
def enroll(id):
    user_id = users.user_id()
    try:
        sql = "insert into enrollments (user_id, course_id, entered) \
            values (:user_id, :course_id, NOW())"
        db.session.execute(sql, {"course_id": id, "user_id": user_id})
        db.session.commit()
    except:
        return render_template("error.html", message='Ilmoittautuminen ei onnistunut.')
    return redirect("/course/" + str(id))


@app.route("/course/<int:id>/confirm")
def confirm(id):
    message = 'Haluatko varmasti ilmoittautua kurssille?'
    return render_template("confirm.html", message=message, id=id)


@app.route("/question/<int:id>")
def question(id):
    sql = "select definitions.definition, words.lemma, questions.inflection, questions.course_id, questions.id \
        from questions \
        inner join definitions on questions.definition_id = definitions.id \
        inner join words on words.id = questions.word_id \
        where questions.id = :id"
    result = db.session.execute(sql, {"id": id})
    current_question = result.fetchone()
    return render_template("question.html", question=current_question)


@app.route("/frame")
def frame():
    return render_template("frame.html")
