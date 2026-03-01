FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# تثبيت المكتبات مع زيادة وقت الانتظار
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

COPY . .

# تشغيل FastAPI (تأكد أن الملف الأساسي اسمه main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]