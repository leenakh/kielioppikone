from db import db


def get_courses():
    sql = "select courses.id, courses.teacher_id, courses.subject, courses.description, courses.exercises, \
        users.first_name, users.last_name from courses \
        left join users on courses.teacher_id = users.id"
    result = db.session.execute(sql)
    courses_list = result.fetchall()
    return courses_list


def get_course(id):
    sql = "select courses.teacher_id, courses.subject, courses.description from courses where courses.id = :id"
    result = db.session.execute(sql, {"id": id})
    course = result.fetchone()
    return course


def get_teacher(course_id):
    sql = "select courses.teacher_id from courses where id = :course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchone()[0]


def get_teachers_courses(user_id):
    sql = "select courses.id, courses.subject, courses.description, courses.exercises from courses where courses.teacher_id = :user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()


def get_users_courses(user_id):
    sql = "select courses.id, courses.subject, courses.description, courses.exercises, enrollments.course_id from courses join enrollments on enrollments.course_id = courses.id where enrollments.user_id = :user_id"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()


def update_exercise_count(course_id, operation):
    if operation == "increment":
        try:
            sql = "update courses set exercises = exercises + 1 where courses.id = :course_id"
            db.session.execute(sql, {"course_id": course_id})
            db. session.commit()
        except:
            return False
    elif operation == "reduce":
        try:
            sql = "update courses set exercises = exercises - 1 where courses.id = :course_id"
            db.session.execute(sql, {"course_id": course_id})
            db. session.commit()
        except:
            return False
    else:
        return False
    return True


def update_subject(id, subject):
    try:
        sql = "update courses set subject = :subject where id = :id"
        db.session.execute(sql, {"id": id, "subject": subject})
        db.session.commit()
    except:
        return False
    return True


def update_description(id, description):
    try:
        sql = "update courses set description = :description where id = :id"
        db.session.execute(sql, {"id": id, "description": description})
        db.session.commit()
    except:
        return False
    return True


def update_course_info(id, subject, description):
    if subject != '' and description == '':
        if not update_subject(id, subject):
            return False
    elif description != '' and subject == '':
        if not update_description(id, description):
            return False
    elif subject != '' and description != '':
        try:
            sql = "update courses set description = :description, subject = :subject where id = :id"
            db.session.execute(sql, {"id": id, "subject": subject, "description": description})
            db.session.commit()
        except:
            return False
    return True
