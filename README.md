
# Blog Post API

A FastAPI-based Blog Post API with authentication, caching using Redis, and reverse proxy using NGINX.

## Features
- Create, read, update, and delete (CRUD) blog posts.
- User authentication and authorization.
- Caching with Redis to improve performance.
- NGINX as a reverse proxy for better scalability and security.

## Project Structure
```
blog_post/
├── .env                     # Environment variables
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Python dependencies
├── blog_api/                # Blog API related files
├── core/                    # Core configurations
├── db/                      # Database session and setup
├── nginx/                   # NGINX configuration
└── user_api/                # User authentication and API
```

## Setup Instructions

### 1. Clone the repository
```sh
extract the blog_post.zip
```

### 2. Create a `.env` file
Create a `.env` file based on the provided `.env.example` file.

### 3. Start the services with Docker Compose
```sh
docker-compose up --build
```

### 4. Access the API
- FastAPI Docs (Swagger UI): [http://localhost/docs](http://localhost/docs)
- Redoc: [http://localhost/redoc](http://localhost/redoc)

### 5. Endpoints Overview
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /blogs/  | Get all blogs |
| GET    | /blogs/{blog_id} | Get a specific blog by ID |
| POST   | /blogs/create | Create a new blog |
| PUT    | /blogs/update/{blog_id} | Update an existing blog |
| DELETE | /blogs/delete/{blog_id} | Delete a blog |

### 6. Run Tests (Optional)
```sh
pytest
```

## NGINX Configuration
- NGINX configuration is located at `nginx/nginx.conf`.
- NGINX listens on port `80` and proxies requests to FastAPI.

## Caching
- Redis is used for caching responses.
- TTL is set for better performance and to reduce database load.

## License
This project is licensed under the MIT License.
