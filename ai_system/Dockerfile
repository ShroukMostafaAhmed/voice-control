FROM python:3.11-slim

WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المكتبات مع زيادة وقت الانتظار لتجنب خطأ الـ Timeout
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# نسخ باقي الكود
COPY . .

# تشغيل محرك الذكاء الاصطناعي
CMD ["python", "ai_api.py"]