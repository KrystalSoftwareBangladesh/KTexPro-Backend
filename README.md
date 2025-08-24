# KTexPro

Solution oriented application for your Garments Buying House Business.

---

## Prerequisite
- Python 3
- PostgreSQL 16

---

## 📦 Installation

### Clone the repository
```bash
git clone git@github.com:KrystalSoftwareBangladesh/KTexPro-Backend.git
cd KTexPro-Backend
```

### Install dependency
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Environment Setup
```bash
cp .env.example KTexPro/env.py
```
And then update values based on your environment.

### Migration
```bash
python manage.py migrate
```

### Create Super User
```bash
python manage.py createsuperuser
```

### Run on local environment
```bash
python manage.py runserver
```
