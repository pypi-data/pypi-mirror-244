from extras.plugins import PluginConfig
from .version import __version__


class DeviceSupportConfig(PluginConfig):
    name = "netbox_device_support_plugin"
    verbose_name = "Device Support Plugin"
    description = "Device support information about software release, maintenance contract, license and more."
    version = __version__
    author = "Willi Kubny"
    author_email = "willi.kubny@gmail.com"
    base_url = "device-support"
    min_version = "3.5.0"
    required_settings = ["CISCO_SUPPORT_API_CLIENT_ID", "CISCO_SUPPORT_API_CLIENT_SECRET"]
    default_settings = {"MANUFACTURER": "Cisco", "TEMPLATE_EXTENSION_PLACEMENT": "right"}


config = DeviceSupportConfig
