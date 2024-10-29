import pytest
from fastapi import status

@pytest.fixture
def new_category_data():
    return {"name": "Test Category Product", "parent_id": None}

@pytest.fixture
def new_product_data():
    return {
        "name": "Test Product",
        "description": "Test Description",
        "price": 9.99,
        "quantity": 10,
        "category_id": 2
    }


def test_create_product(client, new_product_data, new_category_data):
    response = client.post("/categories/", json=new_category_data)
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post("/products/", json=new_product_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == new_product_data["name"]
    assert "id" in data


def test_not_create_product_with_same_name(client, new_product_data):
    response = client.post("/products/", json=new_product_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Product already exists"


def test_read_products(client, initial_data):
    response = client.get("/products/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == initial_data["products"][0]["name"]

def test_read_products_with_category_id(client, initial_data):
    category_id = 1
    response = client.get(f"/products/?category_id={category_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == initial_data["products"][0]["name"]
    assert data[0]["category_id"] == 1


def test_read_product(client, initial_data):
    product_id = 1
    response = client.get(f"/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == initial_data["products"][0]["name"]


def test_update_product(client):
    product_id = 1
    updated_data = {"name": "Updated product"}
    response = client.patch(f"/products/{product_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated product"


def test_delete_product(client):
    product_id = 11
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(f"/products/{product_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_read_products_with_pagination(client, initial_data):
    response = client.get("/products/?limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert initial_data["products"][1]["name"] in [item["name"] for item in data]
    assert len(data) == 2

    response = client.get("/products/?skip=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert initial_data["products"][1]["name"] not in [item["name"] for item in data]
    assert len(data) == 10

    response = client.get("/products/?limit=2&skip=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert initial_data["products"][1]["name"] not in [item["name"] for item in data]
    assert len(data) == 2

@pytest.mark.parametrize("sort_by, sort_order", [
    ("name", "asc"),
    ("name", "desc"),
    ("id", "asc"),
    ("id", "desc"),
    ("price", "asc"),
    ("price", "desc")
])
def test_read_products_with_sorting(client, sort_by, sort_order):
    params = {"sort_by": sort_by, "sort_order": sort_order}
    response = client.get("/products/", params=params)
    assert response.status_code == 200
    data = response.json()

    if sort_by == "name":
        sorted_data = sorted(data, key=lambda x: x["name"], reverse=(sort_order == "desc"))
    elif sort_by == "id":
        sorted_data = sorted(data, key=lambda x: x["id"], reverse=(sort_order == "desc"))
    else:
        sorted_data = sorted(data, key=lambda x: float(x["price"]), reverse=(sort_order == "desc"))
    assert data == sorted_data, f"Products should be sorted by {sort_by} in {sort_order} order"
