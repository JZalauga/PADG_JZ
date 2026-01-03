import psycopg2

class __User:
    '''
    Parent object that contains all information about users
    :param address: str
    :param coords: list
    '''
    def __init__(self, address: str, coords: list = None):
        self.address: str = address
        self.coords :list = self.get_coord_osm() if coords is None else coords
        self.marker: object = None
        self.color: str = ""
        self.columns: dict ={}

    def get_coord_osm(self) -> list[float]:
        '''
        Return coordinates of point from its address basing on OSM
        :return: list[float]
        '''
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



class Cemetery(__User):
    '''
    Object representing cemetery user
    :param address: str
    :param name: str
    :param c_type: str
    :param index: int
    :param coords: list
    '''
    def __init__(self, address: str, name: str, c_type: str, index: int = None, coords: list[float] = None):
        super().__init__(address, coords= coords)
        self.index = index
        self.name: str = name
        self.c_type: str = c_type
        self.color: str = "blue"


class Worker(__User):
    '''
    Object representing cemetery worker user
    :param address: str
    :param name: str
    :param surname: str
    :param age: int
    :param cemetery: str
    :param index: int
    :param coords: list
    '''
    def __init__(self, address: str, name: str, surname: str, age: int, cemetery: str, index = None, coords = None):
        super().__init__(address, coords = coords)
        self.index = index
        self.name: str = name
        self.surname: str = surname
        self.cemetery: str = cemetery
        self.age: int = age
        self.color: str = "red"


class Client(__User):
    '''
    Object representing cemetery client user
    :param address: str
    :param name: str
    :param client_type: str
    :param nip: int
    :param phone: str
    :param cemetery: str
    :param index: int
    :param coords: list
    '''
    def __init__(self, address:str, name:str, client_type:str, nip: int, phone: str, cemetery: str, index = None, coords= None):
        super().__init__(address, coords= coords)
        self.index = index
        self.name: str = name
        self.client_type: str = client_type
        self.nip: int = nip
        self.phone: str = phone
        self.cemetery: str = cemetery
        self.color: str = "green"


class Repository[T]:
    def get(self, id: int) -> T:
        pass
    def get_all(self) -> list[T]:
        '''
        Return list of objects with parameters form database
        :return: list[T]
        '''
        pass
    def add(self, obj: T) -> None:
        pass
    def update(self, obj: T) -> None:
        pass
    def delete(self, id: int) -> None:
        pass


class CemeteryRepository(Repository[Cemetery]):
    '''
    Repository class for Cemetery object that contains all methods for database operations
    '''
    def __init__(self):
        super().__init__()
        self.db_engine = None
        self.cursor = None
        self.db_connection()

    def db_connection(self) -> None:
        '''
        Create connection to local PostgreSQL database
        '''
        self.db_engine = psycopg2.connect(
            user="postgres",
            database="cemetery_database",
            password="postgres",
            port="5432",
            host="localhost",
        )
        self.cursor = self.db_engine.cursor()

    def get(self, id: int) -> Cemetery:
        '''
        Gets all values from record based on id
        :param id: int
        :return: Cemetery
        '''
        SQL = "SELECT *, ST_X(location::geometry), ST_Y(location::geometry) FROM public.cemeteries WHERE cemetery_id = %s;"
        self.cursor.execute(SQL, (id,))
        entry = self.cursor.fetchone()
        return Cemetery(index= entry[0], address=entry[1],name=entry[2], c_type= entry[3],coords= [entry[-2], entry[-1]])

    def get_all(self) -> list[Cemetery]:
        '''
        Return list of Cemetery with parameters form database. List length depend on number of records
        :return: list[Cemetery]
        '''
        SQL = "SELECT *, ST_X(location::geometry), ST_Y(location::geometry) FROM public.cemeteries;"
        self.cursor.execute(SQL)
        entries = self.cursor.fetchall()
        return [Cemetery(index= entry[0], address=entry[1],name = entry[2],c_type= entry[3], coords=[entry[-2], entry[-1]]) for entry in entries]

    def add(self, obj: Cemetery) -> None:
        '''
        Adds Cemetery object to database
        :param obj: Cemetery
        '''
        SQL = "INSERT INTO public.cemeteries(address, name, type, location) VALUES (%s, %s, %s, 'SRID=4326;POINT(%s %s)');"
        data = (obj.address, obj.name, obj.c_type, obj.coords[0], obj.coords[1])
        self.cursor.execute(SQL, data)
        self.db_engine.commit()

    def update(self, obj: Cemetery) -> None:
        '''
        Update record of database based on Cemetery object
        :param obj: Cemetery
        '''
        SQL = "UPDATE public.cemeteries SET address= %s, name= %s, type= %s, location= 'SRID=4326;POINT(%s %s)' WHERE cemetery_id = %s;"
        data = (obj.address, obj.name, obj.c_type, obj.coords[0], obj.coords[1], obj.index)
        self.cursor.execute(SQL, data)
        self.db_engine.commit()

    def delete(self, id: int) -> None:
        '''
        Delete record based on id
        :param id: int
        '''
        SQL = "DELETE FROM public.cemeteries WHERE cemetery_id= %s;"
        self.cursor.execute(SQL, (id, ))
        self.db_engine.commit()

    def get_cemetery_workers(self, name: str) -> list[tuple[str, float, float]]:
        '''
        Return list of tuples(name, latitude, longitude) for all workers where cemetery name is equal to name
        :param name: str
        :return: list[tuple[str, float, float]]
        '''
        SQL = "SELECT name, latitude, longitude FROM public.cemetery_worker_view WHERE cemetery = %s;"
        self.cursor.execute(SQL, (name,))
        entries = self.cursor.fetchall()
        return [(entry[0], entry[1], entry[2]) for entry in entries]

    def get_cemetery_clients(self, name: str) -> list[tuple[str, float, float]]:
        '''
        Return list of tuples(name, latitude, longitude) for all clients where cemetery name is equal to name
        :param name: str
        :return: list[tuple[str, float, float]]
        '''
        SQL = "SELECT name, latitude, longitude FROM public.cemetery_client_view WHERE cemetery = %s;"
        self.cursor.execute(SQL, (name,))
        entries = self.cursor.fetchall()
        return [(entry[0], entry[1], entry[2]) for entry in entries]

