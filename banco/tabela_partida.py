from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import Time, db_session, Partida


def select_todos():
    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()
    return partidas
def salvar(time_casa_id,time_visitante_id,gols_casa,gols_visitante,data_partida):
    try:
        partidanova = Partida(time_casa_id=int(time_casa_id), time_visitante_id=int(time_visitante_id),
                              gols_casa=int(gols_casa), gols_visitante=int(gols_visitante),
                              data_partida=data_partida)
        db_session.add(partidanova)
        db_session.commit()
        flash("Partida criada com sucesso", "success")

    except SQLAlchemyError as e:
        db_session.rollback()
        print(e)
        flash("Erro ao criar a partida", "Error")

    except Exception as e:
        db_session.rollback()
        flash("Erro inesperado", "Error")
        print(e)