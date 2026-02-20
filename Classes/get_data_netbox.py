import json
import pandas as pd
from Classes.instance import netbox_instance
# Instanciando a classe

netbox = netbox_instance()

# Classe de Redirecionamento de dados do Netbox e Coleta de dados do Banco de dados
class data_netbox:
    def __init__(self):

        # Carregar a base de dados dos devices
        db_devices_arch = pd.read_csv("database/db_devices.csv") 
        
        # Coletando colunas únicas da base de dados
        self.db_localidade = db_devices_arch["localidade"].unique().tolist()    # LOCALIDADE
        self.db_site = db_devices_arch["sites"].unique().tolist()               # SITES
        self.db_modelo = db_devices_arch["modelo"].unique().tolist()            # MODELO
        self.db_manufact = db_devices_arch["manufacturer"].unique().tolist()    # MANUFACTURER
        self.db_tipo = db_devices_arch["tipo"].unique().tolist()                # TIPO
        self.db_color = db_devices_arch["cor"].unique().tolist()                # COR

        # Base de caso isolado
        self.db_sites_localidade = db_devices_arch[["sites", "localidade"]].drop_duplicates().to_dict(orient="records")
        self.db_devices_data = db_devices_arch[["hostname", "localidade", "tipo", "sites", "modelo", "serial_number"]].drop_duplicates().to_dict(orient="records")
        self.db_hostname_ip = db_devices_arch[["hostname", "ip"]].drop_duplicates().to_dict(orient="records")

    # ==================================== GET DATA NETBOX ======================================= #
    # Coletar Manufacturers do NetBox
    def get_manufacturers(self, NETBOX_URL, API_TOKEN, PATHS):
        # Manufacturers --------------------------------------------------------- #
        nb_manufact = netbox.request_headers_default(METHOD="GET", NETBOX_URL=NETBOX_URL, API_TOKEN=API_TOKEN, PATH=PATHS["manufacturers"])
        # print(json.dumps(nb_manufact, indent=3))

        # Coletando lista de Vendors cadastrados no NetBox
        netbox_manufact_list = netbox.return_list_manufacturers(nb_manufact)
        # print(json.dumps(netbox_manufact_list, indent=3))
        # ----------------------------------------------------------------------- #

        return netbox_manufact_list

    # Coletar Roles do NetBox
    def get_roles(self, NETBOX_URL, API_TOKEN, PATHS):
        # Roles ----------------------------------------------------------------- #
        nb_roles = netbox.request_headers_default(METHOD="GET", NETBOX_URL=NETBOX_URL, API_TOKEN=API_TOKEN, PATH=PATHS["device_roles"])
        # print(json.dumps(nb_roles, indent=3))

        # Coletando lista de Roles e Colors cadastrados no NetBox
        netbox_roles_list = netbox.return_list_roles(nb_roles)
        # print(json.dumps(netbox_roles_list, indent=3))
        # ----------------------------------------------------------------------- #
        return netbox_roles_list
    
    # Coletar Modelos no NetBox dos Vendors
    def get_model(self, NETBOX_URL, API_TOKEN, PATHS):
        # Type ----------------------------------------------------------------- #
        nb_model = netbox.request_headers_default(METHOD="GET", NETBOX_URL=NETBOX_URL, API_TOKEN=API_TOKEN, PATH=PATHS["device_types"])
        # print(json.dumps(nb_model, indent=3))

        # Coletando lista de Roles e Colors cadastrados no NetBox
        netbox_model_list = netbox.return_list_models(nb_model)
        # print(json.dumps(netbox_model_list, indent=3))
        # ----------------------------------------------------------------------- #
        return netbox_model_list
    
    # Coletar Localidades no NetBox dos Vendors
    def get_sites(self, NETBOX_URL, API_TOKEN, PATHS):
        # Locations ----------------------------------------------------------------- #
        nb_sites = netbox.request_headers_default(METHOD="GET", NETBOX_URL=NETBOX_URL, API_TOKEN=API_TOKEN, PATH=PATHS["sites"])
        # print(json.dumps(nb_sites, indent=3))

        # Coletando lista de Sites cadastrados no NetBox
        netbox_sites_list = netbox.return_list_sites(nb_sites)
        # print(json.dumps(netbox_sites_list, indent=3))
        # ----------------------------------------------------------------------- #
        return netbox_sites_list
    
    # Coletar Localidades no NetBox dos Vendors
    def get_locations(self, NETBOX_URL, API_TOKEN, PATHS):
        # Locations ----------------------------------------------------------------- #
        nb_locations = netbox.request_headers_default(METHOD="GET", NETBOX_URL=NETBOX_URL, API_TOKEN=API_TOKEN, PATH=PATHS["locations"])
        # print(json.dumps(nb_locations, indent=3))

        # Coletando lista de Roles e Colors cadastrados no NetBox
        netbox_location_list = netbox.return_list_locations(nb_locations)
        # print(json.dumps(netbox_location_list, indent=3))
        # ----------------------------------------------------------------------- #
        return netbox_location_list
    
    # Coletar Localidades no NetBox dos IPv4
    def get_ipv4_mgmt(self, NETBOX_URL, API_TOKEN, PATHS):
        # IPv4 ------------------------------------------------------------------- #
        nb_ipv4 = netbox.request_headers_default(METHOD="GET", NETBOX_URL=NETBOX_URL, API_TOKEN=API_TOKEN, PATH=PATHS["ipv4"])
        # print(json.dumps(nb_ipv4, indent=3))

        # Coletando lista de IPv4 cadastrados no NetBox
        netbox_ipv4_list = netbox.return_list_ipv4(nb_ipv4)
        # print(json.dumps(netbox_ipv4_list, indent=3))
        # ----------------------------------------------------------------------- #
        return netbox_ipv4_list
    
    # Coletar Localidades no NetBox dos Devices
    def get_devices(self, NETBOX_URL, API_TOKEN, PATHS):
        # Devices --------------------------------------------------------------- #
        nb_devices = netbox.request_headers_default(METHOD="GET", NETBOX_URL=NETBOX_URL, API_TOKEN=API_TOKEN, PATH=PATHS["devices"])
        # print(json.dumps(nb_devices, indent=3))

        # Coletando lista de Roles e Colors cadastrados no NetBox
        netbox_devices_list = netbox.return_list_devices(nb_devices)
        # print(json.dumps(netbox_devices_list, indent=3))
        # ----------------------------------------------------------------------- #
        return netbox_devices_list
    
    # Coletar Localidades no NetBox dos Interfaces
    def get_interfaces(self, NETBOX_URL, API_TOKEN, PATHS, DEVICES):
        
        intf_dict_list = {}

        for device in DEVICES:
            hostname = DEVICES[device]["hostname"]
            nb_interfaces = netbox.request_headers_default(METHOD="GET", NETBOX_URL=NETBOX_URL, API_TOKEN=API_TOKEN, PATH=f"{PATHS['interfaces']}?device_id={int(device)}")
            # print(json.dumps(nb_interfaces, indent=3))

            if nb_interfaces["results"] != []:
                intf_dict_list[hostname] = []

                for int_device in nb_interfaces["results"]: 

                    intf_dict_list[hostname].append({
                        f'{int_device["display"]}': int_device["id"]
                    })
            
            elif nb_interfaces["results"] == []:
                intf_dict_list[hostname] = []
        
        # print(json.dumps(intf_dict_list, indent=3))
        return intf_dict_list 
    
    # =================================== GET DATABASE DEVICE ==================================== #
    # Coletar Manufacturers de items
    def db_manufacturers_types(self):

        list_manufact = [item.upper() for item in self.db_manufact]
        list_type = [item.upper() for item in self.db_tipo]

        return {
            "manufacturers": list(set(list_manufact)),
            "types": list(set(list_type))
        }
    
    # Coletar Tipos dos Devices e Cores Hex no Bando de Dados
    def db_roles(self):

        list_roles = []

        for tipo, color in zip(self.db_tipo, self.db_color): 
            list_roles.append({
                    "role": tipo.upper(),
                    "color": color
                    })

        return {
            "roles": list_roles
        }
    
    # Coletar Modelos dos Devices no Bando de Dados
    def db_model(self):

        cisco, fortinet, ubiquiti, juniper, huawei = [],[],[],[],[]
  
        for data in self.db_modelo: # Mostra os primeiros 5 manufacturers
            if "Cisco" in data: 
                cisco_model = data.split()[-1]

                # Validando se o modelo é Catalyst
                if data.split()[1] == "Catalyst": 
                    model = f'C{cisco_model}'
                    cisco.append(model)
                 
                # Validando se o modelo é Aironet
                elif data.split()[1] == "Aironet":
                    model = cisco_model.upper()
                    cisco.append(model)
                 
                # Validando se o modelo é Router
                elif data.split()[1] == "Router":
                    model = cisco_model.upper()
                    cisco.append(model)

            elif "Fortinet" in data:
                model = f'{data.split()[-1]}'
                fortinet.append(model)
 
            elif "Ubiquiti" in data:
                model = f'{data.split()[-1]}'
                ubiquiti.append(model)

            elif "Juniper" in data:
                model = f'{data.split()[-1]}'
                juniper.append(model)

            elif "Huawei" in data:
                model = f'{data.split()[-1]}'
                huawei.append(model)

            list_model = {
                "CISCO": list(set(cisco)),
                "FORTINET": list(set(fortinet)),
                "UBIQUITI": list(set(ubiquiti)),
                "JUNIPER": list(set(juniper)),
                "HUAWEI": list(set(huawei))
            }

        # print(json.dumps(list_model, indent=3))
        return list_model

    # Coletar Sites dos Devices no Bando de Dados
    def db_sites(self):

        list_sites = []
        list_sites = [item.upper() for item in self.db_site] 

        # print(json.dumps(list_sites, indent=3))
        return {
            "sites": sorted(list(set(list_sites)))
        }
    
    # Coletar Localidades dos Devices no Bando de Dados    
    def db_locatation(self):

        dict_sites_localidade = {}

        for item in self.db_sites_localidade:
            site_name = item["sites"].strip()
            localidade = item["localidade"].strip().upper()

            if site_name not in dict_sites_localidade:
                dict_sites_localidade[site_name] = []

            if localidade not in dict_sites_localidade[site_name]:
                dict_sites_localidade[site_name].append(localidade)

        return dict_sites_localidade

    # Coletar informação dos Devices no Bando de Dados
    def db_devices(self):
        return self.db_devices_data
    
    # Coletar informação de Hostname e IP no Bando de Dados
    def db_ipv4_mgmt(self):
        return self.db_hostname_ip
    # ============================================================================================ #
    
# END