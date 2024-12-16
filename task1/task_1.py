import inspect
from typing import Callable

def strict(func: Callable) -> Callable:
    def result_function(*args):

        siganture = inspect.signature(func)

        if len(siganture.parameters) != len(args): 
            raise TypeError(f'Количество аргументов в функции не совпадает!')
        
        params = list(siganture.parameters.values())

        for i in range(len(args)):

            if isinstance(i, params[i].annotation):
                raise TypeError(f'{params[i].name} не соответствует типу!')

        return func(*args)

    return result_function

