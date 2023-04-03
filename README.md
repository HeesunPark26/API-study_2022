# API-study_2022

Wellysis 사내 스터디 (기초 백엔드 API) 기록 repo입니다.

API가 무엇인지...에 대한 이해부터 시작하기 위해 토큰 인증 구현, user 부분 구현 등을 생략하고 진행한 스터디입니다.

아래 스터디 이후 모든 것을 구현한 두번째 스터디를 진행했습니다.
- 두번째 스터디 보러 가기 [링크](https://github.com/HeesunPark26/API-study_2023)

기간: 2022.09 - 2022.11

참고: https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints

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
  1. 이렇게 DB에 직접 저장하고 response body를 위해 다시 data를 retrieve하는 것이 맞는지? O
  2. tag를 List로 저장하기(현재는 "tag1, tag2"로 저장, ["tag1", "tag2"]로 저장하고 싶음
    - sql에는 일단 string으로 저장, list로 받은 인풋을 자체적으로 string으로 바꾸고 return할때는 다시 파싱해서 list로 내보내는 방식으로 할 것.
  3. author 정보 잘 가져와서 JSON에 넣기 (SQL에서부터 깔끔하게 가져오기 vs 다 불러와서 Python에서 잘 조합)


* 참고
  * https://www.youtube.com/watch?v=EgnyWxKFwjs&list=PLillGF-RfqbbbPz6GSEM9hLQObuQjNoj_&index=4
  * https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
  * https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
  * https://flask.palletsprojects.com/en/2.2.x/tutorial/database/
  
## 3주차 - 아티클 get, update, and delete
* 미션: {{로컬호스트url}}/articles/{{slug}}로 들어온 요청을 요청 종류에 따라 처리함 (get, put (update), delete)
  * update할 때는 title이 바뀌면 slug도 바뀌도록

* 결과: [app.py](https://github.com/HeesunPark26/API-study_2022/blob/main/app.py)


## 4주차 - comment create, get, and delete
* 미션: {{로컬호스트url}}/articles/{{slug}}/comments로 들어온 요청을 요청 종류에 따라 처리함 POST, GET, DELETE (delete의 경우에는 /comments/{{id}} 까지)

* 결과: [app.py](https://github.com/HeesunPark26/API-study_2022/blob/main/app.py)

## 5주차 - favorite article, unfavorite article, get tags
* 미션: {{로컬호스트url}}/articles/{{slug}}/favorite 로 들어온 요청을 종류에 따라 처리함(POST, DELETE) + GET {{로컬호스트url}}/tags 를 통해 tags 불러오기.

* 결과: [app.py](https://github.com/HeesunPark26/API-study_2022/blob/main/app.py)

## 6주차 - list articles, feed articles
* 미션: list article의 경우 GET {{로컬호스트url}}/articles를 콜했을 때 filter에 따라서 아티클 보여주기. feed article의 경우 GET {{로컬호스트url}}/articles/feed를 콜했을 때 article 보여주기

* 결과: [app.py](https://github.com/HeesunPark26/API-study_2022/blob/main/app.py)

 * 참고: 수정하고 tag 처리하는 과정에서 에러 발생함. 수정 요망..
