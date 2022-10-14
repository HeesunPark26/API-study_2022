# API-study_2022

Wellysis 사내 스터디 (기초 백엔드 API) 기록 repo입니다.

## Setting

**1. 가상환경 생성**
```bash
python -m venv .venv
```

  - (option) 가상환경 디렉토리를 .gitignore에 추가
```bash
echo '.venv' >> .gitignore
```

**2. 가상환경 활성화**
```bash
. .venv/bin/activate
```

  - (option) check 
```bash
which python
```
가상환경 내의 Python을 사용하고 있으면 OK

**3. 패키지 다운로드**
```bash
pip install -r requirements.txt 
```


**4. 가상환경 비활성화**
```bash
deactivate
```

## 1주차 - 환경 설정

* 미션: 로컬에 빈 웹 서비스 띄우기 - 본인은 Python + Flask 조합을 사용

* 결과: [hello.py](https://github.com/HeesunPark26/API-study_2022/blob/main/hello.py) 확인
  * 환경 설정 후 터미널에 `python hello.py` 치면 로컬 주소(e.g., http://127.0.0.1:5000) 확인 가능 -> 해당 주소로 접속


## 2주차 - 아티클 생성
* 미션: {{로컬호스트url}}/articles 요청으로 아티클을 생성한다.
  * 예시) POST /localhost:8080/articles
  
* 결과: [app.py](https://github.com/HeesunPark26/API-study_2022/blob/main/app.py) & [init_db.py](https://github.com/HeesunPark26/API-study_2022/blob/main/init_db.py)
  1. [한번만] `init_db.py` 실행하여 database 생성 및 initialization
  2. Postman에서 `POST http://127.0.0.1:5000/article_`로 요청
  3. request body로 받은 데이터 `database.db`에 저장 (sqlite3 사용)
  4. DB에서 다시 데이터 불러와 reponse body 보냄

* 불충분한 부분
  1. 이렇게 DB에 직접 저장하고 response body를 위해 다시 data를 retrieve하는 것이 맞는지?
  2. tag를 List로 저장하기(현재는 "tag1, tag2"로 저장, ["tag1", "tag2"]로 저장하고 싶음
  3. author 정보 잘 가져와서 JSON에 넣기 (SQL에서부터 깔끔하게 가져오기 vs 다 불러와서 Python에서 잘 조합)


* 참고
  * https://www.youtube.com/watch?v=EgnyWxKFwjs&list=PLillGF-RfqbbbPz6GSEM9hLQObuQjNoj_&index=4
  * https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
  * https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
  * https://flask.palletsprojects.com/en/2.2.x/tutorial/database/
