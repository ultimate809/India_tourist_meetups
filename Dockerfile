# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure that Python output is displayed in the terminal
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY ultimate_meetup /app/

# Delete existing migration files
RUN find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Expose the port on which Django will run
EXPOSE 8000

# Run migrations, create superuser, and start the server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]