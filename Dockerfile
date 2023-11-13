# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /product_price_manager
WORKDIR /product_price_manager

# Copy the current directory contents into the container at /product_price_manager
COPY . /product_price_manager

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 8003 available to the world outside this container
EXPOSE 8003

# Define environment variable for Django (uncomment if running in production)
# ENV DJANGO_SETTINGS_MODULE=product_price_manager.settings.production

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]
