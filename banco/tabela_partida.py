from flask import flash
from sqlalchemy import select,func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import Time, db_session, Partida


def select_todos():

    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)
    partidas_sql = (
        select(Partida,TimeCasa,TimeVisitante)
        .join(TimeCasa,Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
    )
    partidas_casa = db_session.execute(partidas_sql).all()
    return partidas_casa
def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    qtd_total_partidas = db_session.execute(partidas_sql).scalar()
    return qtd_total_partidas
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

def select_por_time(id_time):
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)
    partidas_sql = (
        select(Partida, TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
        .where(or_(Partida.time_casa_id == id_time,Partida.time_visitante_id == id_time))
    )
    partidas_time = db_session.execute(partidas_sql).all()
    return partidas_time
print(select_por_time(1))