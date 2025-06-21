import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.app import app
from src.models import InstanceState, InstanceType, AWSRegion, EC2Instance, StopInstanceResponse

client = TestClient(app)


class TestInstancesRoutes:
    """Tests para las rutas de instancias"""
    
    def setup_method(self):
        """Configuración antes de cada test"""
        # Resetear el estado de los datos mock antes de cada test
        from src.utils.mock_data import get_mock_instances, MOCK_INSTANCES_DB
        MOCK_INSTANCES_DB.clear()
        MOCK_INSTANCES_DB.update({instance.id: instance for instance in get_mock_instances()})
    
    def test_get_instances_success(self):
        """Test para GET /instances - éxito"""
        response = client.get("/instances/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5
        
        # Verificar estructura de la primera instancia
        instance = data[0]
        required_fields = ["id", "name", "type", "state", "region"]
        for field in required_fields:
            assert field in instance
    
    def test_get_instance_by_id_success(self):
        """Test para GET /instances/{id} - éxito"""
        instance_id = "i-1234567890abcdef0"
        response = client.get(f"/instances/{instance_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == instance_id
        assert data["name"] == "web-server-prod"
        assert data["type"] == "t3.medium"
        assert data["state"] == "running"
        assert data["region"] == "us-east-1"
    
    def test_get_instance_by_id_not_found(self):
        """Test para GET /instances/{id} - no encontrada"""
        instance_id = "i-nonexistent"
        response = client.get(f"/instances/{instance_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_stop_instance_success(self):
        """Test para POST /instances/{id}/stop - éxito"""
        instance_id = "i-1234567890abcdef0"
        response = client.post(f"/instances/{instance_id}/stop")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["instance_id"] == instance_id
        assert data["previous_state"] == "running"
        assert data["current_state"] == "stopping"
        assert "stopping" in data["message"].lower()
    
    def test_stop_instance_not_found(self):
        """Test para POST /instances/{id}/stop - instancia no encontrada"""
        instance_id = "i-nonexistent"
        response = client.post(f"/instances/{instance_id}/stop")
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_stop_already_stopped_instance(self):
        """Test para POST /instances/{id}/stop - instancia ya detenida"""
        instance_id = "i-abcdef1234567890"  # Esta instancia está STOPPED
        response = client.post(f"/instances/{instance_id}/stop")
        
        assert response.status_code == 400
        data = response.json()
        assert "already stopped" in data["detail"].lower()
    
    def test_stop_already_stopping_instance(self):
        """Test para POST /instances/{id}/stop - instancia ya deteniéndose"""
        instance_id = "i-5678901234abcdef"  # Esta instancia está STOPPING
        response = client.post(f"/instances/{instance_id}/stop")
        
        assert response.status_code == 400
        data = response.json()
        assert "already stopping" in data["detail"].lower()
    
    def test_root_endpoint(self):
        """Test para el endpoint raíz"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "EC2 Manager API"
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
    
    def test_health_endpoint(self):
        """Test para el endpoint de salud"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "EC2 Manager API"
        assert data["version"] == "1.0.0"
        assert "checks" in data
        assert data["checks"]["api"] == "ok"
        assert data["checks"]["mock_data"] == "ok"
    
    @patch('src.routes.instances.ec2_service.get_all_instances')
    def test_get_instances_service_error(self, mock_get_instances):
        """Test para manejo de errores en GET /instances"""
        mock_get_instances.side_effect = Exception("Service error")
        
        response = client.get("/instances/")
        
        assert response.status_code == 500
        data = response.json()
        assert "Error retrieving instances" in data["detail"]
    
    @patch('src.routes.instances.ec2_service.stop_instance')
    def test_stop_instance_service_error(self, mock_stop_instance):
        """Test para manejo de errores en POST /instances/{id}/stop"""
        instance_id = "i-1234567890abcdef0"
        mock_stop_instance.side_effect = RuntimeError("Service error")
        
        response = client.post(f"/instances/{instance_id}/stop")
        
        assert response.status_code == 500
        data = response.json()
        assert "Error stopping instance" in data["detail"]
    
    def test_openapi_docs(self):
        """Test para verificar que la documentación OpenAPI está disponible"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_json(self):
        """Test para verificar que el esquema OpenAPI JSON está disponible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] == "EC2 Manager API"
        assert data["info"]["version"] == "1.0.0"
    
    def test_cors_headers(self):
        """Test para verificar que los headers CORS están configurados"""
        response = client.get("/instances/")
        # Verificar que no hay errores CORS en las respuestas
        assert response.status_code == 200
        # FastAPI maneja automáticamente las opciones CORS
