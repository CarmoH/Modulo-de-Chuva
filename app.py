from flask import Flask, jsonify, render_template, request
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)


# Conexão com o PostgreSQL (ajuste os dados abaixo)
dbconfig ={
  'host': "localhost",
    'port': 5432,
    'dbname': "Banco",
    'user': "postgres",
    'password': "adminalice"
}

def db_connect():
    return psycopg.connect(**dbconfig)

@app.route('/')
def index():
    return render_template('index.html')  # o gráfico está aqui

@app.route('/dados')
def dados():
    try:
        conn = db_connect() # CONECTA AO BANCO DE DADOS
        cur = conn.cursor()
        cur.execute("""
                SELECT data_hora, valor_chuva, valor_luz
                FROM leituras
                ORDER BY data_hora DESC
                LIMIT 10
        """)
        rows = cur.fetchall()
        cur.close()

        dados = [
            {
                "hora": row[0].strftime("%H:%M:%S"),
                "valor_chuva": row[1],
                "valor_luz": row[2]
            }
            for row in reversed(rows)
        ]
        return jsonify(dados)

    except Exception as e:
        print("Erro na rota /dados:", e)
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/receber_dados', methods=['POST'])
def receber_dados():
    try:
        dados = request.get_json()

        valor_chuva = dados.get('valor_chuva')
        valor_luz = dados.get("valor_luz")

        conn = db_connect()

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO leituras (valor_chuva, valor_luz)
            VALUES (%s, %s)
        """, (valor_chuva, valor_luz))
        conn.commit()
        cur.close()
        conn.close() # FECHA A CONEXÃO

        return jsonify({"mensagem": "Dados inseridos com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    # Use host='0.0.0.0' se quiser permitir acesso do ESP32 (na rede)
    app.run(debug=True, host='0.0.0.0')
