# Container-Name: my-cool-app
# Port-Map: 8050:8050

FROM python:3.9-slim
WORKDIR /app
COPY ./html /app
CMD ["python", "-m", "http.server", "8050"]
EXPOSE 8050