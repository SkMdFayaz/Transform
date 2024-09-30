# Project Setup

This guide will walk you through the process of setting up the project locally, including initializing Git, pulling the latest branch, setting up Docker Compose, running migrations, and accessing the application.

## Prerequisites

- Docker
- Docker Compose
- Git
- Postman (for testing APIs)

---

## Step 1: Initialize Git and Pull the Project

1. **Clone the Repository:**

   If you haven't already, initialize a Git repository and pull the latest branch of the project.

   ```bash
   git init
   git remote add origin https://github.com/SkMdFayaz/Transform.git
   git clone https://github.com/SkMdFayaz/Transform.git
   git pull origin feat/transformer

## Step 2: Docker Setup

1. **Stack up**
   Go to the path where there is docker_compose.yml
   do docker compose up -d 
2. Do docker ps -a to check all the containers are up and running
3. Once all the containers are up and running run following command for db migrations
   docker-compose exec web python manage.py migrate
4. To check the logs make use of command docker logs -f <container-id>
5. Please import the collections in postman
6. Perform all the request present in the collections and do refer the examples for testing the apis 
