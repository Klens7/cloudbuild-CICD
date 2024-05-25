import pytest
from unittest.mock import patch,MagicMock
from main import app, client as app_client

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
# methods load table from uri and get table are part of bigquery python sdk 
@patch.object(app_client,'load_table_from_uri')
@patch.object(app_client,'get_table')
# main fixture method, runs test for number of rows
def test_main_endpoint(mock_get_table, mock_load_table_from_uri, client):
    mock_load_job = MagicMock()
    mock_load_table_from_uri.return_value = mock_load_job

    mock_table = MagicMock()
    # number of rows in our csv is 50
    mock_table.num_rows = 50
    mock_get_table.return_value = mock_table

    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert data['data'] == 50
    
    mock_load_table_from_uri.assert_called_once()
    mock_load_job.result.assert_called_once()
    mock_get_table.assert_called_once()

#### in order to run it, LS to test_main.py,
# in command line below, put in    pytest test_main.py   then enter
# it should run 1 test case, and it will say passed
# unit test complete