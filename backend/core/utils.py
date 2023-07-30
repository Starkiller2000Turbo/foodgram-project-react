from typing import Union


def BooleanNone(element: Union[str, int]) -> Union[None, bool]:
    """Функция преобразования значения в False, True и None.

    Agrs:
        string: Элемент, который необходимо преобозовать.

    Returns:
        True: Если элемент имеет значения 1, '1', 'yes', 'true'.
        False: Если элемент имеет значения 0, '0', 'no', 'false'.
        None: В других случаях.
    """
    response = None
    if element == 0:
        response = False
    if element == 1:
        response = True
    if isinstance(element, str):
        if element.lower() in ['0', 'no', 'false']:
            response = False
        if element.lower() in ['1', 'yes', 'true']:
            response = True
    return response
