FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5001

RUN chmod +x ./start.sh

CMD ["bash", "start.sh"]
