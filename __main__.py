from epidemy.epidemy_state import Model


def run():
    m = Model(
        animals_number=100,
        initial_sickness=20,  # in percentages
    )
    for i in range(5):
        print(i, ':', len(m.animals))
        m.next_timeframe()
        input('---')


if __name__ == '__main__':
    run()
