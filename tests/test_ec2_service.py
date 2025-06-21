import pytest
from unittest.mock import Mock, patch
from src.services.ec2_service import EC2Service
from src.models import InstanceState, InstanceType, AWSRegion
from src.utils.mock_data import MOCK_INSTANCES_DB


class TestEC2Service:
    """Tests para el servicio EC2"""
    
    def setup_method(self):
        """Configuración antes de cada test"""
        self.ec2_service = EC2Service()
        # Resetear el estado de los datos mock
        from src.utils.mock_data import get_mock_instances
        global MOCK_INSTANCES_DB
        MOCK_INSTANCES_DB.clear()
        MOCK_INSTANCES_DB.update({instance.id: instance for instance in get_mock_instances()})
    
    def test_get_all_instances(self):
        """Test para obtener todas las instancias"""
        instances = self.ec2_service.get_all_instances()
        
        assert len(instances) == 5
        assert all(hasattr(instance, 'id') for instance in instances)
        assert all(hasattr(instance, 'name') for instance in instances)
        assert all(hasattr(instance, 'type') for instance in instances)
        assert all(hasattr(instance, 'state') for instance in instances)
        assert all(hasattr(instance, 'region') for instance in instances)
    
    def test_get_instance_by_id_exists(self):
        """Test para obtener una instancia que existe"""
        instance_id = "i-1234567890abcdef0"
        instance = self.ec2_service.get_instance_by_id(instance_id)
        
        assert instance is not None
        assert instance.id == instance_id
        assert instance.name == "web-server-prod"
        assert instance.type == InstanceType.T3_MEDIUM
        assert instance.state == InstanceState.RUNNING
        assert instance.region == AWSRegion.US_EAST_1
    
    def test_get_instance_by_id_not_exists(self):
        """Test para obtener una instancia que no existe"""
        instance_id = "i-nonexistent"
        instance = self.ec2_service.get_instance_by_id(instance_id)
        
        assert instance is None
    
    def test_stop_running_instance(self):
        """Test para detener una instancia en ejecución"""
        instance_id = "i-1234567890abcdef0"
        
        # Verificar estado inicial
        instance = self.ec2_service.get_instance_by_id(instance_id)
        assert instance.state == InstanceState.RUNNING
        
        # Detener la instancia
        result = self.ec2_service.stop_instance(instance_id)
        
        assert result.success is True
        assert result.instance_id == instance_id
        assert result.previous_state == InstanceState.RUNNING
        assert result.current_state == InstanceState.STOPPING
        assert "stopping" in result.message.lower()
        
        # Verificar que el estado cambió en la "base de datos"
        updated_instance = self.ec2_service.get_instance_by_id(instance_id)
        assert updated_instance.state == InstanceState.STOPPING
    
    def test_stop_already_stopped_instance(self):
        """Test para detener una instancia ya detenida"""
        instance_id = "i-abcdef1234567890"  # Esta instancia está STOPPED
        
        result = self.ec2_service.stop_instance(instance_id)
        
        assert result.success is False
        assert result.instance_id == instance_id
        assert result.previous_state == InstanceState.STOPPED
        assert result.current_state == InstanceState.STOPPED
        assert "already stopped" in result.message.lower()
    
    def test_stop_nonexistent_instance(self):
        """Test para detener una instancia que no existe"""
        instance_id = "i-nonexistent"
        
        with pytest.raises(ValueError) as exc_info:
            self.ec2_service.stop_instance(instance_id)
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_stop_stopping_instance(self):
        """Test para detener una instancia que ya se está deteniendo"""
        instance_id = "i-5678901234abcdef"  # Esta instancia está STOPPING
        
        result = self.ec2_service.stop_instance(instance_id)
        
        assert result.success is False
        assert result.instance_id == instance_id
        assert result.previous_state == InstanceState.STOPPING
        assert result.current_state == InstanceState.STOPPING
        assert "already stopping" in result.message.lower()
    
    def test_simulate_state_transition(self):
        """Test para la transición de estado de stopping a stopped"""
        instance_id = "i-5678901234abcdef"  # Esta instancia está STOPPING
        
        # Verificar estado inicial
        instance = self.ec2_service.get_instance_by_id(instance_id)
        assert instance.state == InstanceState.STOPPING
        
        # Simular transición
        self.ec2_service.simulate_state_transition(instance_id)
        
        # Verificar que cambió a STOPPED
        updated_instance = self.ec2_service.get_instance_by_id(instance_id)
        assert updated_instance.state == InstanceState.STOPPED
    
    @patch('src.services.ec2_service.logger')
    def test_logging_get_instances(self, mock_logger):
        """Test para verificar que se registran los logs correctamente"""
        self.ec2_service.get_all_instances()
        
        mock_logger.info.assert_called()
        # Verificar que se llamó al menos una vez con el mensaje esperado
        info_calls = [call.args[0] for call in mock_logger.info.call_args_list]
        assert any("Fetching all EC2 instances" in call for call in info_calls)
    
    @patch('src.services.ec2_service.logger')
    def test_logging_stop_instance(self, mock_logger):
        """Test para verificar logging en stop_instance"""
        instance_id = "i-1234567890abcdef0"
        self.ec2_service.stop_instance(instance_id)
        
        mock_logger.info.assert_called()
        info_calls = [call.args[0] for call in mock_logger.info.call_args_list]
        assert any(f"Attempting to stop instance: {instance_id}" in call for call in info_calls)
