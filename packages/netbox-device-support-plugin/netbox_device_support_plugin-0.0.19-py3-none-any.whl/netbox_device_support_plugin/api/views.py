from netbox.api.viewsets import NetBoxModelViewSet

from .. import models, filtersets
from .serializers import (
    CiscoDeviceSupportSerializer,
    CiscoDeviceTypeSupportSerializer,
    FortinetDeviceSupportSerializer,
)


#### Cisco Support ##########################################################################################


class CiscoDeviceSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoDeviceSupport.objects.all().prefetch_related("device")
    serializer_class = CiscoDeviceSupportSerializer
    filterset_class = filtersets.CiscoDeviceSupportFilterSet


class CiscoDeviceTypeSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoDeviceTypeSupport.objects.all().prefetch_related("device_type")
    serializer_class = CiscoDeviceTypeSupportSerializer
    filterset_class = filtersets.CiscoDeviceTypeSupportFilterSet


#### Fortinet Support #######################################################################################


class FortinetDeviceSupportViewSet(NetBoxModelViewSet):
    queryset = models.FortinetDeviceSupport.objects.all().prefetch_related("device")
    serializer_class = FortinetDeviceSupportSerializer
    filterset_class = filtersets.FortinetDeviceSupportFilterSet
