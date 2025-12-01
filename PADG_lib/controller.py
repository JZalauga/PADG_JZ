from PADG_lib.model import cemetery_list


class Object:
    def __init__(self, address: str):
        self.address: str = address
        self.coords :list = self.get_coord_OSM()

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



class Cemetery(Object):
    def __init__(self, address: str, name: str, type: str):
        super().__init__(address)
        self.name: str = name
        self.type: str = type




class CemeteryFunctions:
    def __init__(self, GUI_instance):
        self.gui = GUI_instance
        pass
    def add_cemetery(self) -> None:
        info = self.gui.get_cem_entry()
        new_cem = Cemetery(info[0], info[1], info[2])
        cemetery_list.append(new_cem)
        self.gui.update_cem_info()
        self.gui.clear_cem_form()