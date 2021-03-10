# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /order_tracking

# Install dependencies
COPY Pipfile Pipfile.lock /order_tracking/
RUN pip install pipenv && pipenv install --system


# Copy project
COPY . /bookstore_project/
