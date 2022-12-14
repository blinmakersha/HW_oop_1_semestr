from json import dumps


class ErrorSyntax(Exception):

    def __init__(self, text: str):
        """

        Args:
            text (str): text of the following error
        """
        self.text = text

    def __str__(self):
        """Returns error message."""
        return 'ErrorSyntax: {0}'.format(self.text)


class Building:
    """Initializing the House."""

    def __init__(self, floors: int, height: float, width: float, name: str):
        """

        Args:
            floors (int): the amount of floors
            height (float): the height of the building
            width (float): the width of the building
            name (str): the name of the building

        Raises:
            ErrorSyntax: the error of bad numbers
        """
        self.floors = floors
        self.height = height
        self.width = width
        self.name = name
        if not self.is_valid():
            raise ErrorSyntax('К сожалению значения неверны, попробуйте еще раз.')
        print('Данные об здании {} успешно добавлены в файл!'.format(name))

    def is_valid(self):
        """
        Checks if building is valid or not.

        Returns:
            Boolean: False or True
        """
        all_info = [self.floors, self.height, self.width]
        for info in all_info:
            if not isinstance(info, (int, float)):
                return False
            if self.floors < 1 or self.height < 1 or self.width < 1:
                return False
        return True

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(**kwargs)

    def to_dict(self):
        return self.__dict__


def write_json(building):
    """
    Adding info to file.json.

    Args:
        building (list): the parameters of the building
    """
    with open('{0}.json'.format(building.name), 'wt') as file:
        data = dumps(building.to_dict())
        file.write(data)


q_fl = 'Введите количество этажей в здании: '
q_h = 'Введите высоту здания: '
q_w = 'Введите ширину здания: '
q_n = 'Введите название здания: '
try:
    fl, hg, wg, nm = int(input(q_fl, )), int(input(q_h, )), int(input(q_w, )), input(q_n, )
except Exception:
    raise ErrorSyntax('К сожалению значения неверны, попробуйте еще раз.')


building = Building(fl, hg, wg, nm)
write_json(building)
