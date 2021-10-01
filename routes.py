from flask import redirect, render_template, request, session, abort
from app import app
from db import db
import users
import math


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
    if request.method == "GET" and users.user_id() == 0:
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")
    return render_template("error.html", message="Toiminto ei ole sallittu.")


@app.route("/logout")
def logout():
    if users.logout():
        return redirect("/")
    return render_template("error.html", message="Uloskirjautuminen ei onnistunut.")


@app.route("/courses/")
def courses():
    sql = "select courses.id, courses.teacher_id, courses.subject, courses.description, courses.exercises, \
        users.first_name, users.last_name from courses \
        left join users on courses.teacher_id = users.id"
    result = db.session.execute(sql)
    courses_list = result.fetchall()
    return render_template("courses.html", courses=courses_list)


@app.route("/profile/<int:id>")
def profile(id):
    correct_answers = 0
    incorrect_answers = 0
    success_rate = 0
    user_id = users.user_id()
    username = users.username()
    allow = False
    if users.is_admin():
        allow = True
    elif users.user_id() == id:
        allow = True
    if not allow:
        return render_template("error.html", message="Pääsy kielletty.")
    elif users.is_teacher():
        sql = "select courses.id, courses.subject, courses.description, courses.exercises from courses where courses.teacher_id = :user_id"
        result = db.session.execute(sql, {"user_id": user_id})
        users_courses = result.fetchall()
    else:
        sql = "select courses.id, courses.subject, courses.description, courses.exercises, enrollments.course_id from courses join enrollments on enrollments.course_id = courses.id where enrollments.user_id = :user_id"
        result = db.session.execute(sql, {"user_id": user_id})
        users_courses = result.fetchall()
        sql = "select count(answers.id), answers.correct, answers.user_id from answers group by answers.correct, answers.user_id having answers.user_id = :user_id"
        result = db.session.execute(sql, {"user_id": user_id})
        answers = result.fetchall()
        for answer in answers:
            if answer.correct:
                correct_answers = answer.count
            else:
                incorrect_answers = answer.count
        answers_total = correct_answers + incorrect_answers
        success_rate = math.floor(correct_answers / answers_total * 100)
    return render_template("profile.html", user=user_id, username=username, courses=users_courses, is_user=users.is_user(), is_teacher=users.is_teacher(), is_admin=users.is_admin(), correct=correct_answers, incorrect=incorrect_answers, success=success_rate)


@app.route("/answer/<int:id>", methods=["POST"])
def answer(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
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
    sql = "select courses.teacher_id, courses.subject, courses.description from courses where courses.id = :id"
    result = db.session.execute(sql, {"id": id})
    course = result.fetchone()
    teacher_id = course.teacher_id
    print("teacher_id ", teacher_id)
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
    return render_template("edit.html", questions=questions, id=id, words=words, definitions=definitions, course=course)


@app.route("/course/<int:id>/edit/add", methods=["GET", "POST"])
def add(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    lemma = request.form["lemma"]
    inflection = request.form["inflection"]
    definition = request.form["definition"]
    lemma_id = 0
    if 1 < len(lemma) < 51 and 1 < len(inflection) < 51 and len(definition) < 51:
        try:
            sql = "select words.id from words where words.lemma = :lemma"
            result = db.session.execute(sql, {"lemma": lemma})
            lemma_id = result.fetchone()[0]
        except:
            sql = "insert into words (lemma) values (:lemma) returning id"
            result = db.session.execute(sql, {"lemma": lemma})
            db.session.commit()
            lemma_id = result.fetchone()[0]
    else:
        return render_template("error.html", message="Syötteen täytyy olla 2 - 50 merkkiä pitkä.")
    sql = "select definitions.id from definitions where definitions.definition = :definition"
    result = db.session.execute(sql, {"definition": definition})
    definition_id = result.fetchone()[0]
    sql = "insert into questions (course_id, word_id, definition_id, inflection) \
        values (:id, :lemma_id, :definition_id, :inflection)"
    db.session.execute(sql, {"id": id, "lemma_id": lemma_id,
                       "definition_id": definition_id, "inflection": inflection})
    db.session.commit()
    sql = "update courses set exercises = exercises + 1 where courses.id = :id"
    db.session.execute(sql, {"id": id})
    db. session.commit()
    return redirect("/course/" + str(id) + "/edit")


@app.route("/course/<int:id>/edit/change", methods=["POST"])
def change(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    subject = request.form["subject"]
    description = request.form["description"]
    if len(subject) > 50 or len(description) > 200:
        return render_template("error.html", message="Syöte saa olla enintään 50 merkkiä pitkä.")
    if subject != '' and description == '':
        sql = "update courses set subject = :subject where id = :id"
        db.session.execute(sql, {"id": id, "subject": subject})
        db.session.commit()
    elif description != '' and subject == '':
        sql = "update courses set description = :description where id = :id"
        db.session.execute(sql, {"id": id, "description": description})
        db.session.commit()
    elif subject != '' and description != '':
        sql = "update courses set description = :description, subject = :subject where id = :id"
        db.session.execute(
            sql, {"id": id, "subject": subject, "description": description})
        db.session.commit()
    return redirect("/course/" + str(id) + "/edit")


@app.route("/course/<int:id>/statistics/<int:user>")
def statistics(id, user):
    sql = "select count(answers.id) as count, answers.correct, answers.course_id, answers.user_id, courses.subject from answers join courses on courses.id = answers.course_id group by answers.correct, answers.course_id, answers.user_id, courses.subject having answers.course_id = :id and answers.user_id = :user"
    result = db.session.execute(sql, {"id": id, "user": user})
    answers = result.fetchall()
    correct_answers = 0
    incorrect_answers = 0
    for answer in answers:
        if answer.correct:
            correct_answers = answer.count
        else:
            incorrect_answers = answer.count
    answers_total = correct_answers + incorrect_answers
    success_rate = math.floor(correct_answers / answers_total * 100)
    subject = answers[0].subject
    return render_template("statistics.html", course=id, user=user, correct=correct_answers, incorrect=incorrect_answers, success=success_rate, subject=subject)


@app.route("/course/<int:id>/enroll")
def enroll(id):
    user_id = users.user_id()
    sql = "select enrollments.id from enrollments \
        where user_id = :user_id and course_id = :id"
    result = db.session.execute(sql, {"user_id": user_id, "id": id})
    enrolled = result.fetchone()
    if enrolled:
        return render_template("error.html", message="Olet jo ilmoittautunut tälle kurssille.")
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

# TODO
# etusivulle jotain uusimmat tapahtumat tms.
# tietojen poistaminen: käyttäjätunnus, kurssi, kurssin tehtävä
# kurssille kenttä, joka kertoo luokan (esim. nominien taivutus, verbien taivutus), ja/tai ehkä asiasanoja?
# placeholderit lomakekenttiin
