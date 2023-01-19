FROM python:3.8
WORKDIR /bot/
COPY . /bot/
RUN pip install -r ./requirements.txt
RUN pip install discord.py
CMD python ./main.py
