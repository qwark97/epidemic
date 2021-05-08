from epidemy.animals_based_on_table import provide_animals
from epidemy.epidemy_state import Model
from epidemy.mocked_database import State


def run():
    m = Model(provide_animals())
    first_group_born_rates = [0.13, 0.14, 0.15, 0.16, 0.17]  # age between [2-4]
    second_group_born_rates = [0.09, 0.10, 0.11]             # age between [5-6]
    for i in range(7):
        print(i, ':', len(m.animals))
        print('chore:', sum([animal.is_sick for animal in m.animals]))
        m.next_timeframe(first_group_born_rates, second_group_born_rates)
        print('---')

    x = State.load()
    print(x)


if __name__ == '__main__':
    run()
