import hashlib

from PADG_lib.model import Cemetery, CemeteryRepository, Worker, WorkerRepository, Client, ClientRepository, LoginDataRepository


class Controller:
    '''
    Base Controller class to manage entities and their GUI representation.
    It handles adding, removing, editing, and updating entities and managing markers
    :param: gui_instance:
    :param: entity_class:
    :param: data_class:
    '''
    def __init__(self, gui_instance, entity_class, data_class):
        self.gui = gui_instance
        self.marker_list: list = []
        self.EntityClass = entity_class
        self.DataClass = data_class()


    def add(self) -> None:
        '''
        Adds a new entity based on user input and append marker to marker list.
        '''
        entry = self.gui.get_entry()
        new_entity = self.EntityClass(*entry)
        self.marker_list.append(self.gui.set_marker(new_entity.coords[0], new_entity.coords[1], new_entity.name, new_entity.color))
        self.DataClass.add(new_entity)
        self.gui.update_info(self.DataClass.get_all())
        self.gui.clear_form()

    def remove(self) -> None:
        '''
        Remove selected entity and its marker from the map and data repository
        '''
        index = self.gui.get_active_index()
        remove_entity = self.DataClass.get_all()[index]
        self.marker_list[index].delete()
        self.DataClass.delete(remove_entity.index)
        self.gui.update_info(self.DataClass.get_all())

    def data_to_form(self) -> None:
        '''
        Fill the form with data from the selected entity
        '''
        index = self.gui.get_active_index()
        edited_entity = self.DataClass.get_all()[index]
        self.gui.fill_form(edited_entity, index)

    def update(self, index: int) -> None:
        '''
        Update the selected entity with data from the form and refresh its marker
        :param index:
        '''
        entry = self.gui.get_entry()
        edited_index = self.DataClass.get_all()[index].index
        edited_entity = self.EntityClass(*entry, index = edited_index)
        self.DataClass.update(edited_entity)
        self.marker_list[index].delete()
        self.marker_list.insert(index,self.gui.set_marker(edited_entity.coords[0], edited_entity.coords[1], edited_entity.name, edited_entity.color))
        self.gui.update_info(self.DataClass.get_all())
        self.gui.clear_form()

    def show(self) -> None:
        '''
        Create markers for all entities
        '''
        self.gui.update_info(self.DataClass.get_all())
        entities = self.DataClass.get_all()
        for entity in entities:
             self.marker_list.append(self.gui.set_marker(entity.coords[0], entity.coords[1], entity.name, entity.color))

    def remove_markers(self) -> None:
        '''
        Remove all markers from the map
        :return:
        '''
        if self.marker_list:
            for marker in self.marker_list:
                marker.delete()
        self.marker_list.clear()

class CemeteryFunctions(Controller):
    '''
    Cemetery Controller class to manage Cemetery entities and markers
    '''
    def __init__(self, gui_instance):
        super().__init__(gui_instance, Cemetery, CemeteryRepository)
        self.workers_markers: list = []
        self.clients_markers: list = []

    def add_cemetery(self):
        '''
        Adds a new cemetery based on user input
        '''
        super().add()

    def remove_cemetery(self):
        '''
        Remove selected cemetery
        '''
        super().remove()

    def data_to_form_cemetery(self):
        '''
        Fill the form with data from the selected cemetery
        :return:
        '''
        super().data_to_form()

    def update_cemetery(self, index: int):
        '''
        Update the selected cemetery with data from the form
        :param index: int
        :return:
        '''
        super().update(index)

    def cemetery_show(self):
        '''
        Create markers for all cemeteries
        '''
        super().show()

    def cemetery_remove_markers(self):
        '''
        Remove all cemetery, its workers and clients markers from the map
        '''
        super().remove_markers()
        self.marker_list_cleaner(self.workers_markers)
        self.marker_list_cleaner(self.clients_markers)

    def get_cemetery_names(self) -> list:
        '''
        Return list of cemetery names
        :return: list
        '''
        return[cemetery.name for cemetery in self.DataClass.get_all()]

    def get_cemetery_workers(self, index: int, state: int) -> None:
        '''
        Create markers for cemetery workers
        :param index: int
        :param state: int
        '''
        cemetery = self.DataClass.get_all()[index].name
        self.marker_list_cleaner(self.workers_markers)
        if state == 1:
            self.workers_markers = [self.gui.set_marker(value[1], value[2], value[0], "red") for value in self.DataClass.get_cemetery_workers(cemetery)]


    def get_cemetery_clients(self, index: int, state: int) -> None:
        '''
        Create markers for cemetery clients
        :param index: int
        :param state: int
        '''
        cemetery = self.DataClass.get_all()[index].name
        self.marker_list_cleaner(self.clients_markers)
        if state == 1:
            self.clients_markers = [self.gui.set_marker(value[1], value[2], value[0], "green") for value in self.DataClass.get_cemetery_clients(cemetery)]

    def marker_list_cleaner(self, marker_list: list) -> None:
        '''
        Remove markers and clear the marker list
        :param marker_list:
        '''
        for marker in marker_list:
            marker.delete()
        self.marker_list.clear()



