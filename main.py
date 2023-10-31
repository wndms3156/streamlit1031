import streamlit as st
import sqlite3

# 데이터베이스 연결을 열기 위한 함수
def get_connection():
    conn = sqlite3.connect('./login.db', check_same_thread=False)
    return conn

# Streamlit 앱 시작
st.title("SQLite와 Streamlit 연동 예제")
# 초기에 회원가입 폼만 표시
st.header("회원가입")
signup_id = st.text_input("사용자 이름:", key="signup_id")
signup_pw = st.text_input("비밀번호:", type="password", key="signup_pw")
signup_button = st.button("가입")

# 로그인 폼
st.header("로그인")
login_id = st.text_input("사용자 이름:", key="login_id")
login_pw = st.text_input("비밀번호:", type="password", key="login_pw")
login_button = st.button("로그인")

message = st.empty()  # 빈 메시지 컨테이너 생성

if signup_button:
    conn = get_connection()  # 데이터베이스 연결 열기
    cursor = conn.cursor()

    # 가입 버튼을 클릭한 경우 아이디 중복 확인
    cursor.execute("SELECT id FROM users WHERE id = ?", (signup_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        message.text("이미 존재하는 아이디입니다. 다른 아이디를 사용해주세요.")
    else:
        # 가입 로직을 처리하고 데이터베이스에 추가
        cursor.execute("INSERT INTO users (id, pw) VALUES (?, ?)", (signup_id, str(signup_pw)))
        conn.commit()  # 변경사항을 저장
        conn.close()  # 데이터베이스 연결 닫기
        message.text("회원가입이 완료되었습니다.")

if login_button:
    conn = get_connection()  # 데이터베이스 연결 열기
    cursor = conn.cursor()

    # 로그인 버튼을 클릭한 경우 로그인 로직을 추가
    cursor.execute("SELECT id, pw FROM users WHERE id = ? AND pw = ?", (login_id, login_pw))
    user = cursor.fetchone()
    conn.close()  # 데이터베이스 연결 닫기

    if user:
        message.text("로그인되었습니다.")
        signup_button = False  # 회원가입 폼을 숨깁니다.
        login_button = False  # 로그인 폼을 숨깁니다.
    else:
        message.text("사용자 이름 또는 비밀번호가 올바르지 않습니다.")

# 데이터 조회 및 표시
st.subheader("사용자 목록:")
conn = get_connection()  # 데이터베이스 연결 열기
cursor = conn.cursor()
cursor.execute("SELECT id, pw FROM users")
data = cursor.fetchall()
conn.close()  # 데이터베이스 연결 닫기

for row in data:
    st.write(f"아이디: {row[0]}, 비밀번호: {row[1]}")
