import random
from numpy.random import normal

from epidemic.mocked_database import State
from epidemic.zwierzok import Zwierzok


class Model:
    def __init__(self, animals: [Zwierzok]):
        self.__t = 0
        self.__animals = animals

    def next_timeframe(self):
        # powiększenie wewnętrznego licznika etapóœ pandemii
        self.__t += 1

        # podbicie wieku wszystkim żyjącym zwierzętom o 1
        self.__age_up()

        # zapisanie zwierząt, które uzyskały odporność na poprzednim etapie epidemii
        animals_with_expired_immunity = self.__animals_with_expired_immunity()

        # symulacja zarażeń oraz wszystkiego co z tym związane - szczegóły w samej metodzie
        self.__next_stage_of_disease()

        # pozbawienie odporności wszystkich zwierząt, które uzyskały ją w poprzednim etapie epidemii
        for animal in animals_with_expired_immunity:
            animal.lost_immunity()

        # symulacja narodzenia się nowych zwierząt - szczegóły w samej metodzie
        self.__birthrate_action()

        # symulacja naturalnych śmierci (z powodu wieku) - szczegóły w samej metodzie
        self.__natural_deaths()

        # aktualizacja stanu na potrzeby wykresu
        state = State(self)
        state.save()

    @property
    def animals(self):
        return [animal for animal in self.__animals if animal.is_alive]

    @property
    def all_dead_animals(self):
        return [animal for animal in self.__animals if not animal.is_alive]

    @staticmethod
    def __is_sick(sickness_percentage: int):
        sickness_percentage = int(sickness_percentage)
        return random.choice([False for _ in range(100-sickness_percentage)] + [True for _ in range(sickness_percentage)])

    def __birthrate_action(self):
        # osobno dla dwóch grup wiekowych, wyliczany jest przyrost naturalny
        # obowiązujący dla wszystkich zwięrząt (z danej grupy wiekowej) na tym etapie (w tej iteracji) pandemii
        first_group_born_rates = normal(15, 2) / 100    # age between [2-4]
        second_group_born_rates = normal(10, 1) / 100   # age between [5-6]

        sick_percentage_in_first_group, sick_percentage_in_second_group = None, None
        first_group = len([animal for animal in self.__animals if animal.age in [2, 3, 4] and animal.is_alive])
        second_group = len([animal for animal in self.__animals if animal.age in [5, 6] and animal.is_alive])

        # na podstawie wcześniej uzyskanego przyrostu naturalnego, rodzi się określona liczba zwierząt
        new_animals_from_first_group = int(first_group * first_group_born_rates)
        new_animals_from_second_group = int(second_group * second_group_born_rates)

        new_animals = []
        # na podstawie liczby chorych zwierząt z danej grupy wiekowej (rodziców) wyliczane jest prawdopodobieństwo
        # że dziecko urodzone w tej grupie będzie chore
        if new_animals_from_first_group:
            sick_percentage_in_first_group = sum([animal.is_sick for animal in self.__animals if animal.age in [2, 3, 4] and animal.is_alive]) / first_group
        if new_animals_from_second_group:
            sick_percentage_in_second_group = sum([animal.is_sick for animal in self.__animals if animal.age in [5, 6] and animal.is_alive]) / second_group

        if sick_percentage_in_first_group:
            # zgodnie z wyliczoną wartością na podstawie przyrostu naturalnego, "rodzą się" kolejne zwierzaki
            # przy czym dla każdego z osobna na podstawie wcześniej wyliczonego prawdopodobieństwa zarazenia w grupie "rodziców"
            # następuje symulacja czy zwierze urodzi się chore (w pierwszej fazie) czy tez zdrowe
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
            # zgodnie z wyliczoną wartością na podstawie przyrostu naturalnego, "rodzą się" kolejne zwierzaki
            # przy czym dla każdego z osobna na podstawie wcześniej wyliczonego prawdopodobieństwa zarazenia w grupie "rodziców"
            # następuje symulacja czy zwierze urodzi się chore (w pierwszej fazie) czy tez zdrowe
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

    def __age_up(self):
        for animal in self.animals:
            animal.age_up()

    def __natural_deaths(self):
        for animal in self.animals:
            # dla każdego zwierzaka, co fazę epidemii wyliczany jest "wiek śmierci"
            # przy założeniu długości życia 6 z odchuleniem standardowym 1;
            # jeśli w danej iteracji zwierze będzie miało więcej lat niż jego maksymalny wiek
            # to wtedy umiera śmiercią naturalną
            natural_death_age = normal(6, 1)
            if animal.age > natural_death_age:
                animal.die()

    def __next_stage_of_disease(self):
        for animal in self.animals:
            # blok dotyczący zwierząt chorych w tym momencie symulacji
            if animal.is_sick:
                # chore zwierzęta w pierwszej fazie przechodzą do fazy drugiej
                if animal.is_in_first_phase:
                    animal.is_in_first_phase = False
                    animal.is_in_second_phase = True
                else:
                    animal.is_in_second_phase = False
                    # zwierzęta, które na poprzednim etapie były w drugiej fazie zostają
                    # poddane symulacji czy przeżyją (osiągając jednorundową odporność)
                    # czy też umrą z powodu choroby - szczegóły w samej metodzie
                    self.__dance_macabre(animal)

            else:
                # jeśli zwierzę jest odporne to nie następuje symulacja czy się zarazi
                if animal.is_immune:
                    continue

                # na podstawie liczby chorych zwierząt w stosunku do wszystkich żyjących zwierząt
                # wyliczane jest prawdopodobieństwo, że dane zwierze zachoruje na chorobę;
                # prawdopodobieństwo wyliczane jest dla każdego zwierzęcia osobno na podstawie
                # na bieżąco aktualizowanych danych
                sick_animals = len([animal for animal in self.animals if animal.is_sick])
                probability_to_become_sick = int((sick_animals / len(self.animals)) * 100)
                if self.__is_sick(probability_to_become_sick):
                    animal.become_sick()

    def __animals_with_expired_immunity(self):
        animals = []
        for animal in self.animals:
            if animal.is_immune:
                animals.append(animal)
        return animals

    @staticmethod
    def __dance_macabre(animal: Zwierzok):
        # w zależności od wieku zwierzęcia, różnią się wartości na podstawie których
        # liczone jest prawdopodobieństwo śmierci / wyzdrowienia
        if animal.age <= 3:
            probability_of_death = round(normal(20, 5))
            # dla zwierząt młodszych (bądz równych) niż 3, prawdopodobieństwo wynosi 20% z odchyleniem
            # standardowym 5% (wyliczane dla każdego zwierzaka osobno);
            # zaokrąglenie wartości wynika z wymagań języka
            will_die = random.choice([False for _ in range(100-probability_of_death)] + [True for _ in range(probability_of_death)])
            if will_die:
                animal.die()
            else:
                animal.get_well()

        elif animal.age <= 5:
            probability_of_death = round(normal(30, 7))
            # dla zwierząt starszych niż 3 i młodszych (bądz równych) niż 5, prawdopodobieństwo wynosi 30% z odchyleniem
            # standardowym 7% (wyliczane dla każdego zwierzaka osobno);
            # zaokrąglenie wartości wynika z wymagań języka
            will_die = random.choice([False for _ in range(100 - probability_of_death)] + [True for _ in range(probability_of_death)])
            if will_die:
                animal.die()
            else:
                animal.get_well()

        else:
            probability_of_death = round(normal(50, 15))
            # dla zwierząt starszych niż 5, prawdopodobieństwo wynosi 50% z odchyleniem
            # standardowym 15% (wyliczane dla każdego zwierzaka osobno);
            # zaokrąglenie wartości wynika z wymagań języka
            will_die = random.choice([False for _ in range(100 - probability_of_death)] + [True for _ in range(probability_of_death)])
            if will_die:
                animal.die()
            else:
                animal.get_well()

    @property
    def t(self):
        return self.__t

    @property
    def all_dead_animals(self):
        return [animal for animal in self.__animals if not animal.is_alive]
