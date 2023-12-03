from django.urls import path
from . import views


app_name = "netbox_device_support_plugin"

urlpatterns = (
    # Cisco Device Support
    path(
        "cisco-device/",
        views.CiscoDeviceSupportListView.as_view(),
        name="ciscodevicesupport_list",
    ),
    path(
        "cisco-device/delete/",
        views.CiscoDeviceSupportBulkDeleteView.as_view(),
        name="ciscodevicesupport_bulk_delete",
    ),
    path(
        "cisco-device/<int:pk>/delete/",
        views.CiscoDeviceSupportDeleteView.as_view(),
        name="ciscodevicesupport_delete",
    ),
    # Cisco Device Type Support
    path(
        "cisco-device-type/",
        views.CiscoDeviceTypeSupportListView.as_view(),
        name="ciscodevicetypesupport_list",
    ),
    path(
        "cisco-device-type/delete/",
        views.CiscoDeviceTypeSupportBulkDeleteView.as_view(),
        name="ciscodevicetypesupport_bulk_delete",
    ),
    path(
        "cisco-device-type/<int:pk>/delete/",
        views.CiscoDeviceTypeSupportDeleteView.as_view(),
        name="ciscodevicetypesupport_delete",
    ),
    # Fortnet Support
    path(
        "fortinet-device/",
        views.FortinetDeviceSupportListView.as_view(),
        name="fortinetdevicesupport_list",
    ),
    path(
        "fortinet-device/delete/",
        views.FortinetDeviceSupportBulkDeleteView.as_view(),
        name="fortinetdevicesupport_bulk_delete",
    ),
    path(
        "fortinet-device/<int:pk>/delete/",
        views.FortinetDeviceSupportDeleteView.as_view(),
        name="fortinetdevicesupport_delete",
    ),
)
