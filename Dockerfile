FROM node:24-alpine AS frontend-builder

WORKDIR /app/frontend

COPY app/frontend/package*.json ./

RUN npm install

COPY app/frontend/ .

COPY modeling/eda/output/*.png /app/frontend/src/assets/
COPY modeling/eda/output/single_distributions/*.png /app/frontend/src/assets/
COPY ref.json /app/frontend/src

RUN npm run build

FROM python:3.13-slim AS backend

WORKDIR /app

COPY app/app.py ./

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

COPY modeling/linear_model.pkl /app
COPY modeling/preprocessor/output/joined_out.csv /app

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
