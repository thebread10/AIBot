FROM python:3.8
COPY . .
RUN pip install -r requirements.txt
CMD python3 main.py
