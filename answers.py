import math
from db import db


def get_by_user(user_id):
    sql = "select count(answers.id), answers.correct, answers.user_id from answers \
        group by answers.correct, answers.user_id \
            having answers.user_id = :user_id"
    result = db.session.execute(sql, {
        "user_id": user_id})
    return result.fetchall()


def get_by_course(user_id, course_id):
    sql = "select count(answers.id) as count, answers.correct, answers.course_id, answers.user_id, \
        courses.subject from answers \
        join courses on courses.id = answers.course_id \
            group by answers.correct, answers.course_id, answers.user_id, courses.subject \
                having answers.course_id = :course_id and answers.user_id = :user_id"
    result = db.session.execute(sql, {
        "course_id": course_id, 
        "user_id": user_id})
    return result.fetchall()


def count_correct(answers):
    count = 0
    for answer in answers:
        if answer.correct:
            count = answer.count
    return count


def count_incorrect(answers):
    count = 0
    for answer in answers:
        if not answer.correct:
            count = answer.count
    return count


def get_success_rate(correct, incorrect):
    answers_total = correct + incorrect
    if answers_total != 0:
        return math.floor(correct / answers_total * 100)
    return 0


def add(user_id, question_id, course_id, is_correct):
    try:
        sql = "insert into answers (user_id, question_id, course_id, answered, correct) \
            values (:user_id, :question_id, :course_id, NOW(), :is_correct)"
        db.session.execute(sql, {
            "user_id":user_id, 
            "question_id":question_id, 
            "course_id":course_id, 
            "is_correct":is_correct})
        db.session.commit()
    except:
        return  False
    return True


def get_correct(user_id):
    sql = "select question_id from answers \
        where user_id = :user_id and correct = true"
    result = db.session.execute(sql, {
        "user_id": user_id})
    return result.fetchall()


def count_recent(user_id):
    sql = "select count(answers.id) from answers \
        where user_id = :user_id and answered > now() - interval '30 minute'"
    result = db.session.execute(sql, {
        "user_id":user_id})
    return result.fetchone()
