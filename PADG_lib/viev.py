import tkinter
from tkinter import ttk

from PADG_lib.controller import CemeteryFunctions

class GUI(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("PADG_JZ")
        self.geometry("1025x600")

        self.user: str = "cemetery"

        self.cem_logic = CemeteryFunctions(self)


        self.__create_map_view()
        self.__create_widgets()


    def __create_widgets(self):
        self.frame_list = tkinter.Frame(self)
        self.frame_list.grid(row=0, column=0, sticky="nw")

        # Listbo
        self.label_cem_list = tkinter.Label(self.frame_list, text="Lista obiektów")
        self.label_cem_list.grid(row=0, column=0, columnspan=3)

        self.label_choose_user = tkinter.Label(self.frame_list, text="Wybierz obiekt:")
        self.label_choose_user.grid(row=1, column=0)
        self.entry_choose_user = ttk.Combobox(self.frame_list,
                                              values=["cmentarze"])

        self.entry_choose_user.grid(row=1, column=1, columnspan=3,)

        self.entry_choose_user.bind("<<ComboboxSelected>>", lambda event: self.__user_check())


        self.listbox_list = tkinter.Listbox(self.frame_list)
        self.listbox_list.grid(row=2, column=0, columnspan=3)
        

        self.button_remove = tkinter.Button(self.frame_list, text="Usuń cmentarz", command=self.cem_logic.remove_cemetery)
        self.button_remove.grid(row=3, column=1)

        self.button_edit = tkinter.Button(self.frame_list, text="Edytuj cmentarz", command=self.cem_logic.edit_cemetery)
        self.button_edit.grid(row=3, column=2)
        
    def __create_cem_view(self):
        self.frame_cem_form = tkinter.Frame(self)
        self.frame_cem_form.grid(row=0, column=1, padx=10, sticky="w")

        self.label_cem_form = tkinter.Label(self.frame_cem_form, text="Dodawanie cmentarza")
        self.label_cem_form.grid(row=0, column=0, columnspan=2)

        self.label_cem_name = tkinter.Label(self.frame_cem_form, text="Nazwa:")
        self.label_cem_name.grid(row=1, column=0)
        self.entry_cem_name = tkinter.Entry(self.frame_cem_form)
        self.entry_cem_name.grid(row=1, column=1, pady=2, sticky="ew")

        self.label_cem_type = tkinter.Label(self.frame_cem_form, text="Rodzaj:")
        self.label_cem_type.grid(row=2, column=0)
        self.entry_cem_type = ttk.Combobox(self.frame_cem_form,
                                           values=["komunalny", "rzymskokatolicki", "ewangelicki", "żydowski",
                                                   "prawosławny", "inny"])
        self.entry_cem_type.grid(row=2, column=1, pady=2, sticky="ew")

        self.label_cem_address = tkinter.Label(self.frame_cem_form, text="Adres:")
        self.label_cem_address.grid(row=3, column=0)
        self.entry_cem_address = tkinter.Entry(self.frame_cem_form)
        self.entry_cem_address.grid(row=3, column=1, pady=2, sticky="ew")

        self.button_cem_add = tkinter.Button(self.frame_cem_form, text="Dodaj cmentarz",
                                             command=self.cem_logic.add_cemetery)
        self.button_cem_add.grid(row=4, column=0, columnspan=2)
        
    def __create_map_view(self):
        import tkintermapview
        self.frame_map = tkinter.Frame(self)
        self.frame_map.grid(row=2, column=0, pady=10, columnspan= 2)

        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=1025, height=400)
        self.map_widget.grid(row=1, column=0, sticky="sw")
        self.map_widget.set_position(52.0, 21.0)
        self.map_widget.set_zoom(6)

    def __user_check(self):
        if self.entry_choose_user.get() == "cmentarze":
            self.user = "cemetery"
            self.__create_cem_view()
        else:
            self.user = ""

    def get_entry(self) -> list:
        if self.user == "cemetery":
            return [
                self.entry_cem_address.get(),
                self.entry_cem_name.get(),
                self.entry_cem_type.get()
            ]
        else :
            return []

    def update_info(self, cem_list: list) -> None:
        self.listbox_list.delete(0, tkinter.END)
        if self.user == "cemetery":
            for idx, item in enumerate(cem_list):
                self.listbox_list.insert(tkinter.END, f"{idx + 1}. {item.name} {item.type}")

    def clear_form(self):
        if self.user == "cemetery":
            self.entry_cem_name.delete(0, tkinter.END)
            self.entry_cem_address.delete(0, tkinter.END)
            self.entry_cem_type.set('')
            self.entry_cem_name.focus()

    def get_active_index(self) -> int:
        selected = self.listbox_list.curselection()
        if selected:
            return selected[0]
        return -1

    def fill_form(self, edited_cem: object, index: int) -> None:
        self.clear_form()
        i = index
        if self.user == "cemetery":
            self.entry_cem_address.insert(0, edited_cem.address)
            self.entry_cem_name.insert(0, edited_cem.name)
            self.entry_cem_type.set(edited_cem.type)

            self.button_cem_add.config(text="Zapisz zmiany", command=lambda: self.cem_logic.update_cemetery(i))

    def set_marker(self, latitude: float, longitude: float, text: str, color: str) -> None:
        marker = self.map_widget.set_marker(latitude, longitude, text, marker_color_outside=color)
        self.map_widget.set_position(latitude, longitude)
        self.map_widget.set_zoom(12)
        return marker