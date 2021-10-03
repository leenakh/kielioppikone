from db import db


def enrolled(user_id, course_id):
    sql = "select enrollments.id from enrollments \
        where user_id = :user_id and course_id = :course_id"
    result = db.session.execute(sql, {"user_id": user_id, "course_id": course_id})
    return result.fetchone()


def enroll(user_id, course_id):
    try:
        sql = "insert into enrollments (user_id, course_id, entered) \
            values (:user_id, :course_id, NOW())"
        db.session.execute(sql, {"course_id": course_id, "user_id": user_id})
        db.session.commit()
    except:
        return False
    return True


