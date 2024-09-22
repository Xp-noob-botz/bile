FROM python:3.10
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
RUN pip install motor==2.5.1 pymongo==3.12.3
CMD ["python3", "bot.py"]