class WorkerFunctions(Controller):
    '''
    Worker Controller class to manage Worker entities and markers
    '''
    def __init__(self, gui_instance):
        super().__init__(gui_instance, Worker, WorkerRepository)

    def add_worker(self):
        '''
        Adds a new worker based on user input
        '''
        super().add()

    def remove_worker(self):
        '''
        Remove selected worker
        '''
        super().remove()

    def data_to_form_worker(self):
        '''
        Fill the form with data from the selected worker
        '''
        super().data_to_form()

    def update_worker(self, index: int):
        '''
        Update the selected worker with data from the form
        :param index: int
        '''
        super().update(index)

    def worker_show(self):
        '''
        Create markers for all workers
        '''
        super().show()

    def worker_remove_markers(self):
        '''
        Remove all worker markers from the map
        '''
        super().remove_markers()

class ClientFunctions(Controller):
    '''
    Client Controller class to manage Client entities and markers
    '''
    def __init__(self, gui_instance):
        super().__init__(gui_instance, Client, ClientRepository)

    def add_client(self):
        '''
        Adds a new client based on user input
        '''
        super().add()

    def remove_client(self):
        '''
        Remove selected client
        '''
        super().remove()

    def data_to_form_client(self):
        '''
        Fill the form with data from the selected client
        '''
        super().data_to_form()

    def update_client(self, index: int):
        '''
        Update the selected client with data from the form
        :param index: int
        '''
        super().update(index)

    def client_show(self):
        '''
        Create markers for all clients
        '''
        super().show()

    def client_remove_markers(self):
        '''
        Remove all client markers from the map
        '''
        super().remove_markers()

class LogInController:
    def __init__(self, gui_instance):
        self.gui = gui_instance
        self.database = LoginDataRepository()

    def confirm_login(self):
        '''
        Confirm login credentials
        '''
        username, enter_password = self.gui.get_login_entry()
        if not self.database.check_login(username):
            self.gui.login_failed_alert()
            return
        stored_hash = self.database.get_password(username)
        hash = hashlib.sha256()
        hash.update(enter_password.encode())
        enter_hash = hash.hexdigest()
        if stored_hash != enter_hash:
            self.gui.login_error_alert()
            return
        self.gui.create_app_view()

    def register_user(self):
        '''
        Register new user
        '''
        username, password, repeat_password = self.gui.get_register_entry()
        print(username, password, repeat_password)
        if password != repeat_password:
            self.gui.password_mismatch_alert()
            return
        if self.database.check_login(username):
            self.gui.username_exists_alert()
            return
        hash = hashlib.sha256()
        hash.update(password.encode())
        hash_password = hash.hexdigest()
        self.database.add_login_data(username, hash_password)
        self.gui.clean_register_entries()
