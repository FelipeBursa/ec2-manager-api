from enum import Enum


class InstanceState(str, Enum):
    """Estados posibles de una instancia EC2"""
    PENDING = "pending"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting-down"
    TERMINATED = "terminated"
    STOPPING = "stopping"
    STOPPED = "stopped"


class InstanceType(str, Enum):
    """Tipos de instancia EC2 más comunes"""
    T2_MICRO = "t2.micro"
    T2_SMALL = "t2.small"
    T2_MEDIUM = "t2.medium"
    T3_MICRO = "t3.micro"
    T3_SMALL = "t3.small"
    T3_MEDIUM = "t3.medium"
    M5_LARGE = "m5.large"
    M5_XLARGE = "m5.xlarge"
    C5_LARGE = "c5.large"
    C5_XLARGE = "c5.xlarge"
