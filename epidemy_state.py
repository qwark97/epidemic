import numpy.random
import random
from epidemy.zwierzok import Zwierzok


class Model:
    def __init__(self,
                 animals_number: int,
                 initial_sickness: int):
        self.__t = 0
        self.__animals_number = animals_number
        self.__percentage_of_sick_animals_at_the_beginning = self.__initial_sickness(initial_sickness)
        self.__animals = list(self.__generate_animals(self.__animals_number, self.__percentage_of_sick_animals_at_the_beginning))

    @staticmethod
    def __initial_sickness(percentage):
        if 0 > percentage > 100 or type(percentage) != int:
            raise Exception('Percentage value must be in range [0, 100] and has to be integer')
        return percentage

    @staticmethod
    def __is_sick(sickness_percentage):
        return numpy.random.choice([False for _ in range(100-sickness_percentage)] + [True for _ in range(sickness_percentage)])

    def __generate_animals(self, number_of_animals, sickness_percentage):
        ages = numpy.random.normal(loc=3.5, size=number_of_animals)
        for age in ages:
            yield Zwierzok(int(age), self.__is_sick(sickness_percentage))

    @property
    def animals(self):
        return self.__animals

    def __birthrate_action(self, first_group_rate, second_group_rate):
        first_group = len([animal for animal in self.__animals if animal.age in [2, 3, 4] and animal.is_alive])
        second_group = len([animal for animal in self.__animals if animal.age in [5, 6] and animal.is_alive])

        new_animals_from_first_group = int(first_group * first_group_rate)
        new_animals_from_second_group = int(second_group * second_group_rate)
        new_animals = []

        sick_percentage_in_first_group = len([animal.is_sick for animal in self.__animals if animal.age in [2, 3, 4] and animal.is_alive]) // first_group
        sick_percentage_in_second_group = len([animal.is_sick for animal in self.__animals if animal.age in [5, 6] and animal.is_alive]) // second_group
        for _ in range(new_animals_from_first_group):
            new_animals.append(Zwierzok(1, self.__is_sick(sick_percentage_in_first_group)))

        for _ in range(new_animals_from_second_group):
            new_animals.append(Zwierzok(1, self.__is_sick(sick_percentage_in_second_group)))

        return new_animals

    def next_timeframe(self):
        first_group_born_rates = [0.13, 0.14, 0.15, 0.16, 0.17]
        second_group_born_rates = [0.09, 0.10, 0.11]
        animals_born = self.__birthrate_action(
            first_group_rate=random.choice(first_group_born_rates),
            second_group_rate=random.choice(second_group_born_rates),
        )
        self.__animals = self.__animals + animals_born
