# aim

## 주요 기술 스택

- Python 3.12.3 
- Django
- Django REST Framework
- Celery
- Redis
- MySQL 8.0.41

## 프로젝트 실행 방법
### 1. 가상환경 설정
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Celery 실행 방법
```bash
# venv
celery -A config worker -l info
```

### 3. Redis 설치 및 실행
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis
sudo systemctl start redis
```

### 4. 환경설정
시스템 환경에 맞추어 `env_template`을 바탕으로 `.env`을 생성합니다.

### 5. Django 서버 실행
```bash
python manage.py runserver
```

### 증권정보 더미데이터 삽입
```bash
# venv
python insert_dummy_data.py
```

