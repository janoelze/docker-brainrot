# Container-Name: docker-brainrot-test-app
# Port-Map: 8000:8000

FROM python:3.9-slim
WORKDIR /app
COPY ./html /app
ADD https://place-hold.it/100x100 /app/logo.png
CMD ["python", "-m", "http.server", "8000"]
EXPOSE 8000