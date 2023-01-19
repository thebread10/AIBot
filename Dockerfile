FROM python:3.8
WORKDIR /bot/
COPY . /bot/
RUN pip3 install -r ./requirements.txt
RUN pip3 install discord
CMD python ./main.py
