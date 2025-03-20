from expenses_back.fn.base import SQLQuery
from expenses_back.fn.decorator import Response


class Expenses(SQLQuery):
    def __init__(self):
        super().__init__()

    @Response(desc_error="Error when searching expenses.", lista_retornos=['expenses'])
    def get_expenses_by_month(self,month:int) -> dict:
        ls_expenses = self.select(
        query=f"""
        select TO_CHAR(e.date_expense, 'YYYY-MM-DD') as date_expense,
               e.value::float,
               type.name,
               e.description
        from public.expenses e
            left join public.expense_type type
                on type.id = e.type_id
        where extract(month from e.date_expense) = :month

        """,parametros=dict(month=month)
        )

        total_income = self.select(query="""select sum(i.value)::float 
                                            from public.incomes i 
                                            where extract(month from i.date_income) = :month""",parametros=dict(month=month),
                                   is_primeiro=True,is_values_list=True) or 0

        total_expenses = sum(i['value'] for i in ls_expenses)

        for i in ls_expenses:
            i['expense_percent'] = round(i['value']/total_expenses * 100,2) if total_expenses > 0 else 0
            i['income_percent'] = round(i['value']/total_income * 100,2) if total_income > 0 else 0
        return {
            'list_expenses': ls_expenses,
            'total_expenses': total_expenses,
            'total_income':total_income
        }

    @Response(desc_error="Error trying to save expense.",lista_retornos=['dict_expense'])
    def save_expanse(self,description:str,date:str,value:float,type:str|int,id:str|int=None) -> dict:
        dict_expense={
            'description':description,
            'date_expense':date,
            'value':value,
            'type_id':type
        }
        if id:
            dict_expense['id'] = id

        id_return = self.save(table_name='expenses',dict_save=dict_expense)
        dict_expense['id'] = id_return if not id else id

        return dict_expense

    @Response(desc_error="Error trying to delete expense.",lista_retornos=[])
    def delete_expense(self,expense_id:str|int):

        id_return = self.update(table_name='expenses',dict_update=dict(status=False),dict_filter=dict(id=expense_id),
                                is_values_list=True)
        if not id_return:
            raise Exception()
