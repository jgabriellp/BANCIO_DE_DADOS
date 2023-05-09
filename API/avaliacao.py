import psycopg2
from datetime import datetime, date
import json
from flask import Flask, request

# Conecta ao banco de dados PostgreSQL - http://projetobd.cpq0d6o4wlxw.us-east-1.rds.amazonaws.com/
# projetobd.cpq0d6o4wlxw.us-east-1.rds.amazonaws.com
banco = psycopg2.connect(
    host="projetobd.cpq0d6o4wlxw.us-east-1.rds.amazonaws.com",
    database="projetobd",
    user="postgres",
    password="alunoaluno"
)

app = Flask(__name__)

# Rota para criar um novo medico
@app.route('/create_medico', methods=['POST'])
def create_medico():
    data = request.get_json()

    # Insere o medico no banco de dados
    comando = banco.cursor()
    comando.execute("INSERT INTO banco.medico VALUES ((CAST (%s AS INTEGER)),%s,%s,(CAST (%s AS INTEGER)),%s,%s,%s,%s,%s)",
                    (data['id_medico'], data['especialidade'], data['salario'], data['cpf'], data['primeiro_nome'],
                     data['sobrenome'], data['endereco'], data['data_nascimento'], data['telefone']))

    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Medico cadastrado com sucesso!'}))
    return json.dumps({'message': 'Medico cadastrado com sucesso!'})

# Rota para criar atualizar um medico
@app.route('/update_medico', methods=['PUT'])
def update_medico():
    data = request.get_json()

    # Atualiza o medico no banco de dados
    comando = banco.cursor()
    comando.execute("UPDATE banco.medico SET telefone = %s WHERE cpf = %s",
                    (data['telefone'], data['cpf']))

    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Medico atualizado com sucesso!'}))
    return json.dumps({'message': 'Medico atualizado com sucesso!'})

# Rota para buscar informações de um medico
@app.route('/get_medico/<cpf>', methods=['GET'])
def get_medico(cpf):
    cpf_new = str(cpf)

    # Busca o medico no banco de dados
    comando = banco.cursor()
    banco.rollback()
    comando.execute("SELECT * FROM banco.medico WHERE cpf = " + cpf_new)
    results = comando.fetchall()
    comando.close()

    if results:
        user_dict = {
            'id_medico': results[0][0],
            'especialidade': results[0][1],
            'salario': str(results[0][2]),
            'cpf': results[0][3],
            'primeiro_nome': results[0][4],
            'sobrenome': results[0][5],
            'endereco': results[0][6],
            'data_nascimento': str(results[0][7]),
            'telefone': results[0][8]
        }
        print(json.dumps(user_dict))
        return json.dumps(user_dict)
    else:
        print(json.dumps({'message': 'Medico nao encontrada.'}))
        return json.dumps({'message': 'Medico nao encontrada.'})

# Rota para deletar um medico
@app.route('/delete_medico', methods=['DELETE'])
def delete_medico():
    data = request.get_json()

    # Deleta o medico no banco de dados
    comando = banco.cursor()
    banco.rollback()
    comando.execute("DELETE FROM banco.medico WHERE cpf = (CAST (%s AS INTEGER))", data['cpf'])
    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Meddico deletado com sucesso.'}))
    return json.dumps({'message': 'Meddico deletado com sucesso.'})

# Rota para criar um novo sala_has_medico
@app.route('/create_sala_has_medico', methods=['POST'])
def create_sala_has_medico():
    data = request.get_json()

    # Insere uma sala em uso no banco de dados
    comando = banco.cursor()
    comando.execute("INSERT INTO banco.sala_has_medico VALUES ((CAST (%s AS INTEGER)),(CAST (%s AS INTEGER)))",
                    (data['id_sala'], data['id_medico']))

    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Sala criada com sucesso!'}))
    return json.dumps({'message': 'Sala criada com sucesso!'})

# Rota para atualizar uma nova sala_has_medico
@app.route('/update_sala_has_medico', methods=['PUT'])
def update_sala_has_medico():
    data = request.get_json()

    # Atualiza uma sala em uso no banco de dados
    comando = banco.cursor()
    banco.rollback()
    comando.execute("UPDATE banco.sala_has_medico SET id_medico = (CAST (%s AS INTEGER)) WHERE id_sala = (CAST (%s AS INTEGER)) AND id_medico = (CAST (%s AS INTEGER))",
                    (data['id_new'], data['id_sala'], data['id_old']))

    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Sala atualizada com sucesso!'}))
    return json.dumps({'message': 'Sala atualizada com sucesso!'})

