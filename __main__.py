from epidemic.animals_based_on_table import provide_animals
from epidemic.epidemy_state import Model
from epidemic.mocked_database import State

import matplotlib.pyplot as plt
import numpy as np


def run():
    m = Model(provide_animals())

    state = State(m)
    state.save()
    number_of_stages = 10
    table_head = "Wiek || Zdrowe | Odporne | Chore | Faza1 | Faza2 | Żywe | Do tej pory zmarłe"
    table_row_pattern = "%4s || %6s | %7s | %5s | %5s | %5s | %4s | %19s"
    for i in range(number_of_stages+1):
        summed_healthy = 0
        summed_immune = 0
        summed_sick = 0
        summed_phase_1 = 0
        summed_phase_2 = 0
        summed_alive = 0
        summed_already_dead = 0

        parsed = _parse_animals(m)
        print(f'Faza: {i}')
        print(table_head)
        ages = sorted(parsed.keys())
        for age in ages:
            healthy = parsed.get(age, {}).get('healthy', 0)
            immune = parsed.get(age, {}).get('immune', 0)
            sick = parsed.get(age, {}).get('sick', 0)
            phase_1 = parsed.get(age, {}).get('phase_1', 0)
            phase_2 = parsed.get(age, {}).get('phase_2', 0)
            alive = parsed.get(age, {}).get('alive', 0)
            already_dead = parsed.get(age, {}).get('already_dead', 0)

            print(table_row_pattern % (str(age), str(healthy), str(immune), str(sick), str(phase_1), str(phase_2), str(alive), str(already_dead)))

            summed_healthy += healthy
            summed_immune += immune
            summed_sick += sick
            summed_phase_1 += phase_1
            summed_phase_2 += phase_2
            summed_alive += alive
            summed_already_dead += already_dead

        print('='*77)
        print(table_row_pattern % ('Suma', str(summed_healthy), str(summed_immune), str(summed_sick), str(summed_phase_1), str(summed_phase_2), str(summed_alive), str(summed_already_dead)))
        print()
        m.next_timeframe()

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


def _parse_animals(model):
    res = {}
    for animal in model.animals:
        age = animal.age
        if not res.get(age):
            res[age] = {}

        try:
            res[age]['alive'] += 1
        except KeyError:
            res[age]['alive'] = 1

        if animal.is_immune:
            try:
                res[age]['immune'] += 1
            except KeyError:
                res[age]['immune'] = 1

        if animal.is_sick:
            try:
                res[age]['sick'] += 1
            except KeyError:
                res[age]['sick'] = 1
        else:
            try:
                res[age]['healthy'] += 1
            except KeyError:
                res[age]['healthy'] = 1

        if animal.is_in_first_phase:
            try:
                res[age]['phase_1'] += 1
            except KeyError:
                res[age]['phase_1'] = 1

        if animal.is_in_second_phase:
            try:
                res[age]['phase_2'] += 1
            except KeyError:
                res[age]['phase_2'] = 1

    for dead_animal in model.all_dead_animals:
        age = dead_animal.age
        if not res.get(age):
            res[age] = {}
        try:
            res[age]['already_dead'] += 1
        except KeyError:
            res[age]['already_dead'] = 1

    return res


if __name__ == '__main__':
    run()
