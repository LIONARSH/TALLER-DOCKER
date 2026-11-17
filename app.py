from flask import Flask, render_template_string, request, redirect, url_for
import os
import psycopg2

app = Flask(__name__)

# Función para conectar y crear la tabla si no existe
def init_db():
    try:
        conn = psycopg2.connect(
            dbname="leonardo_db",
            user="leonardo_user",
            password="mi_password_seguro",
            host="db",
            port="5432"
        )
        cursor = conn.cursor()
        # Creamos una tabla llamada 'registros' si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error al inicializar la BD:", e)

# Inicializamos la base de datos al arrancar
init_db()

@app.route('/')
def home():
    registros = []
    try:
        conn = psycopg2.connect(
            dbname="leonardo_db",
            user="leonardo_user",
            password="mi_password_seguro",
            host="db",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM registros ORDER BY id DESC;")
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error al consultar:", e)

    # Interfaz visual HTML con formulario y tabla de registros
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>App con Base de Datos - Leonardo Atiencia</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f6f9; text-align: center; padding: 40px; }
            .card { background: white; max-width: 500px; margin: 0 auto; padding: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; font-size: 24px; }
            h2 { color: #27ae60; font-size: 18px; }
            input[type="text"] { padding: 10px; width: 70%; border: 1px solid #ccc; border-radius: 5px; margin-right: 5px; }
            button { padding: 10px 15px; background-color: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background-color: #219653; }
            ul { list-style: none; padding: 0; margin-top: 20px; text-align: left; }
            li { background: #e8f8f5; margin-bottom: 8px; padding: 10px; border-radius: 5px; border-left: 4px solid #27ae60; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Yo estudio en Yavirac</h1>
            <h2>Leonardo Atiencia</h2>
            <p>Registro de datos en PostgreSQL con Docker Compose</p>
            
            <form action="/add" method="POST">
                <input type="text" name="nombre" placeholder="Escribe un dato o nombre..." required>
                <button type="submit">Guardar</button>
            </form>

            <h3 style="margin-top: 30px; color: #333;">Datos guardados en la BD:</h3>
            <ul>
                {% for reg in registros %}
                    <li><b>#{{ reg[0] }}</b> - {{ reg[1] }}</li>
                {% else %}
                    <li style="text-align: center; color: #7f8c8d;">No hay registros todavía.</li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, registros=registros)

@app.route('/add', methods=['POST'])
def add():
    nuevo_nombre = request.form.get('nombre')
    if nuevo_nombre:
        try:
            conn = psycopg2.connect(
                dbname="leonardo_db",
                user="leonardo_user",
                password="mi_password_seguro",
                host="db",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO registros (nombre) VALUES (%s);", (nuevo_nombre,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("Error al insertar:", e)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
