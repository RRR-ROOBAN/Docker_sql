FROM python:3.11
WORKDIR /sql_process
copy requirements.txt .
copy DataTransfer.py .
RUN pip install -r requirements.txt
CMD ["python","DataTransfer.py"]
