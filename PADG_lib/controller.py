from PADG_lib.model import cemetery_list, workers_list


class __Object:
    def __init__(self, address: str):
        self.address: str = address
        self.coords :list = self.get_coord_OSM()
        self.marker = None
        self.color: str = None

    def get_coord_OSM(self) -> list[float]:
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



class Cemetery(__Object):
    def __init__(self, address: str, name: str, type: str):
        super().__init__(address)
        self.name: str = name
        self.type: str = type
        self.color: str = "blue"

class Worker(__Object):
    def __init__(self, address: str, name: str, surname: str, cemetery: str, age: int):
        super().__init__(address)
        self.name: str = name
        self.surname: str = surname
        self.cemetery: str = cemetery
        self.age: int = age
        self.color: str = "red"



class CemeteryFunctions:
    def __init__(self, GUI_instance):
        self.gui = GUI_instance
        pass
    def add_cemetery(self) -> None:
        info = self.gui.get_entry()
        new_cem = Cemetery(info[0], info[1], info[2])
        new_cem.marker = self.gui.set_marker(new_cem.coords[0], new_cem.coords[1], new_cem.name, new_cem.color)
        cemetery_list.append(new_cem)
        self.gui.update_info(cemetery_list)
        self.gui.clear_form()

    def remove_cemetery(self) -> None:
        index = self.gui.get_active_index()
        cemetery_list[index].marker.delete()
        cemetery_list.pop(index)
        self.gui.update_info(cemetery_list)

    def edit_cemetery(self)  -> None:
        cem_index = self.gui.get_active_index()
        edited_workr= cemetery_list[cem_index]
        self.gui.fill_form(edited_cem, cem_index)


    def update_cemetery(self, index: int) -> None:
        info = self.gui.get_entry()
        edited_cem= cemetery_list[index]
        edited_cem.address = info[0]
        edited_cem.name = info[1]
        edited_cem.type = info[2]
        if edited_cem.marker:
            edited_cem.marker.delete()
        edited_cem.coords = edited_cem.get_coord_OSM()
        edited_cem.marker = self.gui.set_marker(edited_cem.coords[0], edited_cem.coords[1], edited_cem.name, edited_cem.color)

        self.gui.update_info(cemetery_list)
        self.gui.clear_form()

class WorkerFunctions:
    def __init__(self, GUI_instance):
        self.gui = GUI_instance

    def add_worker(self) -> None:
        info: list = self.gui.get_entry()
        new_cem = Worker(info[0], info[1], info[2], info[3], info[4])
        new_cem.marker = self.gui.set_marker(new_cem.coords[0], new_cem.coords[1], new_cem.name, new_cem.color)
        workers_list.append(new_cem)
        self.gui.update_info(workers_list)
        self.gui.clear_form()

    def remove_worker(self) -> None:
        index = self.gui.get_active_index()
        workers_list[index].marker.delete()
        workers_list.pop(index)
        self.gui.update_info(workers_list)

    def edit_worker(self)  -> None:
        index = self.gui.get_active_index()
        edited_worker = workers_list[index]
        self.gui.fill_form(edited_worker, index)

    def update_worker(self, index: int) -> None:
        info = self.gui.get_entry()
        edited_worker =  workers_list[index]
        edited_worker.address = info[0]
        edited_worker.name = info[1]
        edited_worker.surname = info[2]
        edited_worker.cemetery = info[3]
        edited_worker.age = info[4]
        if edited_worker.marker:
            edited_worker.marker.delete()
        edited_worker.coords = edited_worker.get_coord_OSM()
        edited_worker.marker = self.gui.set_marker(edited_worker.coords[0], edited_worker.coords[1], edited_worker.name, edited_worker.color)

        self.gui.update_info(workers_list)
        self.gui.clear_form()
