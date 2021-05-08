DATABASE = []


class State:
    def __init__(self, model):
        self.__t = model.t
        self.__all_living_animals = len(model.animals)
        self.__all_sick_animals = len([animal for animal in model.animals if animal.is_sick])
        self.__all_sick_animals_first_phase = len([animal for animal in model.animals if animal.is_in_first_phase])
        self.__all_sick_animals_second_phase = len([animal for animal in model.animals if animal.is_in_second_phase])
        self.__all_immune_animals = len([animal for animal in model.animals if animal.is_immune])
        self.__all_dead_animals = len(model.all_dead_animals)

    def save(self):
        data = {
            't': self.__t,
            'all_living_animals': self.__all_living_animals,
            'all_sick_animals': self.__all_sick_animals,
            'all_sick_animals_first_phase': self.__all_sick_animals_first_phase,
            'all_sick_animals_second_phase': self.__all_sick_animals_second_phase,
            'all_immune_animals': self.__all_immune_animals,
            'all_dead_animals': self.__all_dead_animals,
        }
        idx = len(DATABASE)
        DATABASE.append(data)
        if idx == 0:
            DATABASE[idx]['animals_dead_in_t'] = self.__all_dead_animals
        else:
            DATABASE[idx]['animals_dead_in_t'] = self.__all_dead_animals - DATABASE[idx-1]['all_dead_animals']

    @staticmethod
    def load():
        return DATABASE
