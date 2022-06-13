FROM python:3.10-alpine
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"] 
