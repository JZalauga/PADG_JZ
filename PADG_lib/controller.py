from PADG_lib.model import Cemetery, CemeteryRepository, Worker, WorkerRepository, Client, ClientRepository


class Controller:
    def __init__(self, gui_instance, entity_class, data_class):
        self.gui = gui_instance
        self.marker_list: list = []
        self.EntityClass = entity_class
        self.DataClass = data_class()


    def add(self):
        entry = self.gui.get_entry()
        new_entity = self.EntityClass(*entry)
        self.marker_list.append(self.gui.set_marker(new_entity.coords[0], new_entity.coords[1], new_entity.name, new_entity.color))
        self.DataClass.add(new_entity)
        self.gui.update_info(self.DataClass.get_all())
        self.gui.clear_form()

    def remove(self):
        index = self.gui.get_active_index()
        remove_entity = self.DataClass.get_all()[index]
        self.marker_list[index].delete()
        self.DataClass.delete(remove_entity.index)
        self.gui.update_info(self.DataClass.get_all())

    def edit(self):
        index = self.gui.get_active_index()
        edited_entity = self.DataClass.get_all()[index]
        self.gui.fill_form(edited_entity, index)

    def update(self, index: int):
        entry = self.gui.get_entry()
        edited_index = self.DataClass.get_all()[index].index
        edited_entity = self.EntityClass(*entry, index = edited_index)
        self.DataClass.update(edited_entity)
        self.marker_list[index].delete()
        ##sprawdzić append
        self.marker_list.insert(index,self.gui.set_marker(edited_entity.coords[0], edited_entity.coords[1], edited_entity.name, edited_entity.color))
        self.gui.update_info(self.DataClass.get_all())
        self.gui.clear_form()

    def show(self):
        self.gui.update_info(self.DataClass.get_all())
        entities = self.DataClass.get_all()
        for entity in entities:
             self.marker_list.append(self.gui.set_marker(entity.coords[0], entity.coords[1], entity.name, entity.color))

    def remove_markers(self) -> None:
        if self.marker_list:
            for marker in self.marker_list:
                marker.delete()
        self.marker_list.clear()

class CemeteryFunctions(Controller):
    def __init__(self, gui_instance):
        super().__init__(gui_instance, Cemetery, CemeteryRepository)
        self.workers_markers: list = []
        self.clients_markers: list = []

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
        self.marker_list_cleaner(self.workers_markers)
        self.marker_list_cleaner(self.clients_markers)

    def get_cemetery_list(self) -> list:
        return[cemetery.name for cemetery in self.DataClass.get_all()]

    def get_cemetery_workers(self, index: int, state) -> None:
        cemetery = self.DataClass.get_all()[index].name
        self.marker_list_cleaner(self.workers_markers)

        if state == 1:
            self.workers_markers = [self.gui.set_marker(value[1], value[2], value[0], "red") for value in self.DataClass.get_cemetery_workers(cemetery)]


    def get_cemetery_clients(self, index: int, state) -> None:
        cemetery = self.DataClass.get_all()[index].name
        self.marker_list_cleaner(self.clients_markers)
        if state == 1:
            self.clients_markers = [self.gui.set_marker(value[1], value[2], value[0], "green") for value in self.DataClass.get_cemetery_clients(cemetery)]

    def marker_list_cleaner(self, marker_list: list) -> None:
        for marker in marker_list:
            marker.delete()
        self.marker_list.clear()



class WorkerFunctions(Controller):
    def __init__(self, gui_instance):
        super().__init__(gui_instance, Worker, WorkerRepository)

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
        super().__init__(gui_instance, Client, ClientRepository)

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


