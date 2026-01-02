import tkinter as tk
from tkinter import ttk
import tkintermapview

from PADG_lib.controller import CemeteryFunctions, WorkerFunctions, ClientFunctions


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PADG_JZ")
        self.geometry("1025x600")
        self.current_object = None
        self.current_frame = None

        self.cem_logic = CemeteryFunctions(self)
        self.worker_logic = WorkerFunctions(self)
        self.client_logic = ClientFunctions(self)

        self.__frame_setup()
        self.__create_main_widgets()
        self.__create_map_view()

        self._user_config = {
            "cmentarze": {"logic": self.cem_logic, "builder": self.__create_cemetery_view,
                          "show": self.cem_logic.cemetery_show, "entries": {}},
            "pracownicy": {"logic": self.worker_logic, "builder": self.__create_worker_view,
                           "show": self.worker_logic.worker_show, "entries": {}},
            "klienci": {"logic": self.client_logic, "builder": self.__create_client_view,
                        "show": self.client_logic.client_show, "entries": {}},
        }
        
        self.__default_user()


    def __frame_setup(self) -> None:
        '''
        Create frames for widgets
        '''
        self.frame_list = tk.Frame(self)
        self.frame_list.grid(row=0, column=0, sticky="nw")

        self.frame_form = tk.Frame(self)
        self.frame_form.grid(row=0, column=1, padx=10, sticky="w")

        self.frame_map = tk.Frame(self)
        self.frame_map.grid(row=2, column=0, pady=10, columnspan= 2)

    def __create_main_widgets(self) -> None:
        '''
        Create widgets use by every user
        '''
        label_choose_user = tk.Label(self.frame_list, text="Wybierz obiekt:")
        label_choose_user.grid(row=0, column=0, sticky="sw")
        self.entry_choose_user = ttk.Combobox(self.frame_list,
                                              values=["cmentarze", "pracownicy", "klienci"])
        self.entry_choose_user.grid(row=0, column=1, columnspan=4,sticky="ew")

        self.entry_choose_user.bind("<<ComboboxSelected>>", lambda event: self.__change_user())

        self.label_listbox_list = tk.Label(self.frame_list, text="Lista obiektów")
        self.label_listbox_list.grid(row=1, column=0, columnspan=3)

        self.listbox_list = tk.Listbox(self.frame_list)
        self.listbox_list.grid(row=2, column=0, columnspan=3)
        self.listbox_list.bind("<<ListboxSelect>>", lambda worker: self.cemetery_workers())
        self.listbox_list.bind("<<ListboxSelect>>", lambda client: self.cemetery_clients())

        self.button_remove = tk.Button(self.frame_list)
        self.button_remove.grid(row=3, column=1)

        self.button_edit = tk.Button(self.frame_list)
        self.button_edit.grid(row=3, column=2)

    def __create_form_widget(self, frame: tk.Frame,row: int, label_text: str, widget_type: str = "entry", values: list = None) -> tk.Widget:
        '''
        Create entry or combobox widget with label depend on selected type
        :param frame: tk.Frame
        :param row: int
        :param label_text: str
        :param widget_type: str
        :param values: list
        '''
        tk.Label(frame, text=label_text).grid(row=row, column=0, sticky='e', pady=2)
        if widget_type == "combobox":
            widget = ttk.Combobox(frame, values=values)
        else :
            widget = tk.Entry(frame)
        widget.grid(row=row, column=1, pady=2, sticky="ew")
        return widget

    def __create_cemetery_view(self, cem_frame: tk.Frame) -> None:
        '''
        Create cemetery form view
        :param cem_frame: tk.Frame
        '''
        self.label_cem_form = tk.Label(cem_frame, text="Dodawanie cmentarza")
        self.label_cem_form.grid(row=0, column=0, columnspan=2)
        
        entries = self._user_config["cmentarze"]["entries"]
        entries["address"] = self.__create_form_widget(cem_frame,3, "Adres")
        entries["name"] =  self.__create_form_widget(cem_frame,1, "Nazwa")
        entries["type"] = self.__create_form_widget(cem_frame, 2, "Rodzaj", "combobox",["komunalny", "rzymskokatolicki", "ewangelicki", "żydowski", "prawosławny", "inny"])

        self.button_cem_add = tk.Button(cem_frame, text="Dodaj cmentarz",
                                             command=self.cem_logic.add_cemetery)
        self.button_cem_add.grid(row=4, column=0, columnspan=2)

        self.button_edit.config(text="Edytuj cmentarz", command=self.cem_logic.data_to_form_cemetery)
        self.button_remove.config(text="Usuń cmentarz", command=self.cem_logic.remove_cemetery)
        
        self.worker_state = tk.IntVar()
        self.client_state = tk.IntVar()
        self.button_show_workers = tk.Checkbutton(cem_frame, text="Pokaż pracowników", variable= self.worker_state, onvalue = 1, offvalue = 0, command= self.cemetery_workers)
        self.button_show_workers.grid(row=5, column=0, columnspan=2)
        self.button_show_workers = tk.Checkbutton(cem_frame, text="Pokaż klientów", variable=self.client_state,
                                                  onvalue=1, offvalue=0, command=self.cemetery_clients)
        self.button_show_workers.grid(row=6, column=0, columnspan=2)

    def __create_worker_view(self, worker_frame: tk.Frame) -> None:
        '''
        Create worker form view
        :param worker_frame: tk.Fram
        '''
        cemeteries_list = self._user_config["cmentarze"]["logic"].get_cemetery_names()
        entries = self._user_config["pracownicy"]["entries"]
        
        self.label_cem_form = tk.Label(worker_frame, text="Dodawanie pracownika cmentarza")
        self.label_cem_form.grid(row=0, column=0, columnspan=2)
        
        entries["address"] = self.__create_form_widget(worker_frame, 3, "Adres")
        entries["name"] = self.__create_form_widget(worker_frame, 1, "Imie")
        entries["surname"] = self.__create_form_widget(worker_frame,2, "Nazwisko")
        entries["age"] = self.__create_form_widget(worker_frame, 4, "Wiek")
        entries["cemetery"] =  self.__create_form_widget(worker_frame, 5, "Cmentarz", "combobox", cemeteries_list)

        self.button_worker_add = tk.Button(worker_frame, text="Dodaj pracownika", command=self.worker_logic.add_worker)
        self.button_worker_add.grid(row=6, column=0, columnspan=2)

        self.button_edit.config(text="Edytuj pracownika", command=self.worker_logic.data_to_form_worker)
        self.button_remove.config(text="Usuń pracownika", command=self.worker_logic.remove_worker)
        
    def __create_client_view(self, client_frame:tk.Frame) -> None:
        '''
        Create client form view
        :param client_frame: tk.Frame
        '''
        cemeteries_list = self._user_config["cmentarze"]["logic"].get_cemetery_names()
        entries = self._user_config["klienci"]["entries"]
        
        self.label_cem_form = tk.Label(client_frame, text="Dodawanie klienta cmentarza")
        self.label_cem_form.grid(row=0, column=0, columnspan=2)
        
        entries["address"] = self.__create_form_widget(client_frame,3, "Adres")
        entries["name"] = self.__create_form_widget(client_frame,1, "Nazwa")
        entries["type"] = self.__create_form_widget(client_frame,2, "Typ działalności", "combobox", ["usługi pogrzebowe", "sprzedaż nagrobków", "kwiaciarnia", "inne"])
        entries["nip"] = self.__create_form_widget(client_frame,4, "Nip")
        entries["phone"] = self.__create_form_widget(client_frame,5, "Numer telefonu")
        entries["cemetery"] = self.__create_form_widget(client_frame,6, "Cmentarz", "combobox", cemeteries_list)

        self.button_client_add = tk.Button(client_frame, text="Dodaj klienta", command= self.client_logic.add_client)
        self.button_client_add.grid(row=7, column=0, columnspan=2)

        self.button_edit.config(text="Edytuj klienta",  command=self.client_logic.data_to_form_client)
        self.button_remove.config(text="Usuń klienta",command= self.client_logic.remove_client)

    def __create_map_view(self) -> None:
        '''
        Create map widget using tkintermapview
        '''
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=1025, height=400)
        self.map_widget.grid(row=1, column=0, sticky="sw")
        self.map_widget.set_position(52.0, 21.0)
        self.map_widget.set_zoom(6)
        
    def __clean_view(self) -> None:
        '''
        Clean current frame and remove all markers from the map
        '''
        if self.current_frame:
            self.current_frame.destroy()
        self.cem_logic.cemetery_remove_markers()
        self.worker_logic.worker_remove_markers()
        self.client_logic.client_remove_markers()

    def __change_user(self, default_user: str = None) -> None:
        '''
        Change current user view depend on chosen combobox option
        :param default_user: str
        '''
        self.__clean_view()
        self.current_frame = tk.Frame(self)
        self.current_frame.grid(row=0, column=1, padx=10, sticky="w")

        self.current_object = self.entry_choose_user.get() if not default_user else default_user
        config = self._user_config[self.current_object]
        config["builder"](self.current_frame)
        config["show"]()

    def __default_user(self) -> None:
        '''
        Set default user choosing combobox options for "cmentarze"
        '''
        self.entry_choose_user.set("cmentarze")
        self.__change_user("cmentarze")

    def cemetery_workers(self) -> None:
        '''
        Gets selected cemetery and activates function to set markers of workers belong to selected cemetery
        '''
        if self.current_object == "cmentarze":
            selected_index = self.get_active_index()
            if selected_index != -1:
                self.cem_logic.get_cemetery_workers(selected_index, self.worker_state.get())

    def cemetery_clients(self) -> None:
        '''
        Gets selected cemetery and activates function to set markers for client belong to selected cemetery
        '''
        if self.current_object == "cmentarze":
            selected_index = self.get_active_index()
            if selected_index != -1:
                self.cem_logic.get_cemetery_clients(selected_index, self.client_state.get())

    def get_entry(self) -> list:
        '''
        Return list of data from form entries
        :return: list
        '''
        data = self._user_config[self.current_object]["entries"]
        return [obj.get() for obj in data.values()]

    def update_info(self, object_list: list) -> None:
        '''
        Update listbox with current object list
        :param object_list: list
        '''
        self.listbox_list.delete(0, tk.END)
        for idx, item in enumerate(object_list):
            self.listbox_list.insert(tk.END,f"{idx + 1}. {item.name} {item.c_type if self.current_object == 'cmentarze' else ''} {item.surname if self.current_object == "pracownicy" else ''}")

    def clear_form(self) -> None:
        '''
        Remove all data from form entries
        '''
        widgets = self._user_config[self.current_object]["entries"]
        for widget in widgets.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')

    def get_active_index(self) -> int:
        '''
        Return index of selected object in listbox
        :return: int
        '''
        selected = self.listbox_list.curselection()
        return selected[0] if selected else -1

    def fill_form(self, edited_obj: object, index: int) -> None:
        '''
        Fill form entries with data from selected object for editing
        :param edited_obj: object
        :param index: int
        '''
        self.clear_form()
        entries = self._user_config[self.current_object]["entries"]
        
        if self.current_object == "cmentarze":
            entries["address"].insert(0, edited_obj.address)
            entries["name"].insert(0, edited_obj.name)
            entries["type"].set(edited_obj.c_type)

            self.button_cem_add.config(text="Zapisz zmiany", command=lambda: self.cem_logic.update_cemetery(index))

        if self.current_object == "pracownicy":
            entries["address"].insert(0, edited_obj.address)
            entries["name"].insert(0, edited_obj.name)
            entries["surname"].insert(0, edited_obj.surname)
            entries["age"].insert(0, edited_obj.age)
            entries["cemetery"].insert(0, edited_obj.cemetery)

            self.button_worker_add.config(text="Zapisz zmiany", command=lambda: self.worker_logic.update_worker(index))

        if self.current_object == "klienci":
            entries["name"].insert(0, edited_obj.name)
            entries["type"].set(edited_obj.client_type)
            entries["address"].insert(0,edited_obj.address)
            entries["nip"].insert(0, edited_obj.nip)
            entries["phone"].insert(0, edited_obj.phone)
            entries["cemetery"].insert(0, edited_obj.cemetery)

            self.button_client_add.config(text="Zapisz zmiany", command = lambda: self.client_logic.update_client(index))
            
    def set_marker(self, latitude: float, longitude: float, text: str, color: str) -> object:
        '''
        Set marker on the map at given coordinates with specified text and color
        :param latitude: float
        :param longitude: float
        :param text: str
        :param color:str
        :return: marker object
        '''
        marker = self.map_widget.set_marker(latitude, longitude, text, marker_color_outside=color)
        self.map_widget.set_position(latitude, longitude)
        self.map_widget.set_zoom(12)
        return marker