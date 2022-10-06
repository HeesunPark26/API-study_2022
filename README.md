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

로컬에 빈 웹 서비스 띄우기 - 본인은 Python + Flask 조합을 사용
