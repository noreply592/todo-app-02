from flask import Flask, render_template

# 할일 데이터는 브라우저 localStorage에 저장됩니다.
# 서버는 페이지만 제공하므로 Vercel 같은 서버리스 환경에서도 그대로 동작합니다.
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
