from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models import EC2Instance, StopInstanceResponse, ErrorResponse
from src.services.ec2_service import ec2_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/instances", tags=["instances"])


@router.get(
    "/",
    response_model=List[EC2Instance],
    summary="Obtener todas las instancias EC2",
    description="Retorna una lista de todas las instancias EC2 simuladas con su información completa"
)
async def get_instances():
    """
    Endpoint para obtener todas las instancias EC2.
    
    Returns:
        List[EC2Instance]: Lista de instancias EC2 con id, name, type, state, region
    """
    try:
        logger.info("GET /instances endpoint called")
        instances = ec2_service.get_all_instances()
        logger.info(f"Returning {len(instances)} instances")
        return instances
    except Exception as e:
        logger.error(f"Error in get_instances: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving instances: {str(e)}"
        )


@router.post(
    "/{instance_id}/stop",
    response_model=StopInstanceResponse,
    summary="Detener una instancia EC2",
    description="Simula detener una instancia EC2 específica y retorna el resultado de la operación",
    responses={
        200: {"description": "Instancia detenida exitosamente"},
        404: {"description": "Instancia no encontrada"},
        400: {"description": "No se puede detener la instancia (estado inválido)"},
        500: {"description": "Error interno del servidor"}
    }
)
async def stop_instance(instance_id: str):
    """
    Endpoint para detener una instancia EC2.
    
    Args:
        instance_id (str): ID de la instancia a detener
    
    Returns:
        StopInstanceResponse: Resultado de la operación con mensaje de éxito/fallo
    """
    try:
        logger.info(f"POST /instances/{instance_id}/stop endpoint called")
        
        # Verificar que la instancia existe
        instance = ec2_service.get_instance_by_id(instance_id)
        if not instance:
            logger.warning(f"Instance {instance_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Instance {instance_id} not found"
            )
        
        # Intentar detener la instancia
        result = ec2_service.stop_instance(instance_id)
        
        if result.success:
            logger.info(f"Instance {instance_id} stop operation successful")
            return result
        else:
            logger.warning(f"Instance {instance_id} stop operation failed: {result.message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
            
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"ValueError in stop_instance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in stop_instance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error stopping instance: {str(e)}"
        )


@router.get(
    "/{instance_id}",
    response_model=EC2Instance,
    summary="Obtener una instancia específica",
    description="Retorna la información de una instancia EC2 específica",
    responses={
        200: {"description": "Instancia encontrada"},
        404: {"description": "Instancia no encontrada"}
    }
)
async def get_instance(instance_id: str):
    """
    Endpoint para obtener una instancia específica por ID.
    
    Args:
        instance_id (str): ID de la instancia
    
    Returns:
        EC2Instance: Información de la instancia
    """
    try:
        logger.info(f"GET /instances/{instance_id} endpoint called")
        
        instance = ec2_service.get_instance_by_id(instance_id)
        if not instance:
            logger.warning(f"Instance {instance_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Instance {instance_id} not found"
            )
        
        logger.info(f"Returning instance {instance_id}")
        return instance
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_instance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving instance: {str(e)}"
        )
