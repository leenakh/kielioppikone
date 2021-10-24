from db import db


def get_all():
    sql = "select definitions.definition from definitions \
        order by definitions.definition desc"
    result = db.session.execute(sql)
    return result.fetchall()


def get_id(definition):
    sql = "select definitions.id from definitions \
        where definitions.definition = :definition"
    result = db.session.execute(sql, {
        "definition": definition})
    return result.fetchone()[0]
