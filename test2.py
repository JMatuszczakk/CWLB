import json
import pytest
from playwright.sync_api import Page, expect
import requests

BASE_URL = 'http://localhost:5000'

@pytest.fixture(scope='module')
def sample_dog():
    """Fixture to provide sample dog data for testing"""
    return {
        'name': 'TestDog',
        'race': 'Test Breed',
        'color': 'Test Color',
        'photo': 'test_photo.jpg',
        'number': '999999',
        'illnesses': 'None'
    }

def test_home_page_exists(page: Page):
    """Test that the home page loads correctly"""
    page.goto(BASE_URL)
    expect(page).to_have_title('')  
    expect(page.locator('body')).to_contain_text('Witamy w API Schroniska dla Psów!')

def test_get_dogs_api(sample_dog):
    """Test retrieving dogs via API"""
    add_response = requests.post(f'{BASE_URL}/api/dogs/addDog', json=sample_dog)
    assert add_response.status_code == 201

    get_response = requests.get(f'{BASE_URL}/api/dogs')
    assert get_response.status_code == 200

    dogs = get_response.json()
    added_dog = next((dog for dog in dogs if dog['name'] == sample_dog['name']), None)
    assert added_dog is not None
    assert added_dog['race'] == sample_dog['race']

def test_add_dog_api(sample_dog):
    """Test adding a new dog via API"""
    response = requests.post(f'{BASE_URL}/api/dogs/addDog', json=sample_dog)
    
    assert response.status_code == 201
    assert response.json()['message'] == 'Pies dodany pomyślnie!'

def test_delete_dog_api(sample_dog):
    """Test deleting a dog via API"""
    add_response = requests.post(f'{BASE_URL}/api/dogs/addDog', json=sample_dog)
    assert add_response.status_code == 201

    get_response = requests.get(f'{BASE_URL}/api/dogs')
    assert get_response.status_code == 200


    dogs = get_response.json()
    added_dog = next((dog for dog in dogs if dog['name'] == sample_dog['name']), None)
    assert added_dog is not None


    delete_response = requests.post(f'{BASE_URL}/api/dogs/delete', json={'id': added_dog['id']})
    
 
def test_api_routes_exist(page: Page):
    """Test that all expected routes exist"""
    routes = [
        '/',
        '/api/dogs',
        '/api/dogs/addDog',
        '/api/dogs/delete'
    ]

    for route in routes:
        response = requests.get(f'{BASE_URL}{route}')
        assert response.status_code in [200, 405], f"Route {route} failed"

def create_requirements_file():
    """Create a requirements.txt file for the project"""
    requirements = [
        "flask",
        "psycopg2-binary",
        "python-dotenv",
        "pytest",
        "requests",
        "playwright",
    ]
    
    with open('requirements.txt', 'w') as f:
        for req in requirements:
            f.write(f"{req}\n")

