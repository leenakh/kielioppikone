from db import db


def get_questions(course_id):
    sql = "select questions.id from questions where questions.course_id = :course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()


def get_course_questions(course_id):
    sql = "select count(answers.id) as answers, questions.id, questions.inflection, questions.course_id, words.lemma from questions join words on questions.word_id = words.id left join answers on questions.id = answers.question_id group by questions.id, questions.inflection, questions.course_id, words.lemma having questions.course_id = :course_id order by words.lemma"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()


def get_question(question_id):
    sql = "select definitions.definition, words.lemma, questions.inflection, questions.course_id, questions.id \
        from questions \
        inner join definitions on questions.definition_id = definitions.id \
        inner join words on words.id = questions.word_id \
        where questions.id = :question_id"
    result = db.session.execute(sql, {"question_id":question_id})
    return result.fetchone()


def add_question(course_id, lemma_id, definition_id, inflection):
    try:
        sql = "insert into questions (course_id, word_id, definition_id, inflection) \
        values (:course_id, :lemma_id, :definition_id, :inflection)"
        db.session.execute(sql, {"course_id":course_id, "lemma_id":lemma_id, "definition_id":definition_id, "inflection":inflection})
        db.session.commit()
    except:
        return False
    return True


def remove_question(question_id):
    try:
        sql = "delete from questions where questions.id = :question_id"
        db.session.execute(sql, {"question_id":question_id})
        db.session.commit()
    except:
        return False
    return True
