# use Python 3.12 slim image
FROM python:3.12-slim

# set working directory
WORKDIR /app

# copy dependency file
COPY requirements.txt .

# install package
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY app.py .

# expose port
EXPOSE 8000

# run app (use uvicorn)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

