from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database connection
def get_db():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn

# Home page
@app.route("/")
def index():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

# Upload page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        subject = request.form["subject"]
        semester = request.form["semester"]
        file = request.files["file"]

        if file and file.filename.endswith(".pdf"):
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            conn = get_db()
            conn.execute(
                "INSERT INTO notes (subject, semester, filename) VALUES (?, ?, ?)",
                (subject, semester, filename)
            )
            conn.commit()
            conn.close()

            return redirect(url_for("index"))
        else:
            return "Please upload a PDF file."

    return render_template("upload.html")

# Search notes
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    conn = get_db()
    notes = conn.execute(
        "SELECT * FROM notes WHERE subject LIKE ? ORDER BY id DESC",
        ("%" + query + "%",)
    ).fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
    