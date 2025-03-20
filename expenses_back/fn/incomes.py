from expenses_back.fn.base import SQLQuery
from expenses_back.fn.decorator import Response

class Incomes(SQLQuery):
    def __init__(self):
        super().__init__()


    @Response(desc_error="Error when searching expenses.", return_list=['expenses'])
    def get_incomes_by_month(self,month:str|int):
        ls_incomes = self.select(
            query=f"""
                select i.value::float,
                       i.description,
                       TO_CHAR(i.date_income,'YYYY-MM-DD') as date_income,
                       type.name,
                       i.id
                from public.incomes i
                    left join public.income_type type 
                        on type.id = i.type_id 
                    where extract(month from i.date_income) = :month and i.status = true 
                """, parameters=dict(month=month)
        )

        total_income = sum(i['value'] for i in ls_incomes)


        for i in ls_incomes:
            i['income_percent'] = i['value'] / total_income * 100 if total_income else 0

        return {
            'list_incomes': ls_incomes,
            'total_income': total_income
        }

    @Response(desc_error="Error trying to save expense.",return_list=['dict_expense'])
    def save_income(self,description:str,date:str,value:float,type:str|int,id:str|int=None):
        dict_income = {
            'description': description,
            'date_income': date,
            'value': value,
            'type_id': type,
            'status':True
        }
        if id:
            dict_income['id'] = id

        id_return = self.save(table_name='incomes', dict_save=dict_income)
        dict_income['id'] = id_return if not id else id

        return dict_income

    @Response(desc_error="Error trying to delete expense.",return_list=[])
    def delete_income(self,income_id:str|int):
        id_return = self.update(table_name='incomes',dict_update=dict(status=False),dict_filter=dict(id=income_id),
                                is_values_list=True)
        if not id_return:
            raise Exception()

    @Response(desc_error="Error trying to save income type.", return_list=['dict_type'])
    def save_income_type(self, name: str):
        dict_type = {'name': name}

        id_return = self.save(table_name='income_type', dict_save=dict_type)
        dict_type['id'] = id_return

        return dict_type
