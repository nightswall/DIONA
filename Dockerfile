# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Set the environment variable for the Django settings module
ENV DJANGO_SETTINGS_MODULE myproject.settings

# Run any necessary database migrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
