import requests, json

# Classe de Coleta e Tratamento de dados coletados do Netbox
class netbox_instance:
    # Método para realizar requisições ao NetBox
    def request_headers_default(self, METHOD, NETBOX_URL, DATA={}, API_TOKEN="", PATH=""):

        headers = {
            "Authorization": f"Token {API_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        params = {"limit": 1000}

        try:
            if METHOD == "GET":
                response = requests.request(METHOD, f"{NETBOX_URL}{PATH}", data=json.dumps(DATA), headers=headers, params=params, verify=False) # verify=False para ambientes de lab com certificados autoassinados
                response.raise_for_status() # Levanta um HTTPError para códigos de status de erro (4xx ou 5xx)

            elif METHOD == "POST" or METHOD == "PATCH":
                response = requests.request(METHOD, f"{NETBOX_URL}{PATH}", data=json.dumps(DATA), headers=headers, verify=False) # verify=False para ambientes de lab com certificados autoassinados
                response.raise_for_status() # Levanta um HTTPError para códigos de status de erro (4xx ou 5xx)

            devices = response.json()
            return devices

        except requests.exceptions.HTTPError as errh:
            # print(f"Erro HTTP: {errh}")
            return f"Erro HTTP: {errh}"
        
        except requests.exceptions.ConnectionError as errc:
            # print(f"Erro de Conexão: {errc}")
            return f"Erro de Conexão: {errc}"
        
        except requests.exceptions.Timeout as errt:
            # print(f"Timeout: {errt}")
            return f"Timeout: {errt}"
        
        except requests.exceptions.RequestException as err:
            # print(f"Ocorreu um erro: {err}")
            return f"Ocorreu um erro: {err}"

    # ==================================== RETURN INFORMATION ======================================= #
    # Retornar os devices
    def return_data_devices(self, devices): 
        print("Dispositivos encontrados:")
        for device in devices.get("results", [])[:5]: # Mostra os primeiros 5 dispositivos
            print(f"- {device.get('name')} (ID: {device.get('id')})")
    
    # Retornar lista de Manufacturers
    def return_list_manufacturers(self, manufac):
        
        list_manufacturers = {}
 
        for data in manufac["results"]: # Mostra os primeiros 5 manufacturers
            list_manufacturers.update({
                data["display"]: {
                    "id": data["id"]
                }
            })

        return list_manufacturers
    
    # Retornar lista de Roles
    def return_list_roles(self, dev_roles):
        
        list_roles = {}
 
        for data in dev_roles["results"]: # Mostra os primeiros 5 manufacturers
            list_roles.update({
                data["display"]: {
                    "id": data["id"],
                    "color": data["color"],
                }
            })

        return list_roles
    
    # Retornar lista de Modelos
    def return_list_models(self, net_types):
        # print(json.dumps(net_types, indent=3))
        
        dict_data_type = {} 
 
        for data in net_types["results"]: # Mostra os primeiros 5 manufacturers
            dict_data_type.update({
                data["display"]: {
                    "id": data["id"],
                    "manufacturer": {
                        "id": data["manufacturer"]["id"],
                        "name": data["manufacturer"]["display"]
                    }
                }
            })

        # print(json.dumps(dict_data_type, indent=3))
        return dict_data_type
    
    # Retornar lista de Sites
    def return_list_sites(self, net_sites):
        # print(json.dumps(net_sites, indent=3))
        
        dict_data_site = {} 
 
        for data in net_sites["results"]: # Mostra os primeiros 5 manufacturers
            dict_data_site.update({
                data["display"]: {
                    "id": data["id"],
                    "site": {
                        "status": data["status"]["value"],
                        "slug": data["slug"]
                    }
                }
            })

        # print(json.dumps(dict_data_site, indent=3))
        return dict_data_site 
     
    # Retornar lista de Localidades
    def return_list_locations(self, net_locations):
        # print(json.dumps(net_locations, indent=3))
         
        dict_data_location = {} 

        for data in net_locations["results"]: # Mostra os primeiros 5 manufacturers

            site_name = data["site"]["display"]
            if site_name not in dict_data_location:
                dict_data_location[site_name] = []
 
            dict_data_location[site_name].append({
                data["display"]: {
                    "id": data["id"]
                }
            })

        # print(json.dumps(dict_data_location, indent=3))
        return dict_data_location
    
    # Retornar lista de Devices
    def return_list_devices(self, nb_devices):
        # print(json.dumps(nb_devices, indent=3))
         
        dict_data_devices = {} 

        for data in nb_devices["results"]:
            # print(data["id"], data["name"], data["interface_count"])
            dict_data_devices[data["id"]] = {
                "hostname": data["name"],
                "interface_count": data["interface_count"],
                "status": data["status"]["value"]
                }
            
            if data["primary_ip4"] != None:
                dict_data_devices[data["id"]].update({
                    "ip_mgmt": data["primary_ip4"]["display"]
                } )
            else:
                dict_data_devices[data["id"]].update({
                    "ip_mgmt": "Sem IP"
                } )
        
        # print(json.dumps(dict_data_devices, indent=3)) 
        return dict_data_devices

    # Retornar lista de Interfaces - Não utilizado
    def return_list_interfaces(self, nb_interfaces):
        # print(json.dumps(nb_interfaces, indent=3))
         
        # dict_data_location = {} 

        # for data in net_locations["results"]: # Mostra os primeiros 5 manufacturers

        #     site_name = data["site"]["display"]
        #     if site_name not in dict_data_location:
        #         dict_data_location[site_name] = []
 
        #     dict_data_location[site_name].append({
        #         data["display"]: {
        #             "id": data["id"]
        #         }
        #     })

        # # print(json.dumps(dict_data_location, indent=3))
        # return dict_data_location
        pass
     
    # Retornar lista de IPv4
    def return_list_ipv4(self, nb_ipv4):
        # print(json.dumps(nb_ipv4, indent=3))
         
        dict_data_ipv4 = {} 

        for data in nb_ipv4["results"]: # Mostra os primeiros 5 manufacturers

            ipAddress = data["address"]
            idIp = data["id"]
            interface = data["assigned_object"]["display"] if data["assigned_object"] != None else None
            idInterface = data["assigned_object"]["id"] if data["assigned_object"] != None else None
            device = data["assigned_object"]["device"]["display"]if data["assigned_object"] != None else None
            idDevice = data["assigned_object"]["device"]["id"] if data["assigned_object"] != None else None

            dict_data_ipv4[ipAddress] = {
                "idIp": idIp,
                "interface": interface,
                "idInterface": idInterface,
                "device": device,
                "idDevice": idDevice
            }

        # print(json.dumps(dict_data_ipv4, indent=3))
        return dict_data_ipv4    
    # =============================================================================================== #

# END