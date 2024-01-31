from flask import Flask, render_template, request

import sqlite3

# 데이터베이스 연결 및 테이블 생성
def init_db():
    conn = sqlite3.connect('profile_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profiles
                 (name TEXT, gender TEXT, semester TEXT, mbti TEXT, sleep_time TEXT, cleaning TEXT, bathroom_cleaning TEXT, trash_disposal TEXT, item_sharing TEXT, gaming_music TEXT, snoring TEXT, deep_sleep TEXT, trash_share TEXT, study_lamp_off_time TEXT, smoking_preference TEXT, relationship_preference TEXT, phone_calls_preference TEXT)''')
    conn.commit()
    conn.close()

app = Flask(__name__)

# 번역 사전
translations = {
    'male': '남자',
    'female': '여자',
    '16': '16주(학기)',
    '25': '25주(반기)',
    'daily': '매일',
    'weekly_1': '일주일에 1번',
    'weekly_2_3': '일주일에 2-3번',
    'weekly_4': '일주일에 4번',
    'when_dirty': '더러울 때',
    'separately': '분리수거함 두고 한번에',
    'each_time': '생길 때마다 각자 알아서',
    'allowed': '허용',
    'permission_required': '허락받고 가능한 것만',
    'all_possible': '전부 가능',
    'yes': '사용',
    'no': '미사용',
    'cigarette': '노담',
    'both': '연초',
    'non_smoker': '전담',
    'best_friend': '베스트 프렌드',
    'business': '비지니스',
    'middle': '중간',
    'outside': '외부',
    'parents': '부모님과 짧은 전화만',
    'short': '짧은 전화만',
    'no_preference': '무관',
}

# 프로필 데이터 저장
def save_profile_data(data):
    conn = sqlite3.connect('profile_database.db')
    c = conn.cursor()
    c.execute('INSERT INTO profiles VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', 
              tuple(data.values()))
    conn.commit()
    conn.close()

# 모든 이름 조회
def get_all_names():
    conn = sqlite3.connect('profile_database.db')
    c = conn.cursor()
    c.execute('SELECT name FROM profiles')
    names = [name[0] for name in c.fetchall()]
    conn.close()
    return names

# Flask 애플리케이션에서 "/view_profiles" 경로 추가
@app.route('/view_profiles')
def view_profiles():
    names = get_all_names()  # DB에서 모든 이름을 가져옴
    return render_template('success.html', names=names)


# 메인 페이지 라우트
@app.route('/')
def index():
    names = get_all_names()  # DB에서 모든 이름을 가져옴
    return render_template('success.html', names=names)


# 프로필 제출 라우트
@app.route('/submit_profile', methods=['POST'])
def submit_profile():
    profile_data = {
        'name': request.form['name'],
        'gender': request.form['gender'],
        'semester': request.form['semester'],
        'mbti': request.form['mbti'],
        'sleep_time': request.form['sleep_time'],
        'cleaning': request.form['cleaning'],
        'bathroom_cleaning': request.form['bathroom_cleaning'],
        'trash_disposal': request.form['trash_disposal'],
        'item_sharing': request.form['item_sharing'],
        'gaming_music': request.form['gaming_music'],
        'snoring': request.form['snoring'],
        'deep_sleep': request.form['deep_sleep'],
        'trash_share': request.form['trash_share'],
        'study_lamp_off_time': request.form['study_lamp_off_time'],
        'smoking_preference': request.form['smoking_preference'],
        'relationship_preference': request.form['relationship_preference'],
        'phone_calls_preference': request.form['phone_calls_preference']
    }
    save_profile_data(profile_data)  # 프로필 데이터 저장 함수 호출 (이전에 정의되어야 함)

    names = get_all_names()  # names.txt 파일에서 모든 이름을 불러옴

    return render_template('success.html', names=names)


# 프로필 조회 라우트
@app.route('/profile/<name>')
def view_profile(name):
    conn = sqlite3.connect('profile_database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM profiles WHERE name=?', (name,))
    row = c.fetchone()
    conn.close()
    if row:
        profile_data_keys = ['name', 'gender', 'semester', 'mbti', 'sleep_time', 'cleaning', 'bathroom_cleaning', 'trash_disposal', 'item_sharing', 'gaming_music', 'snoring', 'deep_sleep', 'trash_share', 'study_lamp_off_time', 'smoking_preference', 'relationship_preference', 'phone_calls_preference']
        profile_data = {
            key: row[i] if key in ['mbti', 'age', 'semester', 'sleep_time', 'study_lamp_off_time'] else translations.get(row[i], row[i]) 
            for i, key in enumerate(profile_data_keys)
        }

        return render_template('profile_detail.html', profile_data=profile_data)
    else:
        return f"{name}의 프로필을 찾을 수 없습니다.", 404

@app.route('/new_profile')
def new_profile():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(port=4000,host='0.0.0.0')
