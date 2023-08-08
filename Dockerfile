FROM python:3.9

COPY requirements.txt .

# Set encoding to UTF-8
ENV PYTHONIOENCODING="UTF-8"
ENV LANG="C.UTF-8"

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /usr/app
