from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import Time, db_session, Jogador


def select_todos():
    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return jogadores
def salvar(nome,numero_camisa,posicao,time_id):
    try:
        jogadornovo = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
        db_session.add(jogadornovo)
        db_session.commit()
        flash("jogador criado com sucesso", "success")

    except SQLAlchemyError as e:
        db_session.rollback()
        print(e)
        flash("Erro ao criar o jogador", "Error")

    except Exception as e:
        db_session.rollback()
        flash("Erro inesperado", "Error")
        print(e)