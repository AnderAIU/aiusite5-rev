FROM python:3.11.1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . ./aiusite5-rev
WORKDIR ./aiusite5-rev
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
COPY . .