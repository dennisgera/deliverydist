from unittest.mock import patch

def test_calculate_distance_success(client):
    test_payload = {
        "source_address": "New York, NY",
        "destination_address": "Los Angeles, CA"
    }
    
    # Mock the geocoding and distance calculation services
    with patch('app.services.geocoding.GeocodingService.get_coordinates') as mock_geocoding:
        with patch('app.services.distance_calculator.DistanceCalculatorService.calculate_distance') as mock_distance:
            # Set up mock returns
            mock_geocoding.side_effect = [(40.7128, -74.0060), (34.0522, -118.2437)]
            mock_distance.return_value = 3935.75
            
            response = client.post("/api/v1/queries/", json=test_payload)
            
            assert response.status_code == 200
            assert response.json()["distance"] == 3935.75
            assert response.json()["source_address"] == test_payload["source_address"]
            assert response.json()["destination_address"] == test_payload["destination_address"]

def test_calculate_distance_invalid_address(client):
    test_payload = {
        "source_address": "Invalid Address",
        "destination_address": "Los Angeles, CA"
    }
    
    with patch('app.services.geocoding.GeocodingService.get_coordinates') as mock_geocoding:
        mock_geocoding.side_effect = Exception("Address not found")
        
        response = client.post("/api/v1/queries/", json=test_payload)
        
        assert response.status_code == 500
        assert "Error processing query" in response.json()["detail"]

def test_get_query_history(client):
    # First create some test data
    test_queries = [
        {
            "source_address": "New York, NY",
            "destination_address": "Los Angeles, CA"
        },
        {
            "source_address": "Chicago, IL",
            "destination_address": "Houston, TX"
        }
    ]
    
    # Mock services and create test queries
    with patch('app.services.geocoding.GeocodingService.get_coordinates') as mock_geocoding:
        with patch('app.services.distance_calculator.DistanceCalculatorService.calculate_distance') as mock_distance:
            mock_geocoding.return_value = (0, 0)
            mock_distance.return_value = 1000
            
            for query in test_queries:
                client.post("/api/v1/queries/", json=query)
    
    # Test get history endpoint
    response = client.get("/api/v1/queries/")
    
    assert response.status_code == 200
    assert len(response.json()) == len(test_queries)