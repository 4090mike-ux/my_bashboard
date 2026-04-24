from flask import Flask, render_template, request, redirect

app = Flask(__name__)

skills = []

@app.route("/")
def index():
    return render_template("index.html", skills=skills)

@app.route("/add", methods=["POST"])
def add():
    skill = request.form.get("skill", "").strip()
    if skill:
        skills.append(skill)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
