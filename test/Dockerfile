# Container-Name: docker-brainrot-test-app
# Port-Map: 8049:8049

FROM python:3.9-slim
WORKDIR /app
COPY ./html /app
CMD ["python", "-m", "http.server", "8049"]
EXPOSE 8049