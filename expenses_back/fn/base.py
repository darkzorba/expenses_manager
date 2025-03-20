
import os
import sqlalchemy as db
from dotenv import load_dotenv


class SQLQuery:
    def __init__(self):
        load_dotenv()

        self.resultset = []

        self.engine = db.create_engine(
            os.getenv('DATABASE_URL'),
            pool_size=15,
            max_overflow=0,
            # https://docs.sqlalchemy.org/en/20/core/pooling.html#dealing-with-disconnects
            pool_pre_ping=True,
            # pool_recycle=3600,
            pool_timeout=30,
            connect_args={
                'keepalives': 1,
                'keepalives_idle': 30,
                'keepalives_interval': 20,
                'keepalives_count': 10,
            }
                )
        with self.engine.connect() as conn:
            conn.execute(db.text('select 1'))




    def __query(self, query=None, parameters=None, is_serialized=True):
            if parameters is None:
                parameters = {}

            self.parse_list_to_tuple(parameters)

            # self.engine.dispose()
            with self.engine.begin() as conn:
                text = db.text(query)
                self.resultset = conn.execute(text, parameters)

            if self.resultset.returns_rows:
                return list(self.resultset) if not is_serialized else self.get_serialized_data()
            else:
                return None


    @staticmethod
    def parse_list_to_tuple(parameters):
        for p in parameters:
            if isinstance(parameters[p], (list, set)):
                if len(parameters[p]) > 0:
                    parameters[p] = tuple(parameters[p])
                else:
                    parameters[p] = tuple([None])

            elif isinstance(parameters[p], tuple):
                if len(parameters[p]) < 0:
                    parameters[p] = tuple([None])

    def get_serialized_data(self):
        return [row._asdict() for row in self.resultset]


    def update(self, table_name, dict_update, dict_filter, pk_name='id', is_disable=False, is_values_list=False,
               is_first=True):



        lista_columns = dict_update.keys()

        update = ','.join([f'{column} = :{column}' for column in lista_columns])

        where = ''
        for key, value in dict_filter.items():
            if isinstance(value, list):
                where += f" {key} in :{key} and"
            else:
                where += f" {key} = :{key} and"

        where = where[:-3]  # Removendo o ultimo 'and'

        query = f'update {table_name} set {update} where {where} returning {pk_name};'

        dict_update.update(dict_filter)

        result = self.__query(query=query, parameters=dict_update)

        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)


    @staticmethod
    def format_result(result=None, is_values_list=False, is_first=False):
        if not result:
            return {} if is_first else []

        if is_values_list:
            return_list = []
            for row in result:

                values = tuple(row.values())
                if len(values) == 1:
                    return_list.append(values[0])
                else:
                    return_list.append(values)

            result = return_list

        if is_first:
            return result[0]

        return result

    def select(self,query:str,parameters:dict={},is_values_list:bool=False,is_first:bool=False):

        result = self.__query(query=query,parameters=parameters,is_serialized=True)

        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)

    def save(self, table_name, dict_save, pk_name='id', is_values_list=True, is_first=True):



        is_edicao = pk_name in dict_save


        lista_columns = dict_save.keys()

        columns = ','.join(lista_columns)
        values_name = ','.join([f':{column}' for column in lista_columns])
        update = ','.join([f'{column} = :{column}' for column in lista_columns])

        query = f"""
            insert into {table_name}({columns}) values ({values_name}) 
            on conflict ({pk_name}) do update set {update} RETURNING {pk_name};
        """

        result = self.__query(query=query, parameters=dict_save)

        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)





class ValidationError(Exception):

    def __init__(self, message: str = None, status_code: int = 400, result=None):
        self.__message = message
        self.__result = result
        self.__status_code = status_code
        super().__init__(self.__message)

    @property
    def result(self):
        return self.__result

    @property
    def message(self):
        return self.__message

    @property
    def status_code(self):
        return self.__status_code
