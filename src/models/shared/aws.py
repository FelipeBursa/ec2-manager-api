from enum import Enum


class AWSRegion(str, Enum):
    """Regiones AWS principales - Compartidas entre servicios"""
    US_EAST_1 = "us-east-1"
    US_WEST_1 = "us-west-1"
    US_WEST_2 = "us-west-2"
    EU_WEST_1 = "eu-west-1"
    EU_CENTRAL_1 = "eu-central-1"
    AP_SOUTHEAST_1 = "ap-southeast-1"
    AP_NORTHEAST_1 = "ap-northeast-1"
    SA_EAST_1 = "sa-east-1"
