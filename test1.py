import pytest
import json
from flask import Flask
from app import app, create_connection, fetch_all_dogs, insert_dog, delete_dog
import psycopg2
from unittest.mock import MagicMock, patch

@pytest.fixture
def client():
    """Utwórz klienta testowego dla aplikacji"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db_connection():
    """Symuluj połączenie z bazą danych"""
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_conn, mock_cursor

def test_home_route(client):
    """Testuj trasę główną"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Witamy w API Schroniska dla Psow!" in response.data

def test_create_connection_success():
    """Testuj udane połączenie z bazą danych"""
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        connection = create_connection()
        assert connection is not None
        mock_connect.assert_called_once()

def test_create_connection_failure():
    """Testuj nieudane połączenie z bazą danych"""
    with patch('psycopg2.connect', side_effect=psycopg2.OperationalError):
        connection = create_connection()
        assert connection is None

def test_fetch_all_dogs(mock_db_connection):
    """Testuj pobieranie wszystkich psów"""
    mock_conn, mock_cursor = mock_db_connection
    
    mock_cursor.description = [
        ('id',), ('name',), ('race',), ('color',), 
        ('photo',), ('number',), ('illnesses',)
    ]
    mock_cursor.fetchall.return_value = [
        (1, 'Buddy', 'Labrador', 'Brown', 'photo.jpg', '123', 'None')
    ]
    
    dogs = fetch_all_dogs(mock_cursor)
    
    assert len(dogs) == 1
    assert dogs[0]['name'] == 'Buddy'
    assert dogs[0]['race'] == 'Labrador'

def test_insert_dog(mock_db_connection):
    """Testuj dodawanie nowego psa"""
    mock_conn, mock_cursor = mock_db_connection
    
    dog_data = {
        'name': 'Rex',
        'race': 'Owczarek Niemiecki',
        'color': 'Czarno-Brązowy',
        'photo': 'rex.jpg',
        'number': '456',
        'illnesses': 'Brak'
    }
    
    insert_dog(mock_cursor, dog_data)
    
    mock_cursor.execute.assert_called_once()
    assert 'INSERT INTO dogs' in mock_cursor.execute.call_args[0][0]

def test_delete_dog(mock_db_connection):
    """Testuj usuwanie psa"""
    mock_conn, mock_cursor = mock_db_connection
    
    dog_id = 1
    delete_dog(mock_cursor, dog_id)
    
    mock_cursor.execute.assert_called_once()
    assert 'DELETE FROM dogs' in mock_cursor.execute.call_args[0][0]

def test_get_dogs_route(client, mock_db_connection):
    """Testuj trasę GET /api/dogs"""
    mock_conn, mock_cursor = mock_db_connection
    
    # Konfiguracja kursorka z przykładowymi danymi
    mock_cursor.description = [
        ('id',), ('name',), ('race',), ('color',), 
        ('photo',), ('number',), ('illnesses',)
    ]
    mock_cursor.fetchall.return_value = [
        (1, 'Buddy', 'Labrador', 'Brown', 'photo.jpg', '123', 'None')
    ]
    
    response = client.get('/api/dogs')
    
    assert response.status_code == 200
    dogs = json.loads(response.data)
    assert len(dogs) == 1
    assert dogs[0]['name'] == 'Buddy'

def test_post_dog_route(client, mock_db_connection):
    """Testuj trasę POST /api/dogs/addDog"""
    mock_conn, mock_cursor = mock_db_connection
    
    dog_data = {
        'name': 'Rex',
        'race': 'Owczarek Niemiecki',
        'color': 'Czarno-Brązowy',
        'photo': 'rex.jpg',
        'number': '456',
        'illnesses': 'Brak'
    }
    
    response = client.post('/api/dogs/addDog', 
                           data=json.dumps(dog_data),
                           content_type='application/json')
    
    assert response.status_code == 201
    assert b'Pies dodany pomyslnie!' in response.data