class WorkerRepository(Repository[Worker]):
    '''
    Repository class for Worker object that contains all methods for database operations
    '''
    def __init__(self):
        super().__init__()
        self.db_engine = None
        self.cursor = None
        self.db_connection()

    def db_connection(self):
        '''
        Create connection to local PostgreSQL database
        '''
        self.db_engine = psycopg2.connect(
            user="postgres",
            database="cemetery_database",
            password="postgres",
            port="5432",
            host="localhost",
        )
        self.cursor = self.db_engine.cursor()

    def get(self, id: int) -> Worker:
        '''
        Gets all values from record based on id
        :param id: int
        :return: Worker
        '''
        SQL = "SELECT *, ST_X(location::geometry), ST_Y(location::geometry) FROM public.workers WHERE worker_id= %s;"
        self.cursor.execute(SQL, (id,))
        entry = self.cursor.fetchone()
        return Worker(index=entry[0], address=entry[1],name=entry[2], surname= entry[3], age= entry[4], cemetery=entry[5],coords= [entry[-2], entry[-1]])

    def get_all(self) -> list[Worker]:
        '''
        Return list of Worker objects with parameters form database. List length depend on number of records
        :return: list[Worker]
        '''
        SQL = "SELECT *, ST_X(location::geometry), ST_Y(location::geometry) FROM public.workers;"
        self.cursor.execute(SQL)
        entries = self.cursor.fetchall()
        return [Worker(index=entry[0] ,address=entry[1],name=entry[2], surname= entry[3], age= entry[4], cemetery=entry[5],coords= [entry[-2], entry[-1]]) for entry in entries]

    def add(self, obj: Worker) -> None:
        '''
        Adds Worker object to database
        :param obj: Worker
        '''
        SQL = "INSERT INTO public.workers(address, name, surname, age, cemetery, location) VALUES (%s, %s, %s, %s, %s, 'SRID=4326;POINT(%s %s)');"
        data = (obj.address, obj.name, obj.surname, obj.age, obj.cemetery, obj.coords[0], obj.coords[1])
        self.cursor.execute(SQL, data)
        self.db_engine.commit()

    def update(self, obj: Worker):
        '''
        Update record of database based on Worker object
        :param obj: Worker
        '''
        SQL = "UPDATE public.workers SET address= %s, name= %s, surname= %s, age= %s, cemetery= %s, location= 'SRID=4326;POINT(%s %s)' WHERE worker_id= %s;"
        data = (obj.address, obj.name, obj.surname, obj.age, obj.cemetery, obj.coords[0], obj.coords[1], obj.index)
        self.cursor.execute(SQL, data)
        self.db_engine.commit()

    def delete(self, id: int) -> None:
        '''
        Delete record based on id
        :param id: int
        '''
        SQL = "DELETE FROM public.workers WHERE worker_id= %s;"
        self.cursor.execute(SQL, (id, ))
        self.db_engine.commit()

