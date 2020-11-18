import enum
from pydantic import BaseModel
from typing import List, Optional, Dict, Union


class InterfaceParams(BaseModel):
    id: str
    ipv4_address: str
    ipv4_prefix_len: int


class InterfaceValues(BaseModel):
    interfaces: List[InterfaceParams]


class StaticRouteParams(BaseModel):
    id: str
    dst_ip: str
    dst_prefix_len: str
    device: str
    gateway: str


class StaticRouteValues(BaseModel):
    static_routes: List[StaticRouteParams]


class DeviceAuth(BaseModel):
    hostname: str
    username: str
    password: str
    device_type: str
    firmware_version: str
    configuration: Optional[
        Union[
            InterfaceValues,
            StaticRouteValues
        ]
    ]


class Device(BaseModel):
    device: DeviceAuth