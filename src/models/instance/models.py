from typing import Optional
from pydantic import BaseModel, ConfigDict

from .types import InstanceState, InstanceType
from ..shared.aws import AWSRegion


class EC2Instance(BaseModel):
    """Modelo core para una instancia EC2"""
    model_config = ConfigDict(use_enum_values=True)
    
    id: str
    name: str
    type: InstanceType
    state: InstanceState
    region: AWSRegion
    launch_time: Optional[str] = None
    private_ip: Optional[str] = None
    public_ip: Optional[str] = None
