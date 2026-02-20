import json, os
from Classes.instance import netbox_instance
from Classes.get_data_netbox import data_netbox
from time import sleep

# Instanciando a classe
netbox = data_netbox()
netbox_req = netbox_instance()

class database_netbox_validation:
    
    # ==================================== VALIDATE - CONFIGURATION ======================================= #
    # Coletar Manufacturers de items
    def validation_configure_manufacturers_types(self, NETBOX_URL, API_TOKEN, PATHS, db_manucfact, netbox_manufact_list):
        acao = "MANUFACTURERS"
        print(f"{'=' * 10}{acao}{'=' * 10}")
        sleep(4)

        for manu in db_manucfact["manufacturers"]:
            if manu.upper() not in netbox_manufact_list:
                DATA_LIST = {
                        "display": manu,
                        "name": manu,
                        "slug": manu.lower()
                    }

                type_data = netbox_req.request_headers_default(METHOD="POST", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=PATHS["manufacturers"])
                print(f" - ID: {type_data.get('id')} - {manu} - cadastrado com sucesso no NetBox")
            
            elif manu.upper() in netbox_manufact_list:
                print(f" - ID: {netbox_manufact_list[manu]["id"]} - {manu} - já existe no NetBox")

    # Coletar Tipos dos Devices e Cores Hex
    def validation_configure_roles(self, NETBOX_URL, API_TOKEN, PATHS, db_roles, netbox_roles_list):
        acao = "RULES"
        print(f"{'=' * 10}{acao}{'=' * 10}")
        sleep(4)

        for role in db_roles["roles"]:
            if role["role"] not in netbox_roles_list:
                DATA_LIST = {         
                        "display": role["role"],
                        "name": role["role"],
                        "slug": role["role"].lower().replace(" ", "-"),
                        "color": role["color"],
                    }

                type_data = netbox_req.request_headers_default(METHOD="POST", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=PATHS["device_roles"])
                print(f" - ID: {type_data.get('id')} - {role['role']} - cadastrado com sucesso no NetBox")
            
            elif role["role"] in netbox_roles_list: 
                print(f" - ID: {netbox_roles_list[role["role"]]["id"]} - Cor: {role["color"]} - {role["role"]} - já existe no NetBox")

    # Coletar Modelos
    def validation_configure_model(self, NETBOX_URL, API_TOKEN, PATHS, db_model, netbox_model_list):
        acao = "MODEL"
        print(f"{'=' * 10}{acao}{'=' * 10}")
        sleep(4)
        
        for man, list_model in db_model.items():
            for model in list_model:
                if model.upper() not in netbox_model_list:
                    DATA_LIST = {
                        "display": model,
                        "manufacturer": { 
                            "slug": man.lower()
                        }, 
                        "model": model,
                        "slug": model.lower(),
                    }

                    type_data = netbox_req.request_headers_default(METHOD="POST", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=PATHS["device_types"])
                    print(f" - ID: {type_data.get('id')} - {model} - cadastrado com sucesso no NetBox")
            
                elif model in netbox_model_list:
                    print(f" - ID: {netbox_model_list[model]['id']} - {model} - já existe no NetBox")

    # Coletar Sites
    def validation_configure_sites(self, NETBOX_URL, API_TOKEN, PATHS, db_sites, netbox_sites_list):
        acao = "SITES"
        print(f"{'=' * 10}{acao}{'=' * 10}")
        sleep(4)

        for sites in db_sites["sites"]: 
            if sites not in netbox_sites_list:
                DATA_LIST = {
                    "display": sites,
                    "name": sites,
                    "slug": sites.lower().replace(" ", "-"),
                    "status": "active"
                } 

                type_data = netbox_req.request_headers_default(METHOD="POST", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=PATHS["sites"])
                print(f" - ID: {type_data.get('id')} - {sites} - cadastrado com sucesso no NetBox") 
        
            elif sites in netbox_sites_list:
                print(f" - ID: {netbox_sites_list[sites]['id']} - {sites} - já existe no NetBox")

    # Coletar Localidades dos Localidade
    def validation_configure_locatation(self, NETBOX_URL, API_TOKEN, PATHS, db_localidades, netbox_locations_list):
        acao = "LOCATION"
        print(f"{'=' * 10}{acao}{'=' * 10}")
        sleep(4)

        # Loop dentro do Bando de Dados - Localidades
        for db_sites, db_list_location in db_localidades.items():
            # print(f"ANTES - Site: {db_sites.upper()} - Localidades: {db_list_location}")

            # Loop dentro do Netbox - Localidades
            for nb_site in netbox_locations_list:
                for nb_loc in netbox_locations_list[nb_site]:
                    for nb_location in nb_loc:
                    
                        if db_sites.upper() == nb_site: 

                            if nb_location in db_list_location:
                                print(f" - Localidade: {nb_location} - Site: {db_sites} - já existe no NETBOX")
                                db_localidades[db_sites].remove(nb_location)
                            
                            else:
                                print(f" - Localidade: {nb_location} - Site: {db_sites} - não existe no Banco de Dados")
                                pass

            # print(f"DEPOIS - Site: {db_sites.upper()} - Localidades: {db_list_location}")
            if db_list_location != []:
                for db_location in db_list_location:
                    # print(f"\t{db_location}")

                    DATA_LIST = {
                        "display": db_location,
                        "name": db_location,
                        "slug": db_location.lower().replace(" ", "-"),
                        "status": "active",
                        "site": {
                        "slug": db_sites.lower().replace(" ", "-")
                        }
                    } 
 
                    type_data = netbox_req.request_headers_default(METHOD="POST", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=PATHS["locations"])
                    print(f" - ID: {type_data.get('id')} - {db_location} - cadastrado com sucesso no NetBox")

    # Coletar informação dos Devices
    def validation_configure_devices(self, NETBOX_URL, API_TOKEN, PATHS, db_device_dict, netbox_devices_list):
        acao = "DEVICE"
        print(f"{'=' * 10}{acao}{'=' * 10}")
        sleep(4)
        
        # Coletando dados novamentes caso tenham sido inseridos novos
        netbox_roles_list = netbox.get_roles(NETBOX_URL, API_TOKEN, PATHS)                                          # NETBOX - ROLES
        netbox_model_list = netbox.get_model(NETBOX_URL, API_TOKEN, PATHS)                                          # NETBOX - MODEL 
        netbox_sites_list = netbox.get_sites(NETBOX_URL, API_TOKEN, PATHS)                                          # NETBOX - SITES
        netbox_locations_list = netbox.get_locations(NETBOX_URL, API_TOKEN, PATHS)                                  # NETBOX - LOCATIONS

        # Validando se Device já está cadastrado no NetBox
        db_device_list = [db_device["hostname"] for db_device in db_device_dict]
        for id, nb_devices in netbox_devices_list.items():
            if nb_devices["hostname"] in db_device_list:
                print(f" - ID: {id} - {nb_devices['hostname']} - já existe no NetBox")
                db_device_list.remove(nb_devices["hostname"]) # remover da lista de cadastro

        # Cadastrando devices no NetBox
        for db_device in db_device_list:
            for db_device_data in db_device_dict:
                if db_device == db_device_data["hostname"]:
                    
                    # Localizando o ID do Modelo no NetBox
                    if db_device_data["modelo"].lower().startswith("cisco"): 
                        cisco_model = db_device_data['modelo'].split()

                        # Validando se o modelo é Catalyst
                        if cisco_model[1] == "Catalyst":  
                            modelo = f"C{cisco_model[-1].upper()}" 
                        
                        # Validando se o modelo é Aironet
                        elif cisco_model[1] == "Aironet":
                            modelo = cisco_model[-1].upper()
                        
                        # Validando se o modelo é Router
                        elif cisco_model[1] == "Router":
                            modelo = cisco_model[-1].upper()

                    else:
                        modelo = db_device_data['modelo'].split()[-1].upper()
                    
                    # Variaveis de IDs
                    serial_number = db_device_data["serial_number"]                       # Localiznando o Serial Number do Device
                    id_model = netbox_model_list[modelo]["id"]                            # Localiznando o ID do Modelo no NetBox
                    id_sites = netbox_sites_list[db_device_data["sites"].upper()]["id"]   # Localiznando o ID do Site no NetBox
                    id_tipo = netbox_roles_list[db_device_data["tipo"].upper()]["id"]     # Localiznando o ID do Tipo no NetBox

                    # Localizando o ID da Localidade no NetBox
                    for nb_loc_loop in netbox_locations_list[db_device_data["sites"].upper()]:
                        if  db_device_data["localidade"].upper() in nb_loc_loop:
                            id_localidade = nb_loc_loop[db_device_data["localidade"].upper()]["id"]
                            # print(f" - Localidade: {db_device_data['localidade']} - Site: {db_device_data['sites']} - ID Localidade: {id_localidade}")

                            DATA_LIST = {
                                "name": db_device,
                                "serial": serial_number,
                                "status": "active",
                                "device_type": id_model,
                                "role": id_tipo,
                                "site": id_sites,
                                "location": id_localidade
                                }

                            type_data = netbox_req.request_headers_default(METHOD="POST", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=PATHS["devices"])
                            print(f" - ID: {type_data.get('id')} - {db_device} - cadastrado com sucesso no NetBox")
                            break

    # Coletar informação dos Interface de Gerencia
    def validation_configure_interface_mgmt(self, NETBOX_URL, API_TOKEN, PATHS, netbox_interface_list):
        acao = "INTERFACES_MGMT"
        print(f"{'=' * 10}{acao}{'=' * 10}")
        sleep(4)

        # Coletando dados novamentes caso tenham sido inseridos novos
        netbox_devices_list = netbox.get_devices(NETBOX_URL, API_TOKEN, PATHS)                                      # NETBOX - DEVICES

        for hostname_intf, intf_list in netbox_interface_list.items():
            for id_device, nb_device in netbox_devices_list.items():
                    if hostname_intf == nb_device["hostname"]:
                        
                        if intf_list != []:
                            for find_mgmt in intf_list:
                                if "mgmt" in find_mgmt:
                                    print(f" - ID: {id_device}: {hostname_intf} - MGMT Existente no Device no NETBOX, ID_INT: {find_mgmt["mgmt"]}")
                                    break
                        
                        elif intf_list == []:
                            DATA_LIST = { 
                                    "display": "mgmt",
                                    "name": "mgmt",
                                    "type": "virtual",
                                    "device": id_device,
                                    "enabled": True
                                }
    
                            type_data = netbox_req.request_headers_default(METHOD="POST", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=PATHS["interfaces"])
                            print(f" - ID: {type_data.get('id')} - Interface MGMT criada no Device ID: {id_device}: {hostname_intf}")
 
    # Coletar informação de Hostname e IP
    def validation_configure_ipv4_mgmt(self, NETBOX_URL, API_TOKEN, PATHS, db_ipv4_mgmt_dict, netbox_address_ipv4_mgmt_list):
        acao = "IPv4_MGMT"
        print(f"{'=' * 10}{acao}{'=' * 10}")
        sleep(4)

        netbox_devices_list = netbox.get_devices(NETBOX_URL, API_TOKEN, PATHS)                                      # NETBOX - DEVICES
        netbox_interface_list = netbox.get_interfaces(NETBOX_URL, API_TOKEN, PATHS, DEVICES=netbox_devices_list)    # NETBOX - INTERFACES

        dict_to_config = {}
        ip_id = ""

        # Localizando informação Hostname e IP Management no Netbox
        for id, device_data in netbox_devices_list.items():
            nb_hostname = device_data['hostname']
            nb_ip_mgmt = device_data['ip_mgmt']
            # print(f'{nb_hostname} - {nb_ip_mgmt}')

            dict_to_config[nb_hostname] = {}

            for nb_int in netbox_interface_list[nb_hostname]:
                if "mgmt" in nb_int:
                    nb_int_id = nb_int["mgmt"]
                    dict_to_config[nb_hostname].update({
                            "dev_id": id,
                            "int_id": nb_int["mgmt"]
                        })
                    break 
        
        # print(f'dict_to_config - {json.dumps(dict_to_config, indent=3)}')

        # Validando endereços Existentes/Sem IP/Corrigir
        for ip_mgmt in db_ipv4_mgmt_dict:
            db_host = ip_mgmt["hostname"]
            db_ip = ip_mgmt["ip"]

            for id, nb_device_data in netbox_devices_list.items(): 
                if db_host == nb_device_data["hostname"]:
                    if nb_device_data["ip_mgmt"] == db_ip:
                        print(f" - IP_ID: {netbox_address_ipv4_mgmt_list[db_ip]["idIp"]} - IP {db_ip} já cadastrado no DEVICE_ID: {netbox_address_ipv4_mgmt_list[db_ip]["idDevice"]} - Hostname: {db_host} no Netbox")
                        del dict_to_config[db_host]

                    elif nb_device_data["ip_mgmt"] == "Sem IP":
                        print(f" - Sem IP cadastrado no {db_host} no Netbox - Necessário configurar IP: {db_ip}")
                        dict_to_config[db_host].update({
                            "ip": db_ip,
                        })

                    elif nb_device_data["ip_mgmt"] != db_ip and nb_device_data["ip_mgmt"] != "Sem IP":
                        print(f" - Corrigir IP MGMT {db_host} no Netbox - DE: {nb_device_data["ip_mgmt"]} / PARA: {db_ip}")
                        dict_to_config[db_host].update({
                            "ip": db_ip,
                        })
    
        # print(json.dumps(dict_to_config, indent=3))

        for hostname, data in dict_to_config.items():
            # print(hostname, data, netbox_devices_list[data["dev_id"]]["ip_mgmt"])

            # if netbox_devices_list[data["dev_id"]]["ip_mgmt"] == "Sem IP":
            
            if data['ip'] not in netbox_address_ipv4_mgmt_list:
                DATA_LIST = {  
                        "address": data['ip'],
                        "status": "active",          
                        "description": f"IP de GERENCIA: {hostname}",
                        "assigned_object_type": "dcim.interface",
                        "assigned_object_id": data['int_id']
                    } 
                
                type_data = netbox_req.request_headers_default(METHOD="POST", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=PATHS["ipv4"])
                ip_address = type_data["display"]
                ip_id = type_data["id"]
                device_id = type_data["assigned_object"]["device"]["id"]
                print(f" - ID: {type_data.get('id')} - IP: {ip_address} - Criado no Netbox para o device: {type_data["assigned_object"]["device"]["display"]}")

                DATA_LIST = {
                        "primary_ip4": ip_id
                    }

                type_data = netbox_req.request_headers_default(METHOD="PATCH", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=f'{PATHS["devices"]}{device_id}/')
                print(f" - ID: {type_data.get('id')} - IP: {type_data["primary_ip"]["display"]} - Aplicado como Primario ao device: {type_data["display"]}")

            elif data['ip'] in netbox_address_ipv4_mgmt_list:
                ip_id = netbox_address_ipv4_mgmt_list[data['ip']]["idIp"]
                device_id = netbox_address_ipv4_mgmt_list[data['ip']]["idDevice"] 

                DATA_LIST = {
                        "primary_ip4": ip_id
                    }

                type_data = netbox_req.request_headers_default(METHOD="PATCH", NETBOX_URL=NETBOX_URL, DATA=DATA_LIST, API_TOKEN=API_TOKEN, PATH=f'{PATHS["devices"]}{device_id}/')
                print(f" - ID: {type_data.get('id')} - IP: {type_data["primary_ip"]["display"]} - Aplicado como Primario ao device: {type_data["display"]}")

# END
