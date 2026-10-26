from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__, template_folder=".")

DATABASE = "votes.db"


def initialize_database():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            choice TEXT PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.execute(
        "INSERT OR IGNORE INTO votes (choice, count) VALUES (?, ?)",
        ("cats", 0)
    )

    connection.execute(
        "INSERT OR IGNORE INTO votes (choice, count) VALUES (?, ?)",
        ("dogs", 0)
    )

    connection.commit()
    connection.close()


def get_votes():
    connection = sqlite3.connect(DATABASE)

    rows = connection.execute(
        "SELECT choice, count FROM votes"
    ).fetchall()

    connection.close()

    return {choice: count for choice, count in rows}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vote/<choice>", methods=["POST"])
def vote(choice):
    if choice not in ("cats", "dogs"):
        return jsonify({"error": "Invalid choice"}), 400

    connection = sqlite3.connect(DATABASE)

    connection.execute(
        "UPDATE votes SET count = count + 1 WHERE choice = ?",
        (choice,)
    )

    connection.commit()
    connection.close()

    return jsonify(get_votes())


@app.route("/results")
def results():
    return jsonify(get_votes())


initialize_database()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)