from PADG_lib.model import cemetery_list, workers_list, clients_list


class __Object:
    def __init__(self, address: str):
        self.address: str = address
        self.coords :list = self.get_coord_osm()
        self.marker: object = None
        self.color: str = ""

    def get_coord_osm(self) -> list[float]:
        import requests
        url = "https://nominatim.openstreetmap.org/search"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/130.0 Safari/537.36'
        }
        params = {
            'q': self.address,
            'format': 'json'
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        latitude = float(data[0]['lat'])
        longitude = float(data[0]['lon'])
        return [latitude, longitude]
    def update_data(self, *args):
        pass



class Cemetery(__Object):
    def __init__(self, address: str, name: str, c_type: str):
        super().__init__(address)
        self.name: str = name
        self.c_type: str = c_type
        self.color: str = "blue"

    def update_data(self, address, name, c_type):
        self.address = address
        self.name = name
        self.c_type = c_type

class Worker(__Object):
    def __init__(self, address: str, name: str, surname: str, age: int, cemetery: str):
        super().__init__(address)
        self.name: str = name
        self.surname: str = surname
        self.cemetery: str = cemetery
        self.age: int = age
        self.color: str = "red"

    def update_data(self, address, name, surname, age, cemetery):
        self.address = address
        self.name = name
        self.surname = surname
        self.age = age
        self.cemetery = cemetery

class Client(__Object):
    def __init__(self, address:str, name:str, client_type:str, nip: int, phone: str, cemetery: str):
        super().__init__(address)
        self.name: str = name
        self.client_type: str = client_type
        self.nip: int = nip
        self.phone: str = phone
        self.cemetery: str = cemetery
        self.color: str = "green"

    def update_data(self, address, name, client_type, nip, phone, cemetery):
        self.address = address
        self.name = name
        self.client_type = client_type
        self.nip = nip
        self.phone = phone
        self.cemetery = cemetery


class Controller:
    def __init__(self, gui_instance, data_list: list, entity_class):
        self.gui = gui_instance
        self.data_list = data_list
        self.EntityClass = entity_class

    def __refresh_marker(self, entity):
        if entity.marker:
            entity.marker.delete()
        entity.coords = entity.get_coord_osm()
        entity.marker = self.gui.set_marker(entity.coords[0], entity.coords[1], entity.name, entity.color)

    def add(self):
        entry = self.gui.get_entry()
        new_entity = self.EntityClass(*entry)
        self.__refresh_marker(new_entity)
        self.data_list.append(new_entity)
        self.gui.update_info(self.data_list)
        self.gui.clear_form()

    def remove(self):
        index = self.gui.get_active_index()
        self.data_list[index].marker.delete()
        self.data_list.pop(index)
        self.gui.update_info(self.data_list)

    def edit(self):
        index = self.gui.get_active_index()
        edited_entity = self.data_list[index]
        self.gui.fill_form(edited_entity, index)
    def update(self, index: int):
        entry = self.gui.get_entry()
        edited_entity = self.data_list[index]
        edited_entity.update_data(*entry)
        self.__refresh_marker(edited_entity)
        self.gui.update_info(self.data_list)
        self.gui.clear_form()
    def show(self):
        self.gui.update_info(self.data_list)
        for entity in self.data_list:
            entity.marker = self.gui.set_marker(entity.coords[0], entity.coords[1], entity.name, entity.color)
        #self.gui.update_info(entity for entity in self.data_list)

    def remove_markers(self) -> None:
        for entity in self.data_list:
            if entity.marker:
                entity.marker.delete()

class CemeteryFunctions(Controller):
    def __init__(self, gui_instance):
        super().__init__(gui_instance, cemetery_list, Cemetery)

    def add_cemetery(self):
        super().add()

    def remove_cemetery(self):
        super().remove()

    def edit_cemetery(self):
        super().edit()

    def update_cemetery(self, index: int):
        super().update(index)

    def cemetery_show(self):
        super().show()

    def cemetery_remove_markers(self):
        super().remove_markers()


class WorkerFunctions(Controller):
    def __init__(self, gui_instance):
        super().__init__(gui_instance, workers_list, Worker)

    def add_worker(self):
        super().add()

    def remove_worker(self):
        super().remove()

    def edit_worker(self):
        super().edit()

    def update_worker(self, index: int):
        super().update(index)

    def worker_show(self):
        super().show()

    def worker_remove_markers(self):
        super().remove_markers()

class ClientFunctions(Controller):
    def __init__(self, gui_instance):
        super().__init__(gui_instance, clients_list, Client)

    def add_client(self):
        super().add()

    def remove_client(self):
        super().remove()

    def edit_client(self):
        super().edit()

    def update_client(self, index: int):
        super().update(index)

    def client_show(self):
        super().show()

    def client_remove_markers(self):
        super().remove_markers()
