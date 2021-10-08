from flask import redirect, render_template, request, session, abort
from app import app
import users
import courses
import enrollments
import questions
import words
import definitions
import answers


def validate_token(token):
    if session["csrf_token"] != token:
        abort(403)


def valid_input(min_length, max_length, user_input):
    if min_length <= len(user_input) <= max_length:
        return True
    return False


@app.template_filter()
def format(date):
    date_parts = str(date).split(" ")
    date_parts_final = date_parts[0].split("-")
    day = date_parts_final[2]
    month = date_parts_final[1]
    year = date_parts_final[0]
    return day + "." + month + "." + year


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
            return render_template("error.html", message="Salasanat eivät täsmää.", back="/register")
        if users.register(username, password1, 'user', first_name, last_name):
            return redirect("/")
        return render_template("error.html", message="Rekisteröinti ei onnistunut.", back="/register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET" and users.user_id() == 0:
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana", back="/")
    return render_template("error.html", message="Toiminto ei ole sallittu.", back="/")


@app.route("/logout")
def logout():
    if users.logout():
        return redirect("/")
    return render_template("error.html", message="Uloskirjautuminen ei onnistunut.", back="/")


@app.route("/courses/", methods=["GET", "POST"])
def get_courses():
    if request.method == "POST":
        search = request.form["search"]
        courses_list = courses.get_by_search(search)
    else:
        courses_list = courses.get_courses()
    return render_template("courses.html", courses=courses_list)


@app.route("/profile/<int:id>")
def profile(id):
    if not users.logged_in():
        return redirect("/login")
    correct_answers = 0
    incorrect_answers = 0
    success_rate = 0
    user_id = users.user_id()
    allow = False
    if users.is_admin():
        allow = True
    elif users.owner_of(id):
        allow = True
    if not allow:
        return render_template("error.html", message="Pääsy kielletty.", back="/profile/" + str(user_id))
    if users.is_teacher():
        users_courses = courses.get_teachers_courses(user_id)
    else:
        users_courses = courses.get_users_courses(user_id)
        users_answers = answers.get_by_user(user_id)
        correct_answers = answers.count_correct(users_answers)
        incorrect_answers = answers.count_incorrect(users_answers)
        success_rate = answers.get_success_rate(correct_answers, incorrect_answers)
    return render_template("profile.html", user=user_id, courses=users_courses, is_user=users.is_user(), is_teacher=users.is_teacher(), is_admin=users.is_admin(), correct=correct_answers, incorrect=incorrect_answers, success=success_rate)


@app.route("/answer/<int:id>", methods=["POST"])
def answer(id):
    validate_token(request.form["csrf_token"])
    current_answer = request.form["answer"]
    correct = request.form["correct"]
    current_course = request.form["course"]
    is_correct = True
    user_id = users.user_id()
    if current_answer != correct:
        is_correct = False
    if not answers.add(user_id, id, current_course, is_correct):
        return render_template("error.html", message='Vastauksen lähettäminen ei onnistunut.', back="/course/" + str(current_course))
    return render_template("answer.html", answer=current_answer, id=id, correct=correct, course=current_course)


@app.route("/courses/add", methods=["POST"])
def add_course():
    validate_token(request.form["csrf_token"])
    user_id = users.user_id()
    subject = request.form["subject"]
    description = request.form["description"]
    if not valid_input(0, 50, subject) or not valid_input(0, 200, description):
        return render_template("error.html", message="Otsikko saa olla enintään 50 merkkiä ja kuvaus enintään 200 merkkiä pitkä.", back="/profile/" + str(user_id))
    if not courses.add(subject, description, user_id):
        return render_template("error.html", message="Kurssin lisääminen ei onnistunut.", back="/profile/" + str(user_id))
    return redirect("/profile/" + str(user_id))


@app.route("/course/<int:course_id>")
def course(course_id):
    user_id = users.user_id()
    if not enrollments.enrolled(user_id, course_id):
        return redirect("/course/" + str(course_id) + "/confirm")
    questions_list = questions.get_questions(course_id)
    correct_answers = answers.get_correct(user_id)
    return render_template("course.html", questions_list=questions_list, correct_answers=correct_answers)


@app.route("/course/<int:course_id>/pupils")
def pupils(course_id):
    user_id = users.user_id()
    teacher_id = courses.get_teacher(course_id)
    if not users.owner_of(teacher_id):
        return render_template("error.html", message="Pääsy kielletty.", back="/profile/" + str(user_id))
    pupils_list = courses.get_users(course_id)
    if not pupils:
        return render_template("error.html", message="Kurssin osallistujia ei löytynyt.", back="/profile/" + str(user_id))
    return render_template("pupils.html", pupils_list=pupils_list, course_id=course_id, user_id=user_id)


@app.route("/course/<int:course_id>/edit")
def edit(course_id):
    user_id = users.user_id()
    if not users.logged_in():
        return redirect("/login")
    course = courses.get_course(course_id)
    if not course:
        return render_template("error.html", message="Kurssia ei ole olemassa.", back="/profile/" + str(user_id))
    teacher_id = courses.get_teacher(course_id)
    if not users.owner_of(teacher_id):
        return render_template("error.html", message='Pääsy kielletty.', back="/profile/" + str(user_id))
    course_questions = questions.get_course_questions(course_id)
    words_list = words.get_all()
    definitions_list = definitions.get_all()
    return render_template("edit.html", course_questions=course_questions, exercises=len(course_questions), course_id=course_id, words=words_list, definitions=definitions_list, course=course)


@app.route("/course/<int:course_id>/edit/add", methods=["GET", "POST"])
def add(course_id):
    validate_token(request.form["csrf_token"])
    lemma = request.form["lemma"]
    inflection = request.form["inflection"]
    definition = request.form["definition"]
    lemma_id = 0
    if valid_input(2, 50, lemma) and valid_input(2, 50, inflection):
        try:
            lemma_id = words.get_id(lemma)
        except:
            lemma_id = words.add(lemma)
    else:
        return render_template("error.html", message="Syötteen täytyy olla 2 - 50 merkkiä pitkä.", back=request.referrer)
    definition_id = definitions.get_id(definition)
    if questions.add_question(course_id, lemma_id, definition_id, inflection):
        courses.update_exercise_count(course_id, "increment")
    return redirect("/course/" + str(course_id) + "/edit")


@app.route("/course/<int:id>/edit/change", methods=["POST"])
def change(id):
    validate_token(request.form["csrf_token"])
    subject = request.form["subject"]
    description = request.form["description"]
    if not valid_input(0, 50, subject) or not valid_input(0, 200, description):
        return render_template("error.html", message="Otsikko saa olla enintään 50 merkkiä ja kuvaus enintään 200 merkkiä pitkä.", back="/course/" + str(id) + "/edit")
    if not courses.update_course_info(id, subject, description):
        return render_template("error.html", message="Kurssin tietojen muuttaminen ei onnistunut.", back="/course/" + str(id) + "/edit")
    return redirect("/course/" + str(id) + "/edit")


@app.route("/course/<int:course_id>/remove")
def remove_course(course_id):
    user_id = users.user_id()
    teacher_id = courses.get_teacher(course_id)
    if not users.owner_of(teacher_id):
        return render_template("error.html", message="Pääsy kielletty.", back="/profile/" + str(user_id))
    if not courses.set_visible(course_id, False):
        return render_template("error.html", message="Kurssin piilottaminen ei onnistunut.", back="/course/" + str(course_id) + "/edit")
    return redirect("/profile/" + str(user_id))


@app.route("/course/<int:course_id>/restore")
def restore_course(course_id):
    user_id = users.user_id()
    teacher_id = courses.get_teacher(course_id)
    if not users.owner_of(teacher_id):
        return render_template("error.html", message="Pääsy kielletty.", back="/profile/" + str(user_id))
    if not courses.set_visible(course_id, True):
        return render_template("error.html", message="Kurssin palauttaminen ei onnistunut.", back="/course/" + str(course_id) + "/edit")
    return redirect("/profile/" + str(user_id))


@app.route("/course/<int:id>/statistics/<int:user>")
def statistics(id, user):
    user_id = users.user_id()
    if not users.logged_in():
        return redirect("/login")
    if not users.owner_of(user) and not users.owner_of(courses.get_teacher(id)):
        return render_template("error.html", message="Pääsy kielletty.", back="/profile/" + str(user_id))
    answers_list = answers.get_by_course(user, id)
    if not answers_list:
        return render_template("error.html", message="Et ole vielä vastannut yhteenkään tehtävään.", back="/profile/" + str(user_id))
    correct_answers = answers.count_correct(answers_list)
    incorrect_answers = answers.count_incorrect(answers_list)
    success_rate = answers.get_success_rate(correct_answers, incorrect_answers)
    subject = answers_list[0].subject
    return render_template("statistics.html", course=id, user=user, correct=correct_answers, incorrect=incorrect_answers, success=success_rate, subject=subject, back=request.referrer)


@app.route("/course/<int:course_id>/enroll")
def enroll(course_id):
    user_id = users.user_id()
    if not users.logged_in():
        return redirect("/login")
    if not enrollments.enroll(user_id, course_id):
        return render_template("error.html", message='Ilmoittautuminen ei onnistunut.', back="/profile/" + str(user_id))
    return redirect("/course/" + str(course_id))


@app.route("/course/<int:course_id>/confirm")
def confirm(course_id):
    user_id = users.user_id()
    if not users.logged_in():
        return redirect("/login")
    if enrollments.enrolled(user_id, course_id):
        return render_template("error.html", message="Olet jo ilmoittautunut tälle kurssille.", back="/courses")
    message = 'Haluatko ilmoittautua kurssille?'
    return render_template("confirm.html", message=message, id=course_id)


@app.route("/question/<int:question_id>")
def question(question_id):
    current_question = questions.get_question(question_id)
    return render_template("question.html", question=current_question)


@app.route("/course/<int:course_id>/question/<int:question_id>/remove")
def remove(course_id, question_id):
    if not users.logged_in():
        return redirect("/login")
    teacher_id = courses.get_teacher(course_id)
    if not users.owner_of(teacher_id):
        return render_template("error.html", message="Toiminto ei ole sallittu.", back="/")
    if not questions.remove_question(question_id):
        return render_template("error.html", message="Tehtävän poistaminen ei onnistunut.", back="/course/" + str(course_id) + "/edit")
    courses.update_exercise_count(course_id, "reduce")
    return redirect("/course/" + str(course_id) + "/edit")


@app.route("/frame")
def frame():
    return render_template("frame.html")
