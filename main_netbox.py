import json, os
from Classes.instance import netbox_instance
from Classes.get_data_netbox import data_netbox
from Classes.validation import database_netbox_validation
from dotenv import load_dotenv
load_dotenv()

# Instanciando a classe
netbox = data_netbox()
netbox_req = netbox_instance()
netbox_config = database_netbox_validation()
 
# Acesso inicial
NETBOX_URL = os.getenv("URL")
API_TOKEN = os.getenv("API_TOKEN")

PATHS = {
    "manufacturers": "dcim/manufacturers/",    # Retorna os MANUFACTURERS cadastrados no NetBox
    "device_roles": "dcim/device-roles/",      # Retorna os DEVICE ROLES cadastrados no NetBox
    "device_types": "dcim/device-types/",      # Retorna os DEVICE TYPES cadastrados no NetBox
    "sites": "dcim/sites/",                    # Retorna os SITES cadastrados no NetBox
    "locations": "dcim/locations/",            # Retorna os LOCATIONS cadastrados no NetBox
    "devices": "dcim/devices/",                # Retorna os DEVICES cadastrados no NetBox
    "interfaces": "dcim/interfaces/",          # Retorna os INTERFACES cadastrados nos DEVICES do NetBox
    "ipv4": "ipam/ip-addresses/",              # Retorna os ENDEREÇO IPV4 cadastrados no NetBox
}

# ----------------------------------------------------------------------- #
# Tratar dados da base do NETBOX
netbox_manufact_list = netbox.get_manufacturers(NETBOX_URL, API_TOKEN, PATHS)                               # NETBOX - MANUFACTURERS 
# print(f"netbox_manufact_list - {json.dumps(netbox_manufact_list, indent=3)}")                             # NETBOX - MANUFACTURERS  - JSON_DUMPS SHOW

netbox_roles_list = netbox.get_roles(NETBOX_URL, API_TOKEN, PATHS)                                          # NETBOX - ROLES
# print(f"netbox_roles_list - {json.dumps(netbox_roles_list, indent=3)}")                                   # NETBOX - ROLES - JSON_DUMPS SHOW

netbox_model_list = netbox.get_model(NETBOX_URL, API_TOKEN, PATHS)                                          # NETBOX - MODEL
# print(f"netbox_model_list - {json.dumps(netbox_model_list, indent=3)}")                                   # NETBOX - MODEL - JSON_DUMPS SHOW

netbox_sites_list = netbox.get_sites(NETBOX_URL, API_TOKEN, PATHS)                                          # NETBOX - SITES
# print(f"netbox_sites_list - {json.dumps(netbox_sites_list, indent=3)}")                                   # NETBOX - SITES - JSON_DUMPS SHOW

netbox_locations_list = netbox.get_locations(NETBOX_URL, API_TOKEN, PATHS)                                  # NETBOX - LOCATIONS
# print(f"netbox_locations_list - {json.dumps(netbox_locations_list, indent=3)}")                           # NETBOX - LOCATIONS - JSON_DUMPS SHOW

netbox_devices_list = netbox.get_devices(NETBOX_URL, API_TOKEN, PATHS)                                      # NETBOX - DEVICES
# print(f"netbox_devices_list - {json.dumps(netbox_devices_list, indent=3)}")                               # NETBOX - DEVICES - JSON_DUMPS SHOW

netbox_interface_list = netbox.get_interfaces(NETBOX_URL, API_TOKEN, PATHS, DEVICES=netbox_devices_list)    # NETBOX - INTERFACES
# print(f"netbox_interface_list - {json.dumps(netbox_interface_list, indent=3)}")                           # NETBOX - INTERFACES - JSON_DUMPS SHOW

netbox_address_ipv4_mgmt_list = netbox.get_ipv4_mgmt(NETBOX_URL, API_TOKEN, PATHS)                          # NETBOX - ENDERECAMENTO
# print(f"netbox_address_ipv4_mgmt_list - {json.dumps(netbox_address_ipv4_mgmt_list, indent=3)}")           # NETBOX - ENDERECAMENTO - JSON_DUMPS SHOW

# ----------------------------------------------------------------------- #
# Tratar dados do Banco de Dados
db_manucfact = netbox.db_manufacturers_types()                                                              # DATABASE - MANUFACTURERS
# print(f"db_manucfact - {json.dumps(db_manucfact, indent=3)}")                                             # DATABASE - MANUFACTURERS - JSON_DUMPS SHOW 

db_roles = netbox.db_roles()                                                                                # DATABASE - ROLE
# print(f"db_roles - {json.dumps(db_roles, indent=3)}")                                                     # DATABASE - ROLE - JSON_DUMPS SHOW 

db_model = netbox.db_model()                                                                                # DATABASE - MODELO
# print(f"db_model - {json.dumps(db_model, indent=3)}")                                                     # DATABASE - MODELO - JSON_DUMPS SHOW 

db_sites = netbox.db_sites()                                                                                # DATABASE - SITE
# print(f"db_sites - {json.dumps(db_sites, indent=3)}")                                                     # DATABASE - SITE - JSON_DUMPS SHOW 

db_localidades = netbox.db_locatation()                                                                     # DATABASE - LOCALIDADE
# print(f"db_localidades - {json.dumps(db_localidades, indent=3)}")                                         # DATABASE - LOCALIDADE - JSON_DUMPS SHOW 

db_device_dict = netbox.db_devices()                                                                        # DATABASE - DEVICES
# print(f"db_device_dict - {json.dumps(db_device_dict, indent=3)}")                                         # DATABASE - DEVICES - JSON_DUMPS SHOW 

db_ipv4_mgmt_dict = netbox.db_ipv4_mgmt()                                                                   # DATABASE - IPv4
# print(f"db_ipv4_mgmt_dict - {json.dumps(db_ipv4_mgmt_dict, indent=3)}")                                   # DATABASE - IPv4 - JSON_DUMPS SHOW 

# ----------------------------------------------------------------------- #
# Validadndo e Aplicando configuração 
# Manufacturers
netbox_config.validation_configure_manufacturers_types(NETBOX_URL, API_TOKEN, PATHS, db_manucfact, netbox_manufact_list)

# Roles
netbox_config.validation_configure_roles(NETBOX_URL, API_TOKEN, PATHS, db_roles, netbox_roles_list)

# Model
netbox_config.validation_configure_model(NETBOX_URL, API_TOKEN, PATHS, db_model, netbox_model_list)

# Sites
netbox_config.validation_configure_sites(NETBOX_URL, API_TOKEN, PATHS, db_sites, netbox_sites_list)

# Locatation
netbox_config.validation_configure_locatation(NETBOX_URL, API_TOKEN, PATHS, db_localidades, netbox_locations_list)

# Devices
netbox_config.validation_configure_devices(NETBOX_URL, API_TOKEN, PATHS, db_device_dict, netbox_devices_list)

# Interface MGMT
netbox_config.validation_configure_interface_mgmt(NETBOX_URL, API_TOKEN, PATHS, netbox_interface_list)

# Ipv4 MGMT
netbox_config.validation_configure_ipv4_mgmt(NETBOX_URL, API_TOKEN, PATHS, db_ipv4_mgmt_dict, netbox_address_ipv4_mgmt_list)
# ----------------------------------------------------------------------- #

# END
