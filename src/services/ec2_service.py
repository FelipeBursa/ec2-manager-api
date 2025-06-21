import boto3
from typing import List, Optional
from moto import mock_ec2
from src.models import (
    EC2Instance, 
    InstanceState, 
    InstanceType, 
    AWSRegion,
    StopInstanceResponse
)
from src.utils.mock_data import MOCK_INSTANCES_DB
import logging

logger = logging.getLogger(__name__)


class EC2Service:
    """Servicio para operaciones EC2 usando boto3 con mocks"""
    
    def __init__(self):
        self.ec2_client = None
        self._setup_mock_environment()
    
    @mock_ec2
    def _setup_mock_environment(self):
        """Configura el entorno mock de EC2"""
        self.ec2_client = boto3.client('ec2', region_name='us-east-1')
        logger.info("Mock EC2 environment configured")
    
    def get_all_instances(self) -> List[EC2Instance]:
        """
        Retorna todas las instancias EC2 simuladas
        """
        try:
            logger.info("Fetching all EC2 instances")
            instances = list(MOCK_INSTANCES_DB.values())
            return instances
        except Exception as e:
            logger.error(f"Error fetching instances: {str(e)}")
            raise
    
    def get_instance_by_id(self, instance_id: str) -> Optional[EC2Instance]:
        """
        Busca una instancia por su ID
        
        Args:
            instance_id (str): ID de la instancia
            
        Returns:
            Optional[EC2Instance]: La instancia si existe, None en caso contrario
        """
        try:
            logger.info(f"Fetching instance with ID: {instance_id}")
            instance = MOCK_INSTANCES_DB.get(instance_id)
            if instance:
                logger.info(f"Instance found: {instance.name}")
            else:
                logger.warning(f"Instance not found: {instance_id}")
            return instance
        except Exception as e:
            logger.error(f"Error fetching instance {instance_id}: {str(e)}")
            raise
    
    def stop_instance(self, instance_id: str) -> StopInstanceResponse:
        """
        Simula detener una instancia EC2
        
        Args:
            instance_id (str): ID de la instancia a detener
            
        Returns:
            StopInstanceResponse: Respuesta con el resultado de la operación
            
        Raises:
            ValueError: Si la instancia no existe o no se puede detener
        """
        try:
            logger.info(f"Attempting to stop instance: {instance_id}")
            
            # Verificar si la instancia existe
            instance = MOCK_INSTANCES_DB.get(instance_id)
            if not instance:
                raise ValueError(f"Instance {instance_id} not found")
            
            previous_state = instance.state
            
            # Verificar si la instancia se puede detener
            if instance.state == InstanceState.STOPPED:
                return StopInstanceResponse(
                    success=False,
                    message=f"Instance {instance_id} is already stopped",
                    instance_id=instance_id,
                    previous_state=previous_state,
                    current_state=instance.state
                )
            
            if instance.state in [InstanceState.STOPPING, InstanceState.SHUTTING_DOWN]:
                return StopInstanceResponse(
                    success=False,
                    message=f"Instance {instance_id} is already stopping",
                    instance_id=instance_id,
                    previous_state=previous_state,
                    current_state=instance.state
                )
            
            if instance.state == InstanceState.TERMINATED:
                return StopInstanceResponse(
                    success=False,
                    message=f"Instance {instance_id} is terminated and cannot be stopped",
                    instance_id=instance_id,
                    previous_state=previous_state,
                    current_state=instance.state
                )
            
            # Simular el proceso de detener la instancia
            if instance.state == InstanceState.RUNNING:
                # Cambiar estado a "stopping"
                instance.state = InstanceState.STOPPING
                MOCK_INSTANCES_DB[instance_id] = instance
                
                logger.info(f"Instance {instance_id} state changed from {previous_state} to {instance.state}")
                
                return StopInstanceResponse(
                    success=True,
                    message=f"Instance {instance_id} is now stopping",
                    instance_id=instance_id,
                    previous_state=previous_state,
                    current_state=instance.state
                )
            
            # Para otros estados, intentar detener directamente
            instance.state = InstanceState.STOPPED
            MOCK_INSTANCES_DB[instance_id] = instance
            
            logger.info(f"Instance {instance_id} stopped successfully")
            
            return StopInstanceResponse(
                success=True,
                message=f"Instance {instance_id} stopped successfully",
                instance_id=instance_id,
                previous_state=previous_state,
                current_state=instance.state
            )
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error stopping instance {instance_id}: {str(e)}")
            raise RuntimeError(f"Failed to stop instance {instance_id}: {str(e)}")
    
    def simulate_state_transition(self, instance_id: str):
        """
        Simula la transición de estado de stopping a stopped
        Esta función podría ser llamada por un job en segundo plano
        
        Args:
            instance_id (str): ID de la instancia
        """
        try:
            instance = MOCK_INSTANCES_DB.get(instance_id)
            if instance and instance.state == InstanceState.STOPPING:
                instance.state = InstanceState.STOPPED
                MOCK_INSTANCES_DB[instance_id] = instance
                logger.info(f"Instance {instance_id} transitioned from stopping to stopped")
        except Exception as e:
            logger.error(f"Error during state transition for {instance_id}: {str(e)}")


# Instancia global del servicio
ec2_service = EC2Service()
