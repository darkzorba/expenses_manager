import inspect
import traceback

from typing import Callable

from expenses_back.fn.base import ValidationError


class Response:
    def __init__(
            self,
            desc_error: str,
            desc_success: str = '',
            return_list: list = None,
            is_keep_result: bool = False,
    ):
        self.desc_success = desc_success
        self.desc_error = desc_error
        self.return_list = return_list or []
        self.is_keep_result = is_keep_result

    def __call__(self, function) -> Callable[..., dict]:
        def wrapper(*args, **kwargs):
            response = {
                'status': True,
                'status_code': 200,
                'description': self.desc_success,
            }
            result = None
            try:
                result = function(*args, **kwargs)

            except ValidationError as e:


                response['status'] = False
                response['status_code'] = e.status_code
                response['description'] = e.message
                result = e.result

            except Exception as e:

                response['status'] = False
                response['status_code'] = 500
                response['description'] = self.desc_error

            if self.is_keep_result:
                return result

            if result is not None:
                try:
                    if not self.return_list:
                        response['result'] = result

                    elif isinstance(result, dict):
                        response[self.return_list[0]] = result

                    elif isinstance(result, tuple):
                        for key_name, value in zip(self.return_list, result):
                            response[key_name] = value

                    elif len(self.return_list) == 1:
                        response[self.return_list[0]] = result

                except Exception as e:

                    response['status'] = False
                    response['status_code'] = 500
                    response['description'] = 'Decorator Error!'
            else:
                if self.return_list:
                    for result in self.return_list:
                        response[result] = None

            return response

        # Add the decorator parameters to the wrapper function's signature
        wrapper.__signature__ = inspect.signature(function)

        return wrapper
