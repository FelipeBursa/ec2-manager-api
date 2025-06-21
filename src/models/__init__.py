"""Modelos de datos de la aplicación"""

# Domain: Instance
from .instance import (
    EC2Instance,
    StopInstanceResponse,
    ErrorResponse,
    InstanceState,
    InstanceType,
)

# Shared
from .shared.aws import AWSRegion

__all__ = [
    # Instance domain
    "EC2Instance",
    "StopInstanceResponse",
    "ErrorResponse",
    "InstanceState",
    "InstanceType",
    # Shared
    "AWSRegion",
]