import os
import uuid
from cs50 import SQL
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "cs50-study-calendar-default-secret")

# Conecta ao banco de dados SQLite
db = SQL("sqlite:///study.db")


def get_workspace_id():

  if "workspace_id" not in session:
        session["workspace_id"] = str(uuid.uuid4())
    return session["workspace_id"]


@app.route("/")
def index():
    get_workspace_id()
    return render_template("index.html")


@app.route("/logs", methods=["GET"])
def get_logs():

  workspace_id = get_workspace_id()

    logs = db.execute(
        "SELECT date, topic, notes FROM logs WHERE workspace_id = ?",
        workspace_id
    )
    return jsonify(logs)


@app.route("/save", methods=["POST"])
def save_log():

  workspace_id = get_workspace_id()

    data = request.get_json()
    if not data:
        return jsonify({"error": "Requisição inválida ou sem dados"}), 400

    date = data.get("date")
    topic = data.get("topic", "").strip()
    notes = data.get("notes", "").strip()

  if not date:
        return jsonify({"error": "A data é obrigatória"}), 400

    if len(topic) > 100:
        return jsonify({"error": "O tópico não pode passar de 100 caracteres"}), 400

    if len(notes) > 5000:
        return jsonify({"error": "As anotações não podem passar de 5000 caracteres"}), 400
   
  existing = db.execute(
        "SELECT id FROM logs WHERE workspace_id = ? AND date = ?",
        workspace_id, date
    )

    if len(existing) > 0:
        if not topic and not notes:
            db.execute("DELETE FROM logs WHERE id = ?", existing[0]["id"])
        else:
            db.execute(
                "UPDATE logs SET topic = ?, notes = ? WHERE id = ?",
                topic, notes, existing[0]["id"]
            )
    else:
        if topic or notes:
            db.execute(
                "INSERT INTO logs (workspace_id, date, topic, notes) VALUES (?, ?, ?, ?)",
                workspace_id, date, topic, notes
            )

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
