from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import *
from database import Jogador, Time, db_session, Partida

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    # buscar todos os time no banco
    # 1- montar o select
    times_sql = select(Time)
    # 2-executar o select
    times = db_session.execute(times_sql).scalars().all()

    nome = times
    return render_template(
        "dashboard.html",
        total_jogadores=0,
        total_times=len(times),
        total_partidas=0,

    )


@app.route("/jogadores")
def listar_jogadores():
    return render_template("jogadores.html", jogadores=[], times=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None
        if not nome:
            flash("Preencha o nome do jogador", "Error")
            return render_template("jogadores.html")
        if not numero_camisa:
            flash("Preencha o numero da camisa do jogador", "Error")
            return render_template("jogadores.html")
        if not posicao:
            flash("Preencha a posição do jogador", "Error")
            return render_template("jogadores.html")
        try:
            jogadornovo = Jogador(nome=nome, numero_camisa=numero_camisa, posicao=posicao)
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
    # buscar todos os time no banco
    # 1- montar o select
    times_sql = select(Time)
    # 2-executar o select
    times = db_session.execute(times_sql).scalars().all()

    return render_template("jogadores.html", jogadores=[], times=times)


@app.route("/times")
def listar_times():
    # buscar todos os time no banco
    # 1- montar o select
    times_sql = select(Time)
    # 2-executar o select
    times = db_session.execute(times_sql).scalars().all()
    print(times)
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        # 1-pegar os valores digitados no forms
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        turma = request.form.get("turma", "").strip()
        # 2-verificar se foi digitado
        if not nome:
            flash("Preencha o nome do time", "Error")
            return render_template("times.html")
        if not responsavel:
            flash("Preencha o nome do responsavel pelo time", "Error")
            return render_template("times.html")
        if not turma:
            flash("Preencha a turma do time", "Error")
            return render_template("times.html")
        # 3-salvar no banco
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
    # buscar todos os time no banco
    # 1- montar o select
    times_sql = select(Time)
    # 2-executar o select
    times = db_session.execute(times_sql).scalars().all()
    print(times)

    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():
    return render_template("partidas.html", partidas=[], times=[])


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        if not time_casa_id:
            flash("Preencha o time da casa", "Error")
            return render_template("partidas.html")

        if not time_visitante_id:
            flash("Preencha o nome do time visitante", "Error")
            return render_template("partidas.html")
        if not gols_casa:
            flash("Preencha os gols do time da casa", "Error")
            return render_template("partidas.html")
        if not gols_visitante:
            flash("Preencha os gols do time visitante", "Error")
            return render_template("partidas.html")
        if not data_partida:
            flash("Preencha a data da partida", "Error")
            return render_template("partidas.html")
        try:
            partidanova = Partida(time_casa_id=int(time_casa_id), time_visitante_id=int(time_visitante_id),
                                  gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
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

    return render_template("partidas.html", partidas=[], times=[])


if __name__ == "__main__":
    app.run(debug=True)
