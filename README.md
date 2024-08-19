# flaskLogs

# Flask Application with Docker and Snowflake Integration

This is a Flask application that connects to Snowflake to retrieve and display log data. The application uses Docker for containerization.

## Prerequisites

- Docker installed on your machine.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/<USERNAME>/<REPOSITORY>.git
   cd <REPOSITORY>
docker build -t my-flask-app .
docker run -d -p 5000:5000 --name flask-app my-flask-app
