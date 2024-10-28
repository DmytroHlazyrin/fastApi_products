import pytest
from fastapi import status

from tests.conftest import init_data


@pytest.fixture
def new_category_data():
    return {"name": "Test Category", "parent_id": None}


@pytest.fixture
def new_subcategory_data():
    return {"name": "Test Subcategory", "parent_id": 1}

def test_read_categories(client, init_data, initial_data):
    response = client.get("/categories/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == initial_data["categories"][0]["name"]


def test_create_category(client, new_category_data):
    response = client.post("/categories/", json=new_category_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == new_category_data["name"]
    assert "id" in data


def test_create_subcategory(client, new_subcategory_data):
    response = client.post("/categories/", json=new_subcategory_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == new_subcategory_data["name"]
    assert data["parent_id"] == new_subcategory_data["parent_id"]
    assert "id" in data


def test_not_create_category_with_same_name(client, new_category_data):
    response = client.post("/categories/", json=new_category_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Category already exists"




def test_read_category(client, initial_data):
    category_id = 1
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == initial_data["categories"][0]["name"]


def test_update_category(client):
    category_id = 11
    updated_data = {"name": "Updated Category"}
    response = client.patch(f"/categories/{category_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Category"


def test_delete_category(client):
    category_id = 11
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(f"/categories/{category_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_read_categories_with_pagination(client, initial_data):
    response = client.get("/categories/?limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert initial_data["categories"][0]["name"] in [item["name"] for item in data]
    assert len(data) == 2

    response = client.get("/categories/?skip=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert initial_data["categories"][0]["name"] not in [item["name"] for item in data]
    assert len(data) == 9

    response = client.get("/categories/?limit=2&skip=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert initial_data["categories"][0]["name"] not in [item["name"] for item in data]
    assert len(data) == 2


@pytest.mark.parametrize("sort_by, sort_order", [
    ("name", "asc"),
    ("name", "desc"),
    ("id", "asc"),
    ("id", "desc"),
])
def test_read_categories_with_sorting(client, sort_by, sort_order):
    params = {"sort_by": sort_by, "sort_order": sort_order}
    response = client.get("/categories/", params=params)
    assert response.status_code == 200
    data = response.json()

    if sort_by == "name":
        sorted_data = sorted(data, key=lambda x: x["name"], reverse=(sort_order == "desc"))
    else:
        sorted_data = sorted(data, key=lambda x: x["id"], reverse=(sort_order == "desc"))
    assert data == sorted_data, f"Categories should be sorted by {sort_by} in {sort_order} order"
