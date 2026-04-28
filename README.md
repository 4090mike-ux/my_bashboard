# 기술 배지 대시보드

기술명을 입력하면 종류에 따라 색상 배지로 표시되는 대시보드입니다.

---

## 실행 방법

```bash
# 1. 프로젝트 폴더로 이동
cd ~/mypj/my_dashboard

# 2. 가상환경 활성화 → 프롬프트 앞에 (.venv) 가 붙으면 성공
source .venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 서버 실행
python app.py
```

브라우저에서 http://127.0.0.1:5000 접속

---

## 데이터 흐름 (전체 동작 원리)

```
사용자가 입력창에 기술명 입력
        ↓
[추가] 버튼 클릭 → HTML form이 POST /add 로 전송
        ↓
app.py의 add() 함수 실행
  → request.form 으로 입력값 받기
  → if skill: 로 빈 값 걸러내기
  → skills.append(skill) 로 리스트에 저장
  → redirect("/") 로 첫 페이지로 이동
        ↓
app.py의 index() 함수 실행
  → skills 리스트를 index.html 로 전달
        ↓
index.html에서 for문으로 반복 출력
  → if/elif 로 기술명에 따라 배지 색상 결정
  → 화면에 배지로 표시
```

---

## app.py 코드 설명

```python
from flask import Flask, render_template, request, redirect
# Flask   : 웹 서버를 만드는 도구
# render_template : HTML 파일을 화면에 보여주는 함수
# request : 사용자가 보낸 데이터를 받는 도구
# redirect : 다른 주소로 이동시키는 함수

app = Flask(__name__)
# Flask 앱을 만든다

skills = []
# 사용자가 입력한 기술명을 저장하는 리스트 (빈 리스트로 시작)

@app.route("/")
def index():
    return render_template("index.html", skills=skills)
# 브라우저가 "/" 주소로 접속하면 index.html을 보여준다
# skills 리스트를 HTML에 넘겨준다

@app.route("/add", methods=["POST"])
def add():
    skill = request.form.get("skill", "").strip()
    # request.form : HTML form에서 보낸 데이터를 받는다
    # .get("skill") : input name="skill" 의 값을 꺼낸다
    # .strip() : 앞뒤 공백 제거

    if skill:
        skills.append(skill)
    # 빈 값이면 저장하지 않는다 (예외 처리)
    # 값이 있을 때만 리스트에 추가한다

    return redirect("/")
    # 저장 후 "/" 로 돌아가서 화면을 새로고침한다

if __name__ == "__main__":
    app.run(debug=True)
# 이 파일을 직접 실행할 때만 서버를 시작한다
```

---

## index.html 코드 설명

```html
<form action="/add" method="POST">
    <input type="text" name="skill">
    <button type="submit">추가</button>
</form>
<!-- action="/add" : 버튼을 누르면 /add 주소로 데이터를 보낸다 -->
<!-- method="POST" : 데이터를 POST 방식으로 전송한다 -->
<!-- name="skill"  : app.py에서 request.form.get("skill") 로 받는 이름 -->

{% for skill in skills %}
    <!-- skills 리스트에 있는 항목을 하나씩 꺼내서 반복 출력 -->

    {% if skill == "python" %}
        <span>[backend] python</span>   <!-- 회색 -->
    {% elif skill == "sql" %}
        <span>[DB] sql</span>           <!-- 보라색 -->
    {% elif skill == "html" %}
        <span>html</span>               <!-- 주황색 -->
    {% elif skill == "bash" %}
        <span>bash</span>               <!-- 초록색 -->
    {% else %}
        <span>[ETC] {{ skill }}</span>  <!-- 검정색 -->
    {% endif %}

{% endfor %}
<!-- 리스트의 모든 항목을 출력한 뒤 반복 종료 -->
```

---

## 주요 명령어 정리

| 명령어 | 설명 |
|--------|------|
| `python3 -m venv .venv` | 가상환경 만들기 |
| `source .venv/bin/activate` | 가상환경 활성화 |
| `pip install flask` | Flask 설치 |
| `pip freeze > requirements.txt` | 설치된 패키지 목록 저장 |
| `pip install -r requirements.txt` | 목록 보고 패키지 한번에 설치 |
| `python app.py` | Flask 서버 실행 |
| `Ctrl + C` | 서버 종료 |
