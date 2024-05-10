# Vendor Management App

This is a vendor management app built with Django and Docker. It allows users to manage vendors and purchase orders.

## Installation

### Prerequisites
- Docker
- Docker Compose

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bmyantis/vendor_backend.git
   cd vendor-management-app
2. **Build the Docker image:**
    docker-compose build
3. **Start the Docker containers:**
    docker-compose up
4. **Run Migrations:**
    - docker exec -it <container_id> bash
    - python manage.py migrate
5. **Create a new user:**
    curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' http://localhost:8000/api/auth/users/
6. **Obtain authentication token:**
    - curl -X POST -H "Content-Type: application/json" -d '{"username": "your-username", "password": "your-password"}' http://localhost:8000/api/auth/token/login/
    - Copy the authentication token from the response.

### Usage
- With the authentication token obtained, you can manage vendors and purchase orders using the following endpoints:
    - Vendors: http://localhost:8000/api/vendors/
    - Purchase Orders: http://localhost:8000/api/purchase_orders/
- Use the token in the Authorization header for authentication:
curl -H "Authorization: Token your-auth-token" http://localhost:8000/api/vendors/

### API Endpoints
- `/api/auth/users/`: User registration endpoint.
- `/api/auth/token/login/`: Obtain authentication token endpoint.
- `/api/vendors/`: Vendors management endpoint.
- `/api/vendors/<id>/performance`: Vendors performance endpoint.
- `/api/purchase_orders/`: Purchase orders management endpoint.
- `/api/purchase_orders/<1>/acknowledge/`: Purchase orders acknowledge  endpoint.

## Run Unit Test
- run `docker exec -it <container id> bash`
- run `coverage run --source='.' manage.py test tests/`
- run `coverage report`