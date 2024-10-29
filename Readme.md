# FastAPI Product & Category Management Application

This FastAPI-based application manages products and categories, utilizing SQLAlchemy for ORM and Alembic for database migrations. 
The application supports full CRUD operations with built-in validation, error handling, and logging for key actions.

## Features

- Comprehensive CRUD operations for both categories and products.
- Data validation, including checks to ensure product prices are positive and category names are non-empty.
- Robust error handling for issues such as resource not found and validation failures.
- Logging of important events, like product creation and category deletion.

## Project Structure

The core components of the project include:

- **`models.py`**: Defines the SQLAlchemy models for `Product` and `Category`.
- **`schemas.py`**: Contains Pydantic schemas for data validation.
- **`crud.py`**: Provides CRUD functions for database interaction.
- **`main.py`**: Sets up FastAPI endpoints.
- **`database.py`**: Configures the database connection.
- **`alembic/`**: Directory containing Alembic database migrations.

## Getting Started

### Prerequisites

Ensure you have Python 3.9+ and a PostgreSQL database, as well as the dependencies listed in `requirements.txt`.

### Installation

1. Clone the repository and navigate to the project directory:

```shell
git clone https://github.com/DmytroHlazyrin/fastApi_products
cd fastApi_products
```

2. Install dependencies:

```shell
pip install -r requirements.txt
```
3. Configure environment variables: Create a .env file with your PostgreSQL configuration. There is sample in .env.sample.

### Database Setup and Migrations

1. Initialize the database: Ensure the database is created in PostgreSQL:
```shell
psql -U postgres -c "CREATE DATABASE products;"
```

2. Apply migrations:
```shell
alembic upgrade head
```

If you have problems with using migrations, delete migrations and reinitialize your own:
```shell
alembic revision --autogenerate -m "Initial migration"
```

## Running the Application
To start the FastAPI application, use the following command:
```shell
uvicorn main:app --reload
```
The API will be accessible at http://127.0.0.1:8000.
The docs will be accessible at http://127.0.0.1:8000/docs and at http://127.0.0.1:8000/redoc.

## Running Tests
To run tests, use:
```shell
pytest
```
During testing, the logger will be disabled to prevent log files from being generated.

## API Endpoints
* Categories

    * POST /categories/: Create a new category.
    * GET /categories/: List all categories with pagination and sorting.
    * GET /categories/{category_id}: Retrieve a specific category by ID.
    * PATCH /categories/{category_id}: Update a category.
    * DELETE /categories/{category_id}: Delete a category along with its subcategories and products.

* Products

    * POST /products/: Create a new product.
    * GET /products/: List all products with pagination, sorting, and optional category filter.
    * GET /products/{product_id}: Retrieve a specific product by ID.
    * PATCH /products/{product_id}: Update a product.
    * DELETE /products/{product_id}: Delete a product.
