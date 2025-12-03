import tkinter
from tkinter import ttk
from turtledemo.paint import switchupdown

from click import command

from PADG_lib.controller import CemeteryFunctions, WorkerFunctions, ClientFunctions


class GUI(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("PADG_JZ")
        self.geometry("1025x600")
        self.object = None

        self.cem_logic = CemeteryFunctions(self)
        self.worker_logic = WorkerFunctions(self)
        self.client_logic = ClientFunctions(self)

        self.__create_map_view()
        self.__create_widgets()


    def __create_widgets(self):
        self.frame_list = tkinter.Frame(self)
        self.frame_list.grid(row=0, column=0, sticky="nw")

        # Listbox
        self.label_choose_user = tkinter.Label(self.frame_list, text="Wybierz obiekt:")
        self.label_choose_user.grid(row=0, column=0, sticky="sw")
        self.entry_choose_user = ttk.Combobox(self.frame_list,
                                              values=["cmentarze", "pracownicy", "klienci"])
        self.entry_choose_user.grid(row=0, column=1, columnspan=4,sticky="ew")

        self.entry_choose_user.bind("<<ComboboxSelected>>", lambda event: self.__user_check())

        self.label_cem_list = tkinter.Label(self.frame_list, text="Lista obiektów")
        self.label_cem_list.grid(row=1, column=0, columnspan=3)

        self.listbox_list = tkinter.Listbox(self.frame_list)
        self.listbox_list.grid(row=2, column=0, columnspan=3)
        

        self.button_remove = tkinter.Button(self.frame_list)
        self.button_remove.grid(row=3, column=1)

        self.button_edit = tkinter.Button(self.frame_list)
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

        self.button_edit.config(text="Edytuj cmentarz", command=self.cem_logic.edit_cemetery)
        self.button_remove.config(text="Usuń cmentarz", command=self.cem_logic.remove_cemetery)

    def __create_worker_view(self):
        self.frame_worker_form = tkinter.Frame(self)
        self.frame_worker_form.grid(row=0, column=1, padx=10, sticky="w")

        self.label_cem_form = tkinter.Label(self.frame_worker_form, text="Dodawanie pracownika cmentarza")
        self.label_cem_form.grid(row=0, column=0, columnspan=2)

        self.label_worker_name = tkinter.Label(self.frame_worker_form, text="Imie:")
        self.label_worker_name.grid(row=1, column=0)
        self.entry_worker_name = tkinter.Entry(self.frame_worker_form)
        self.entry_worker_name.grid(row=1, column=1, pady=2, sticky="ew")

        self.label_worker_surname = tkinter.Label(self.frame_worker_form, text="Nazwisko:")
        self.label_worker_surname.grid(row=2, column=0)
        self.entry_worker_surname = tkinter.Entry(self.frame_worker_form)
        self.entry_worker_surname.grid(row=2, column=1, pady=2, sticky="ew")

        self.label_worker_address = tkinter.Label(self.frame_worker_form, text="Adres:")
        self.label_worker_address.grid(row=3, column=0)
        self.entry_worker_address = tkinter.Entry(self.frame_worker_form)
        self.entry_worker_address.grid(row=3, column=1, pady=2, sticky="ew")

        self.label_worker_age = tkinter.Label(self.frame_worker_form, text="Wiek:")
        self.label_worker_age.grid(row=4, column=0)
        self.entry_worker_age = tkinter.Entry(self.frame_worker_form)
        self.entry_worker_age.grid(row=4, column=1, pady=2, sticky="ew")

        self.label_worker_cem = tkinter.Label(self.frame_worker_form, text="Cmentarz:")
        self.label_worker_cem.grid(row=5, column=0)
        self.entry_worker_cem = tkinter.Entry(self.frame_worker_form)
        self.entry_worker_cem.grid(row=5, column=1, pady=2, sticky="ew")

        self.button_worker_add = tkinter.Button(self.frame_worker_form, text="Dodaj pracownika", command=self.worker_logic.add_worker)
        self.button_worker_add.grid(row=6, column=0, columnspan=2)

        self.button_edit.config(text="Edytuj pracownika", command=self.worker_logic.edit_worker)
        self.button_remove.config(text="Usuń pracownika", command=self.worker_logic.remove_worker)

    def __create_client_view(self):
        self.frame_client_form = tkinter.Frame(self)
        self.frame_client_form.grid(row=0, column=1, padx=10, sticky="w")

        self.label_cem_form = tkinter.Label(self.frame_client_form, text="Dodawanie klienta cmentarza")
        self.label_cem_form.grid(row=0, column=0, columnspan=2)

        self.label_client_name = tkinter.Label(self.frame_client_form, text="Nazwa:")
        self.label_client_name.grid(row=1, column=0)
        self.entry_client_name = tkinter.Entry(self.frame_client_form)
        self.entry_client_name.grid(row=1, column=1, pady=2, sticky="ew")

        self.label_client_type = tkinter.Label(self.frame_client_form, text="Typ działalności:")
        self.label_client_type.grid(row=2, column=0)
        self.entry_client_type = ttk.Combobox(self.frame_client_form, values=["usługi pogrzebowe", "sprzedaż nagrobków", "kwiaciarnia", "inne"])
        self.entry_client_type.grid(row=2, column=1, pady=2, sticky="ew")

        self.label_client_address = tkinter.Label(self.frame_client_form, text="Adres:")
        self.label_client_address.grid(row=3, column=0)
        self.entry_client_address = tkinter.Entry(self.frame_client_form)
        self.entry_client_address.grid(row=3, column=1, pady=2, sticky="ew")

        self.label_client_nip = tkinter.Label(self.frame_client_form, text="Nip:")
        self.label_client_nip.grid(row=4, column=0)
        self.entry_client_nip = tkinter.Entry(self.frame_client_form)
        self.entry_client_nip.grid(row=4, column=1, pady=2, sticky="ew")

        self.label_client_phone = tkinter.Label(self.frame_client_form, text="numer telefonu:")
        self.label_client_phone.grid(row=5, column=0)
        self.entry_client_phone = tkinter.Entry(self.frame_client_form)
        self.entry_client_phone.grid(row=5, column=1, pady=2, sticky="ew")

        self.label_client_cem = tkinter.Label(self.frame_client_form, text="Cmentarz:")
        self.label_client_cem.grid(row=6, column=0)
        self.entry_client_cem = tkinter.Entry(self.frame_client_form)
        self.entry_client_cem.grid(row=6, column=1, pady=2, sticky="ew")

        self.button_client_add = tkinter.Button(self.frame_client_form, text="Dodaj klienta", command= self.client_logic.add_client)
        self.button_client_add.grid(row=7, column=0, columnspan=2)

        self.button_edit.config(text="Edytuj klienta", command=self.client_logic.edit_client)
        self.button_remove.config(text="Usuń klienta",command= self.client_logic.remove_client)

    def __create_map_view(self):
        import tkintermapview
        self.frame_map = tkinter.Frame(self)
        self.frame_map.grid(row=2, column=0, pady=10, columnspan= 2)

        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=1025, height=400)
        self.map_widget.grid(row=1, column=0, sticky="sw")
        self.map_widget.set_position(52.0, 21.0)
        self.map_widget.set_zoom(6)
    def delete_form_views(self):
        if hasattr(self, 'frame_cem_form'):
            self.frame_cem_form.destroy()
        if hasattr(self, 'frame_worker_form'):
            self.frame_worker_form.destroy()
        if hasattr(self, 'frame_client_form'):
            self.frame_client_form.destroy()

    def __user_check(self):
        self.delete_form_views()
        self.cem_logic.cemetery_remove_markers()
        self.worker_logic.worker_remove_markers()
        self.client_logic.client_remove_markers()
        if self.entry_choose_user.get() == "cmentarze":
            self.object = "cmentarze"
            self.__create_cem_view()
            self.cem_logic.cemetery_show()
        if self.entry_choose_user.get() == "pracownicy":
            self.object = "pracownicy"
            self.__create_worker_view()
            self.worker_logic.worker_show()
        if self.entry_choose_user.get() == "klienci":
            self.object = "klienci"
            self.__create_client_view()
            self.client_logic.client_show()
        else:
            self.user = ""

    def get_entry(self) -> list:
        if self.entry_choose_user.get() == "cmentarze":
            return [
                self.entry_cem_address.get(),
                self.entry_cem_name.get(),
                self.entry_cem_type.get()
            ]
        if self.entry_choose_user.get() == "pracownicy":
            return [
                self.entry_worker_address.get(),
                self.entry_worker_name.get(),
                self.entry_worker_surname.get(),
                self.entry_worker_cem.get(),
                int(self.entry_worker_age.get())
            ]
        if self.entry_choose_user.get() == "klienci":
            return [
                self.entry_client_address.get(),
                self.entry_client_name.get(),
                self.entry_client_type.get(),
                int(self.entry_client_nip.get()),
                int(self.entry_client_phone.get()),
                self.entry_client_cem.get()
            ]
        else :
            return []

    def update_info(self, object_list: list) -> None:
        self.listbox_list.delete(0, tkinter.END)
        if self.entry_choose_user.get() == "cmentarze":
            for idx, item in enumerate(object_list):
                self.listbox_list.insert(tkinter.END, f"{idx + 1}. {item.name} {item.type}")
        if self.entry_choose_user.get() == "pracownicy":
            for idx, item in enumerate(object_list):
                self.listbox_list.insert(tkinter.END, f"{idx + 1}. {item.name} {item.surname}")
        if self.entry_choose_user.get() == "klienci":
            for idx, item in enumerate(object_list):
                self.listbox_list.insert(tkinter.END, f"{idx + 1}. {item.name}")

    def clear_form(self):
        if self.entry_choose_user.get() == "cmentarze":
            self.entry_cem_name.delete(0, tkinter.END)
            self.entry_cem_address.delete(0, tkinter.END)
            self.entry_cem_type.set('')
            self.entry_cem_name.focus()
        if self.entry_choose_user.get() == "pracownicy":
            self.entry_worker_address.delete(0, tkinter.END)
            self.entry_worker_name.delete(0, tkinter.END)
            self.entry_worker_surname.delete(0, tkinter.END)
            self.entry_worker_age.delete(0, tkinter.END)
            self.entry_worker_cem.delete(0, tkinter.END)
            self.entry_worker_name.focus()
        if self.entry_choose_user.get() == "klienci":
            self.entry_client_address.delete(0, tkinter.END)
            self.entry_client_name.delete(0, tkinter.END)
            self.entry_client_type.set('')
            self.entry_client_nip.delete(0, tkinter.END)
            self.entry_client_phone.delete(0, tkinter.END)
            self.entry_client_cem.delete(0, tkinter.END)
            self.entry_client_name.focus()

    def get_active_index(self) -> int:
        selected = self.listbox_list.curselection()
        if selected:
            return selected[0]
        return -1

    def fill_form(self, edited_cem: object, index: int) -> None:
        self.clear_form()
        i = index
        if self.entry_choose_user.get() == "cmentarze":
            self.entry_cem_address.insert(0, edited_cem.address)
            self.entry_cem_name.insert(0, edited_cem.name)
            self.entry_cem_type.set(edited_cem.type)

            self.button_cem_add.config(text="Zapisz zmiany", command=lambda: self.cem_logic.update_cemetery(i))

        if self.entry_choose_user.get() == "pracownicy":
            self.entry_worker_address.insert(0, edited_cem.address)
            self.entry_worker_name.insert(0, edited_cem.name)
            self.entry_worker_surname.insert(0, edited_cem.surname)
            self.entry_worker_cem.insert(0, edited_cem.cemetery)
            self.entry_worker_age.insert(0, edited_cem.age)

            self.button_worker_add.config(text="Zapisz zmiany", command=lambda: self.worker_logic.update_worker(i))

        if self.entry_choose_user.get() == "klienci":
            self.entry_client_name.insert(0, edited_cem.name)
            self.entry_client_type.set(edited_cem.client_type)
            self.entry_client_address.insert(0,edited_cem.address)
            self.entry_client_nip.insert(0, edited_cem.nip)
            self.entry_client_phone.insert(0, edited_cem.phone)
            self.entry_client_cem.insert(0, edited_cem.cemetery)

            self.button_client_add.config(text="Zapisz zmiany", command = lambda: self.client_logic.update_worker(i))



    def set_marker(self, latitude: float, longitude: float, text: str, color: str) -> None:
        marker = self.map_widget.set_marker(latitude, longitude, text, marker_color_outside=color)
        self.map_widget.set_position(latitude, longitude)
        self.map_widget.set_zoom(12)
        return marker