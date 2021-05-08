import json

from epidemic.animals_based_on_table import provide_animals
from epidemic.epidemy_state import Model
from epidemic.mocked_database import State


def run():
    m = Model(provide_animals())
    first_group_born_rates = [0.13, 0.14, 0.15, 0.16, 0.17]  # age between [2-4]
    second_group_born_rates = [0.09, 0.10, 0.11]             # age between [5-6]
    state = State(m)
    state.save()
    for i in range(7):
        print(f'faza: {i}')
        print('wszystkie żywe:', len(m.animals))
        print('\tzdrowe:', len([animal for animal in m.animals if not animal.is_sick]))
        print('\tchore:', len([animal for animal in m.animals if animal.is_sick]))
        print('\t\tfaza 1:', len([animal for animal in m.animals if animal.is_in_first_phase]))
        print('\t\tfaza 2:', len([animal for animal in m.animals if animal.is_in_second_phase]))
        print('do tej pory zmarłe:', len(m.all_dead_animals))
        print('---')

        m.next_timeframe(first_group_born_rates, second_group_born_rates)

    x = State.load()
    with open('simulation_results.json', 'wt') as f:
        json.dump(x, f)


if __name__ == '__main__':
    run()
