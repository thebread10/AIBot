FROM python:3.8
WORKDIR /bot/
COPY . /bot/
RUN pip install -r requirements.txt
CMD python main.py
