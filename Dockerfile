FROM python:3.8.16-slim
COPY . /chat_app
WORKDIR /chat_app
RUN pip install -r requirmnd.txt
EXPOSE 5000
ENTRYPOINT python3 chat.py
