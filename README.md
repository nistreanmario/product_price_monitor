# Product Price Monitor

This is the API documentation for the Product Price Monitor project. The API is built using Django REST framework and runs inside a Docker container.

## Endpoints

### Products

#### Get all products

- **Endpoint:** `/products/`
- **Method:** `GET`
- **Description:** Get a list of all products.

#### Create a new product

- **Endpoint:** `/products/`
- **Method:** `POST`
- **Description:** Create a new product.

#### Update a product

- **Endpoint:** `/products/{product_id}/`
- **Method:** `PUT`
- **Description:** Update details of a specific product. If your start_date & end_date will match any existing product's price date range, it will change it's price value. In case if any of start_date or end_date overlaps with any product's existing price date range, it will raise an error, if no will create a new price range

#### Partially update a product

- **Endpoint:** `/products/{product_id}/`
- **Method:** `PATCH`
- **Description:** Partially update details of a specific product.

### Calculate Average Price

#### Get average price for a product in a date range

- **Endpoint:** `/products/{product_id}/calculate_average/`
- **Method:** `GET`
- **Description:** Calculate the average price for a product within a specified date range.

## Docker Setup

1. Clone the repository.
2. Build and Run: `docker compose up -d`
3. Run migrations: `docker exec -it ppm-api python manage.py migrate`
4. Create your superuser: `docker exec -it ppm-api python manage.py createsuperuser`
5. You're good to go

The API will be accessible at [http://localhost:8003/swagger/](http://localhost:8003/swagger/)


