FROM tailordev/pandas as base 
# escape=` (backtick)

FROM base as builder 

RUN pip install --upgrade pip

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /install

RUN pip install -r requirements.txt

FROM base 

RUN mkdir /scoreboard
WORKDIR /scoreboard

ADD scoreboard.py /scoreboard

CMD ["python", "scoreboard.py"]