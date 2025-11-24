from flask import Flask, request, render_template, jsonify
import csv
import os

app = Flask(__name__)

CSV_FILE = "rank.csv"

# CSV 파일 없으면 생성
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["school", "name", "score"])


@app.route("/")
def index():
    # CSV 읽기
    data = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    # 점수 높은 순 정렬
    data.sort(key=lambda x: int(x["score"]), reverse=True)

    return render_template("index.html", data=data)


@app.route("/rank", methods=["POST"])
def rank():
    school = request.form.get("school")
    name = request.form.get("name")
    score = request.form.get("score")

    if not school or not name or not score:
        return jsonify({"status": "error", "message": "missing params"}), 400

    # CSV에 저장
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([school, name, score])

    return jsonify({"status": "ok"})
    

if __name__ == "__main__":
    app.run()
