FROM python:3.9

WORKDIR /usr/src/app
ENV CALDAV_CALENDAR=Abseits

COPY ./app ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]