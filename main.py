import tkinter
from tkinter import ttk
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

class GUI(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("PADG_JZ")
        self.geometry("800x600")


        self.__create_widgets()

    def __create_widgets(self):
        self.frame_cem_list = tkinter.Frame(self)
        self.frame_cem_list.grid(row=0, column=0, padx=10)

        self.frame_cem_form = tkinter.Frame(self)
        self.frame_cem_form.grid(row=0, column=1, padx=10)

        # Listbox
        self.label_cem_list = tkinter.Label(self.frame_cem_list, text="Lista obiektów")
        self.label_cem_list.grid(row=0, column=0, columnspan=3)
        self.listbox_cem_list = tkinter.Listbox(self.frame_cem_list, width=40)
        self.listbox_cem_list.grid(row=1, column=0, columnspan=3)

        self.button_remove_cem = tkinter.Button(self.frame_cem_list, text="Usuń cmentarz")
        self.button_remove_cem.grid(row=2, column=1)

        self.button_edit_cem = tkinter.Button(self.frame_cem_list, text="Edytuj cmentarz")
        self.button_edit_cem.grid(row=2, column=2)



        # Form
        self.label_cem_form = tkinter.Label(self.frame_cem_form, text="Dodawanie cmentarza")
        self.label_cem_form.grid(row=0, column=0, columnspan=2)

        self.label_cem_name = tkinter.Label(self.frame_cem_form, text="Nazwa:")
        self.label_cem_name.grid(row=1, column=0)
        self.entry_cem_name = tkinter.Entry(self.frame_cem_form)
        self.entry_cem_name.grid(row=1, column=1)

        self.label_cem_type = tkinter.Label(self.frame_cem_form, text="Typ:")
        self.label_cem_type.grid(row=2, column=0)
        self.entry_cem_type = ttk.Combobox(self.frame_cem_form, values=["komunalny", "żydowski", "prawosławny", "inny"])
        self.entry_cem_type.grid(row=2, column=1)

        self.label_cem_address = tkinter.Label(self.frame_cem_form, text="Adres:")
        self.label_cem_address.grid(row=3, column=0)
        self.entry_cem_address = tkinter.Entry(self.frame_cem_form)
        self.entry_cem_address.grid(row=3, column=1)

        self.button_cem_add = tkinter.Button(self.frame_cem_form, text="Dodaj cmentarz")
        self.button_cem_add.grid(row=4, column=0, columnspan=2)

if __name__ == "__main__":
    test = GUI()
    test.mainloop()
