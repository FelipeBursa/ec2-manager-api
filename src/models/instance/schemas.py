from pydantic import BaseModel, ConfigDict

from .types import InstanceState


class StopInstanceResponse(BaseModel):
    """Schema de respuesta para la operación de detener instancia"""
    model_config = ConfigDict(use_enum_values=True)
    
    success: bool
    message: str
    instance_id: str
    previous_state: InstanceState
    current_state: InstanceState


class ErrorResponse(BaseModel):
    """Schema de respuesta de error estándar"""
    error: str
    message: str
    status_code: int
