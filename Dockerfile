FROM python:3.11
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "-u" ,"main.py"]
