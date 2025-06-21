from datetime import datetime, timezone
from typing import List
from src.models import EC2Instance, InstanceState, InstanceType, AWSRegion


def get_mock_instances() -> List[EC2Instance]:
    """Retorna una lista de instancias EC2 simuladas"""
    return [
        EC2Instance(
            id="i-1234567890abcdef0",
            name="web-server-prod",
            type=InstanceType.T3_MEDIUM,
            state=InstanceState.RUNNING,
            region=AWSRegion.US_EAST_1,
            launch_time="2024-01-15T10:30:00Z",
            private_ip="10.0.1.10",
            public_ip="54.123.45.67"
        ),
        EC2Instance(
            id="i-0987654321fedcba0",
            name="database-server",
            type=InstanceType.M5_LARGE,
            state=InstanceState.RUNNING,
            region=AWSRegion.US_EAST_1,
            launch_time="2024-01-10T08:15:00Z",
            private_ip="10.0.1.20",
            public_ip="34.567.89.123"
        ),
        EC2Instance(
            id="i-abcdef1234567890",
            name="test-environment",
            type=InstanceType.T2_MICRO,
            state=InstanceState.STOPPED,
            region=AWSRegion.US_WEST_2,
            launch_time="2024-01-20T14:45:00Z",
            private_ip="10.0.2.10",
            public_ip=None
        ),
        EC2Instance(
            id="i-fedcba0987654321",
            name="monitoring-server",
            type=InstanceType.T3_SMALL,
            state=InstanceState.RUNNING,
            region=AWSRegion.EU_WEST_1,
            launch_time="2024-01-12T09:20:00Z",
            private_ip="10.0.3.10",
            public_ip="52.789.12.345"
        ),
        EC2Instance(
            id="i-5678901234abcdef",
            name="backup-server",
            type=InstanceType.C5_LARGE,
            state=InstanceState.STOPPING,
            region=AWSRegion.AP_SOUTHEAST_1,
            launch_time="2024-01-18T16:30:00Z",
            private_ip="10.0.4.10",
            public_ip="13.456.78.90"
        )
    ]


# Simulamos una base de datos en memoria
MOCK_INSTANCES_DB = {instance.id: instance for instance in get_mock_instances()}
