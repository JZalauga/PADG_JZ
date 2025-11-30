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
        self.coords: list = self.get_coord_OSM()

if __name__ == "__main__":
    obj = Cemetery("Solidarnośći 36 Warszawa", "Cmentarz Komunalny Południowy", "komunalny")
    print(f"{obj.name} located at {obj.address} has coordinates: {obj.coords}")

