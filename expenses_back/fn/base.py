
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




    def __query(self, query=None, parametros=None, is_serializado=True):
            if parametros is None:
                parametros = {}

            self.parse_lista_para_tupla(parametros)

            # self.engine.dispose()
            with self.engine.begin() as conn:
                texto = db.text(query)
                self.resultset = conn.execute(texto, parametros)

            if self.resultset.returns_rows:
                return list(self.resultset) if not is_serializado else self.get_dados_serializados()
            else:
                return None


    @staticmethod
    def parse_lista_para_tupla(parametros):
        for p in parametros:
            if isinstance(parametros[p], (list, set)):
                if len(parametros[p]) > 0:
                    parametros[p] = tuple(parametros[p])
                else:
                    parametros[p] = tuple([None])

            elif isinstance(parametros[p], tuple):
                if len(parametros[p]) < 0:
                    parametros[p] = tuple([None])

    def get_dados_serializados(self):
        return [row._asdict() for row in self.resultset]


    def update(self, table_name, dict_update, dict_filter, pk_name='id', is_disable=False, is_values_list=False,
               is_primeiro=True):



        lista_colunas = dict_update.keys()

        update = ','.join([f'{coluna} = :{coluna}' for coluna in lista_colunas])

        where = ''
        for chave, valor in dict_filter.items():
            if isinstance(valor, list):
                where += f" {chave} in :{chave} and"
            else:
                where += f" {chave} = :{chave} and"

        where = where[:-3]  # Removendo o ultimo 'and'

        query = f'update {table_name} set {update} where {where} returning {pk_name};'

        dict_update.update(dict_filter)

        retorno = self.__query(query=query, parametros=dict_update)

        return self.formatar_retorno(retorno=retorno, is_values_list=is_values_list, is_primeiro=is_primeiro)


    @staticmethod
    def formatar_retorno(retorno=None, is_values_list=False, is_primeiro=False):
        if not retorno:
            return {} if is_primeiro else []

        if is_values_list:
            lista_retorno = []
            for linha in retorno:

                values = tuple(linha.values())
                if len(values) == 1:
                    lista_retorno.append(values[0])
                else:
                    lista_retorno.append(values)

            retorno = lista_retorno

        if is_primeiro:
            return retorno[0]

        return retorno

    def select(self,query:str,parametros:dict={},is_values_list:bool=False,is_primeiro:bool=False):

        retorno = self.__query(query=query,parametros=parametros,is_serializado=True)

        return self.formatar_retorno(retorno=retorno, is_values_list=is_values_list, is_primeiro=is_primeiro)

    def save(self, table_name, dict_save, pk_name='id', is_values_list=True, is_primeiro=True):



        is_edicao = pk_name in dict_save


        lista_colunas = dict_save.keys()

        colunas = ','.join(lista_colunas)
        nm_valores = ','.join([f':{coluna}' for coluna in lista_colunas])
        update = ','.join([f'{coluna} = :{coluna}' for coluna in lista_colunas])

        query = f"""
            insert into {table_name}({colunas}) values ({nm_valores}) 
            on conflict ({pk_name}) do update set {update} RETURNING {pk_name};
        """

        retorno = self.__query(query=query, parametros=dict_save)

        return self.formatar_retorno(retorno=retorno, is_values_list=is_values_list, is_primeiro=is_primeiro)





class ValidationError(Exception):

    def __init__(self, mensagem: str = None, status_code: int = 400, retorno=None):
        self.__mensagem = mensagem
        self.__retorno = retorno
        self.__status_code = status_code
        super().__init__(self.__mensagem)

    @property
    def retorno(self):
        return self.__retorno

    @property
    def mensagem(self):
        return self.__mensagem

    @property
    def status_code(self):
        return self.__status_code
