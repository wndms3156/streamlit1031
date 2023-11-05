import streamlit as st
import sqlite3


# 데이터베이스 연결을 열기 위한 함수
def get_connection():
    conn = sqlite3.connect('./login.db', check_same_thread=False)
    return conn


# 상태를 초기화하는 함수
def initialize_state():
    st.session_state.page = "login"
    st.session_state.username = ""
    st.session_state.password = ""
    st.session_state.logged_in = False


# Streamlit 앱 초기화
initialize_state()

st.title("회원가입과 로그인을 해보세요!")

# Create empty placeholders for login input fields
login_id_placeholder = None
login_pw_placeholder = None

# 로그인 페이지
if st.session_state.page == "login":
    st.header("로그인")

    if not st.session_state.logged_in:
        login_id_placeholder = st.empty()
        login_pw_placeholder = st.empty()

        login_id = login_id_placeholder.text_input("사용자 이름:", key="login_id")
        login_pw = login_pw_placeholder.text_input("비밀번호:", type="password", key="login_pw")

        login_button = st.button("로그인")

        if login_button:
            conn = get_connection()  # 데이터베이스 연결 열기
            cursor = conn.cursor()

            # 로그인 버튼을 클릭한 경우 로그인 로직을 추가
            cursor.execute("SELECT id, pw FROM user WHERE id = ? AND pw = ?", (login_id, login_pw))
            user = cursor.fetchone()
            conn.close()  # 데이터베이스 연결 닫기

            if user:
                st.success("로그인되었습니다.")
                st.session_state.logged_in = True
                st.session_state.page = "home"
                st.session_state.username = login_id
                # Hide the login input fields
                login_id_placeholder.empty()
                login_pw_placeholder.empty()
            else:
                st.error("사용자 이름 또는 비밀번호가 올바르지 않습니다.")

# 홈 페이지
if st.session_state.page == "home":
    st.header(f"환영합니다, {st.session_state.username}! 로그인이 완료되었습니다.")
    st.write("이 페이지에서 추가적인 컨텐츠를 보실 수 있습니다.")
    # 데이터 조회 및 표시
    st.subheader("사용자 목록:")
    conn = get_connection()  # 데이터베이스 연결 열기
    cursor = conn.cursor()
    cursor.execute("SELECT id, pw FROM user")
    data = cursor.fetchall()
    conn.close()  # 데이터베이스 연결 닫기

    for row in data:
        st.write(f"아이디: {row[0]}, 비밀번호: {row[1]}")
    # 로그아웃
    if st.button("로그아웃"):
        initialize_state()  # 로그아웃하면 다시 초기화

# 회원가입 페이지
if not st.session_state.logged_in:
    st.header("회원가입")
    signup_id = st.text_input("사용자 이름:", key="signup_id")
    signup_pw = st.text_input("비밀번호:", type="password", key="signup_pw")
    signup = st.button("가입")

    if signup:
        conn = get_connection()  # 데이터베이스 연결 열기
        cursor = conn.cursor()

        # 가입 버튼을 클릭한 경우 아이디 중복 확인
        cursor.execute("SELECT id FROM user WHERE id = ?", (signup_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            st.error("이미 존재하는 아이디입니다. 다른 아이디를 사용해주세요.")
        else:
            # 가입 로직을 처리하고 데이터베이스에 추가
            cursor.execute("INSERT INTO user (id, pw) VALUES (?, ?)", (signup_id, str(signup_pw)))
            conn.commit()  # 변경사항을 저장
            conn.close()  # 데이터베이스 연결 닫기
            st.success("회원가입이 완료되었습니다.")
