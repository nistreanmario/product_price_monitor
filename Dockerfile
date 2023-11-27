FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /product_price_manager

COPY . /product_price_manager

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8003

CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]
