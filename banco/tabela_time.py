from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import Time, db_session


def select_todos():
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()
    return times
def salvar(nome,turma,responsavel):
    try:
        timenovo = Time(nome=nome, responsavel=responsavel, turma=turma)
        db_session.add(timenovo)
        db_session.commit()
        flash("Time criado com sucesso", "success")

    except SQLAlchemyError as e:
        db_session.rollback()
        print(e)
        flash("Erro ao criar o time", "Error")

    except Exception as e:
        db_session.rollback()
        flash("Erro inesperado", "Error")
        print(e)