class ClientRepository(Repository[Worker]):
    '''
    Repository class for Client object that contains all methods for database operations
    '''
    def __init__(self):
        super().__init__()
        self.db_engine = None
        self.cursor = None
        self.db_connection()

    def db_connection(self):
        '''
        Create connection to local PostgreSQL database
        '''
        self.db_engine = psycopg2.connect(
            user="postgres",
            database="cemetery_database",
            password="postgres",
            port="5432",
            host="localhost",
        )
        self.cursor = self.db_engine.cursor()


    def get(self, id: int) -> Client:
        '''
        Gets all values from record based on id
        :param id: int
        :return: Client
        '''
        SQL = "SELECT *, ST_X(location::geometry), ST_Y(location::geometry) FROM public.clients WHERE client_id= %s;"
        self.cursor.execute(SQL, (id,))
        entry = self.cursor.fetchone()
        return Client(index=entry[0], address= entry[1],name=entry[2], client_type=entry[3], nip=entry[4],phone=entry[5], cemetery=entry[6], coords=[entry[-2], entry[-1]])

    def get_all(self) -> list[Client]:
        '''
        Return list of Client with parameters form database. List length depend on number of records
        :return: list[Client]
        '''
        SQL = "SELECT *, ST_X(location::geometry), ST_Y(location::geometry) FROM public.clients;"
        self.cursor.execute(SQL)
        entries = self.cursor.fetchall()
        return [Client(index=entry[0], address= entry[1],name=entry[2], client_type=entry[3], nip=entry[4],phone=entry[5], cemetery=entry[6], coords=[entry[-2], entry[-1]]) for entry in entries]

    def add(self, obj: Client) -> None:
        '''
        Adds Client object to database
        :param obj: Client
        '''
        SQL = "INSERT INTO public.clients(address, name, type, nip, phone_number, cemetery, location) VALUES (%s, %s, %s, %s, %s, %s, 'SRID=4326;POINT(%s %s)');"
        data = (obj.address, obj.name,obj.client_type,obj.nip, obj.phone, obj.cemetery , obj.coords[0], obj.coords[1])
        self.cursor.execute(SQL, data)
        self.db_engine.commit()

    def update(self, obj: Client) -> None:
        '''
        Update record of database based on Client object
        :param obj: Client
        '''
        SQL = "UPDATE public.clients SET address= %s, name= %s, type = %s, nip = %s, phone_number = %s, cemetery= %s, location= 'SRID=4326;POINT(%s %s)' WHERE client_id= %s;"
        data = (obj.address, obj.name,obj.client_type,obj.nip, obj.phone, obj.cemetery , obj.coords[0], obj.coords[1], obj.index)
        self.cursor.execute(SQL, data)
        self.db_engine.commit()

    def delete(self, id: int) -> None:
        '''
        Delete record based on id
        :param id: int
        '''
        SQL = "DELETE FROM public.clients WHERE client_id= %s;"
        self.cursor.execute(SQL, (id, ))
        self.db_engine.commit()

class LoginDataRepository:
    '''
    Class that manages all repositories
    '''
    def __init__(self):
        self.db_engine = None
        self.cursor = None
        self.db_connection()

    def db_connection(self):
        '''
        Create connection to local PostgreSQL database
        '''
        self.db_engine = psycopg2.connect(
            user="postgres",
            database="cemetery_database",
            password="postgres",
            port="5432",
            host="localhost",
        )
        self.cursor = self.db_engine.cursor()

    def get_password(self, username: str) -> tuple[str, str]:
        SQL = "SELECT username, password_hash FROM public.user_auth WHERE username= %s;"
        self.cursor.execute(SQL, (username,))
        entry = self.cursor.fetchone()
        return (entry[1]) if entry else None

    def add_login_data(self, username: str, password_hash: str) -> None:
        SQL = "INSERT INTO public.user_auth(username, password_hash) VALUES (%s, %s);"
        self.cursor.execute(SQL, (username, password_hash))
        self.db_engine.commit()