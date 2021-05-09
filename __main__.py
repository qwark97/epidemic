from epidemic.animals_based_on_table import provide_animals
from epidemic.epidemy_state import Model
from epidemic.mocked_database import State

import matplotlib.pyplot as plt
import numpy as np


def run():
    m = Model(provide_animals())
    first_group_born_rates = [0.13, 0.14, 0.15, 0.16, 0.17]  # age between [2-4]
    second_group_born_rates = [0.09, 0.10, 0.11]             # age between [5-6]
    state = State(m)
    state.save()
    number_of_stages = 7
    for i in range(number_of_stages+1):
        print(f'faza: {i}')
        print('wszystkie żywe:', len(m.animals))
        print('\tzdrowe:', len([animal for animal in m.animals if not animal.is_sick]))
        print('\tchore:', len([animal for animal in m.animals if animal.is_sick]))
        print('\t\tfaza 1:', len([animal for animal in m.animals if animal.is_in_first_phase]))
        print('\t\tfaza 2:', len([animal for animal in m.animals if animal.is_in_second_phase]))
        print('do tej pory zmarłe:', len(m.all_dead_animals))
        print('---')

        m.next_timeframe(first_group_born_rates, second_group_born_rates)

    results = State.load()
    create_plot(results)


def create_plot(data):
    stages = []
    all_living_animals = []
    all_sick_animals = []
    all_sick_animals_first_phase = []
    all_sick_animals_second_phase = []
    all_immune_animals = []
    all_dead_animals = []
    animals_dead_in_t = []

    for stage in data:
        stages.append(stage['t'])
        all_living_animals.append(stage['all_living_animals'])
        all_sick_animals.append(stage['all_sick_animals'])
        all_sick_animals_first_phase.append(stage['all_sick_animals_first_phase'])
        all_sick_animals_second_phase.append(stage['all_sick_animals_second_phase'])
        all_immune_animals.append(stage['all_immune_animals'])
        all_dead_animals.append(stage['all_dead_animals'])
        animals_dead_in_t.append(stage['animals_dead_in_t'])

    stages = np.array(stages)
    all_living_animals = np.array(all_living_animals)
    all_sick_animals = np.array(all_sick_animals)
    all_sick_animals_first_phase = np.array(all_sick_animals_first_phase)
    all_sick_animals_second_phase = np.array(all_sick_animals_second_phase)
    all_immune_animals = np.array(all_immune_animals)
    all_dead_animals = np.array(all_dead_animals)
    animals_dead_in_t = np.array(animals_dead_in_t)

    # show a legend on the plot
    # naming the x axis
    plt.xlabel('Etapy zarazy')
    # naming the y axis
    plt.figure(figsize=(19.2, 10.8))
    plt.title('Wykres przedstawiający sytuację zwierzaków')
    plt.plot(stages, all_living_animals, label="Żyjące", color='blue')
    plt.plot(stages, all_sick_animals, label="Chore", color='red')
    plt.plot(stages, all_sick_animals_first_phase, label="Chore - faza pierwsza", linestyle='dotted', color='orange')
    plt.plot(stages, all_sick_animals_second_phase, label="Chore - faza druga", linestyle='dotted', color='magenta')
    plt.scatter(stages, all_immune_animals, label="Odporne", color='green')
    plt.plot(stages, all_dead_animals, label="Wszystkie dotychczas zmarłe", color='black')
    plt.plot(stages, animals_dead_in_t, label="Zmarłe na danym etapie", color='grey')

    plt.legend()
    plt.savefig("results.png")


if __name__ == '__main__':
    run()
