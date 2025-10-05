FROM node:24-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ .
RUN npm run build

FROM python:3.13-slim AS backend

WORKDIR /app

COPY app.py ./

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=8080

EXPOSE 8080

CMD ["flask", "run", "--port=8080"]