# Rota para deletar uma nova sala_has_medico
@app.route('/delete_sala_has_medico', methods=['DELETE'])
def delete_sala_has_medico():
    data = request.get_json()

    # Deleta uma medico de uma sala em uso no banco de dados
    comando = banco.cursor()
    comando.execute("DELETE FROM banco.sala_has_medico WHERE id_sala = (CAST (%s AS INTEGER)) AND id_medico = (CAST (%s AS INTEGER))",
                    (data['id_sala'], data['id_medico']))
    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Sala deletada com sucesso!'}))
    return json.dumps({'message': 'Sala deletada com sucesso!'})

# Rota para buscar informações de uma sala_has_medico
@app.route('/get_sala_has_medico/<id_sala>', methods=['GET'])
def get_sala_has_medico(id_sala):
    id_new = str(id_sala)

    # Busca a sala em uso no banco de dados
    comando = banco.cursor()
    comando.execute("SELECT * FROM banco.sala_has_medico WHERE id_sala = " + id_new)
    results = comando.fetchall()
    comando.close()

    if results:
        user_dict = {
            'id_sala': results[0][0],
            'id_medico': results[0][1]
        }
        print(json.dumps(user_dict))
        return json.dumps(user_dict)
    else:
        print(json.dumps({'message': 'Sala nao encontrada.'}))
        return json.dumps({'message': 'Sala nao encontrada.'})


# Rota para criar uma nova sala
@app.route('/create_sala', methods=['POST'])
def create_sala():
    data = request.get_json()

    # Insere uma sala no banco de dados
    comando = banco.cursor()
    banco.rollback()
    comando.execute("INSERT INTO banco.sala VALUES ((CAST (%s AS INTEGER)),(CAST (%s AS INTEGER)),%s)",
                    (data['id_sala'], data['numero_sala'], data['status_sala']))

    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Sala criada com sucesso!'}))
    return json.dumps({'message': 'Sala criada com sucesso!'})


# Rota para atualizar uma sala
@app.route('/update_sala', methods=['PUT'])
def update_sala():
    data = request.get_json()

    # Atualiza uma sala no banco de dados
    banco.rollback()
    comando = banco.cursor()
    comando.execute("UPDATE banco.sala SET status_sala = %s WHERE numero_sala = (CAST (%s AS INTEGER))",
                    (data['status_sala'], data['numero_sala']))

    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Sala atualizada com sucesso!'}))
    return json.dumps({'message': 'Sala atualizada com sucesso!'})


# Rota para deletar uma sala
@app.route('/delete_sala/<numero_sala>', methods=['DELETE'])
def delete_sala(numero_sala):
    numero_new = str(numero_sala)

    # Deleta uma sala no banco de dados
    comando = banco.cursor()
    comando.execute("DELETE FROM banco.sala WHERE numero_sala = " + numero_new)
    banco.commit()
    comando.close()

    print(json.dumps({'message': 'Sala deletada com sucesso!'}))
    return json.dumps({'message': 'Sala deletada com sucesso!'})


# Rota para buscar informações de uma sala
@app.route('/get_sala/<numero_sala>', methods=['GET'])
def get_sala(numero_sala):
    numero_new = str(numero_sala)

    # Busca uma sala no banco de dados
    comando = banco.cursor()
    comando.execute("SELECT * FROM banco.sala WHERE numero_sala = " + numero_new)
    results = comando.fetchall()
    comando.close()

    if results:
        user_dict = {
            'id_sala': results[0][0],
            'numero_sala': results[0][1],
            'status_sala': str(results[0][2])
        }
        print(json.dumps(user_dict))
        return json.dumps(user_dict)
    else:
        print(json.dumps({'message': 'Sala nao encontrada.'}))
        return json.dumps({'message': 'Sala nao encontrada.'})


if __name__ == '__main__':
    app.run(debug=True)

    # http://localhost:5000/create_medico
    # http://localhost:5000/update_medico
    # http://localhost:5000/get_medico
    # http://localhost:5000/delete_medico

    # http://localhost:5000/create_sala_has_medico
    # http://localhost:5000/update_sala_has_medico
    # http://localhost:5000/delete_sala_has_medico/<id_sala>
    # http://localhost:5000/get_sala_has_medico/<id_sala>

    # http://localhost:5000/delete_sala
    # http://localhost:5000/update_sala
    # http://localhost:5000/get_sala/123456
    # http://localhost:5000/create_sala
