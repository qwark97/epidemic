import random

from epidemy.mocked_database import State
from epidemy.zwierzok import Zwierzok


class Model:
    def __init__(self, animals: [Zwierzok]):
        self.__t = 0
        self.__animals_number = len(animals)
        self.__animals = animals

    @staticmethod
    def __is_sick(sickness_percentage: int):
        sickness_percentage = int(sickness_percentage)
        return random.choice([False for _ in range(100-sickness_percentage)] + [True for _ in range(sickness_percentage)])

    @property
    def animals(self):
        return [animal for animal in self.__animals if animal.is_alive]

    def __birthrate_action(self, first_group_rate, second_group_rate):
        sick_percentage_in_first_group, sick_percentage_in_second_group = None, None
        first_group = len([animal for animal in self.__animals if animal.age in [2, 3, 4] and animal.is_alive])
        second_group = len([animal for animal in self.__animals if animal.age in [5, 6] and animal.is_alive])

        new_animals_from_first_group = int(first_group * first_group_rate)
        new_animals_from_second_group = int(second_group * second_group_rate)
        new_animals = []
        if new_animals_from_first_group:
            sick_percentage_in_first_group = sum([animal.is_sick for animal in self.__animals if animal.age in [2, 3, 4] and animal.is_alive]) / first_group
        if new_animals_from_second_group:
            sick_percentage_in_second_group = sum([animal.is_sick for animal in self.__animals if animal.age in [5, 6] and animal.is_alive]) / second_group

        if sick_percentage_in_first_group:
            for _ in range(new_animals_from_first_group):
                is_sick = self.__is_sick(int(sick_percentage_in_first_group * 100))
                new_animals.append(Zwierzok(
                    age=1,
                    is_sick=is_sick,
                    phase_one=is_sick,
                    phase_two=False,
                    is_immune=False
                ))

        if sick_percentage_in_second_group:
            for _ in range(new_animals_from_second_group):
                is_sick = self.__is_sick(int(sick_percentage_in_second_group * 100))
                new_animals.append(Zwierzok(
                    age=1,
                    is_sick=is_sick,
                    phase_one=is_sick,
                    phase_two=False,
                    is_immune=False
                ))

        self.__animals += new_animals

    def next_timeframe(self,
                       first_group_born_rates: [float],
                       second_group_born_rates: [float]
                       ):
        self.__t += 1
        self.__age_up()
        # self.__next_stage_of_desease()
        self.__birthrate_action(
            first_group_rate=random.choice(first_group_born_rates),
            second_group_rate=random.choice(second_group_born_rates),
        )
        # self.__getting_infected()
        # self.__deth_due_to_desease()
        self.__natural_death()
        state = State(self)
        state.save()

    def __age_up(self):
        for animal in self.animals:
            animal.age_up()

    def __natural_death(self):
        natural_death_ages = [5, 6, 7]
        for animal in self.animals:
            if animal.age > random.choice(natural_death_ages):
                animal.die()

    @property
    def t(self):
        return self.__t

    @property
    def all_dead_animals(self):
        return [animal for animal in self.__animals if not animal.is_alive]
