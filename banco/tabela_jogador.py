from flask import flash
from sqlalchemy import select,func
from sqlalchemy.exc import SQLAlchemyError

from database import Time, db_session, Jogador


def select_todos():
    # join(tabela que eu quero juntar,condição= chave estrangeira igual chave primaria)
    jogadores_sql = select(Jogador,Time).join(Time,Jogador.time_id == Time.id)
    # usar scallars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()
    return jogadores
def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total_jogadores = db_session.execute(jogadores_sql).scalar()

    return qtd_total_jogadores
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