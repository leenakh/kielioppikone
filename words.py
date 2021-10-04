from db import db


def get_all():
    sql = "select words.lemma from words"
    result = db.session.execute(sql)
    return result.fetchall()


def get_id(lemma):
    sql = "select words.id from words where words.lemma = :lemma"
    result = db.session.execute(sql, {"lemma": lemma})
    return result.fetchone()[0]


def add(lemma):
    sql = "insert into words (lemma) values (:lemma) returning id"
    result = db.session.execute(sql, {"lemma": lemma})
    db.session.commit()
    return result.fetchone()[0]
