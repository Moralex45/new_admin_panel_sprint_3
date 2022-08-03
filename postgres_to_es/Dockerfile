FROM python:3.9.7-buster
WORKDIR /data
EXPOSE 8000
COPY ./requirements.txt /data
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /data
CMD python /data/load_data.py