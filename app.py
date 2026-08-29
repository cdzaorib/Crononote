import os
import uuid

from cs50 import SQL
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)

# Chave usada para proteger a sessão
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "cs50-study-calendar-default-secret"
)

# Conecta ao banco de dados SQLite
db = SQL("sqlite:///study.db")

# Cria a tabela caso ela ainda não exista
db.execute(
    """
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workspace_id TEXT NOT NULL,
        date TEXT NOT NULL,
        topic TEXT NOT NULL,
        notes TEXT NOT NULL
    )
    """
)


def get_workspace_id():
    """Retorna o workspace atual e cria um novo se necessário."""
    if "workspace_id" not in session:
        session["workspace_id"] = str(uuid.uuid4())

    return session["workspace_id"]


@app.route("/")
def index():
    """Página principal."""
    get_workspace_id()
    return render_template("index.html")


@app.route("/logs", methods=["GET"])
def get_logs():
    """Retorna as anotações do workspace atual."""
    workspace_id = get_workspace_id()

    logs = db.execute(
        """
        SELECT date, topic, notes
        FROM logs
        WHERE workspace_id = ?
        ORDER BY date
        """,
        workspace_id
    )

    return jsonify(logs)


@app.route("/save", methods=["POST"])
def save_log():
    """Cria, atualiza ou remove uma anotação."""
    workspace_id = get_workspace_id()

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Requisição inválida ou sem dados"
        }), 400

    date = data.get("date")
    topic = data.get("topic", "").strip()
    notes = data.get("notes", "").strip()

    # Validação da data
    if not date:
        return jsonify({
            "error": "A data é obrigatória"
        }), 400

    # Limite do tópico
    if len(topic) > 100:
        return jsonify({
            "error": "O tópico não pode passar de 100 caracteres"
        }), 400

    # Limite das anotações
    if len(notes) > 5000:
        return jsonify({
            "error": "As anotações não podem passar de 5000 caracteres"
        }), 400

    # Procura uma anotação existente para essa data
    existing = db.execute(
        """
        SELECT id
        FROM logs
        WHERE workspace_id = ? AND date = ?
        """,
        workspace_id,
        date
    )

    if len(existing) > 0:

        log_id = existing[0]["id"]

        # Se não existe mais conteúdo, remove a anotação
        if not topic and not notes:
            db.execute(
                "DELETE FROM logs WHERE id = ?",
                log_id
            )

        # Caso contrário, atualiza
        else:
            db.execute(
                """
                UPDATE logs
                SET topic = ?, notes = ?
                WHERE id = ?
                """,
                topic,
                notes,
                log_id
            )

    # Não existe anotação: cria uma nova
    elif topic or notes:
        db.execute(
            """
            INSERT INTO logs
            (workspace_id, date, topic, notes)
            VALUES (?, ?, ?, ?)
            """,
            workspace_id,
            date,
            topic,
            notes
        )

    return jsonify({
        "success": True
    })


if __name__ == "__main__":
    app.run(debug=True)