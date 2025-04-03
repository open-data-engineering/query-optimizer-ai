FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH="/app"
ENV PORT=8080

EXPOSE 8080

CMD ["streamlit", "run", "app/ui/dashboard.py", "--server.port=8080", "--server.address=0.0.0.0"]
