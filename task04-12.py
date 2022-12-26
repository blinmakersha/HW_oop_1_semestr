from multiprocessing import Process, Lock
from time import sleep
from random import randint


class Philosopher(Process):

    TIME_TO_THINK = (1, 3)
    WAITING_CHOPSTICK = 3
    EATING = 2

    def __init__(self, name: str, right_chopstick: Lock, left_chopstick: Lock):
        super().__init__()
        self.name = name
        self.right_chopstick = right_chopstick
        self.left_chopstick = left_chopstick

    def eat(self):
        chop_right = self.right_chopstick
        chop_left = self.left_chopstick
        free_rc = chop_right.acquire(timeout=Philosopher.WAITING_CHOPSTICK)
        if free_rc:
            print(f'Философ №{self.name} взял правую палочку')
        free_lc = chop_left.acquire(timeout=Philosopher.WAITING_CHOPSTICK)
        if free_lc:
            print(f'Философ №{self.name} взял левую палочку')
        if free_rc and free_lc:
            print(f'Философ №{self.name} начал кушать')
            sleep(Philosopher.EATING)
            print(f'Философ №{self.name} покушал и начинает размышлять')
        else:
            print(
                f'Философ №{self.name} не получил палочки, продолжает размышлять')
        if free_rc:
            chop_right.release()
        if free_lc:
            chop_left.release()

    def run(self):
        while True:
            print(f'Философ №{self.name} размышляет')
            sleep(randint(*Philosopher.TIME_TO_THINK))
            print(f'Философ №{self.name} уже проголодался')
            self.eat()


if __name__ == '__main__':
    PHILOSOPHERS_NUM = 5
    CHOPSTICKS = [Lock() for _ in range(PHILOSOPHERS_NUM)]
    PHILOSOPHERS = [
        Philosopher(str(num), CHOPSTICKS[num % PHILOSOPHERS_NUM],
                    CHOPSTICKS[(num + 1) % PHILOSOPHERS_NUM])
        for num in range(PHILOSOPHERS_NUM)
    ]
    for philosopher in PHILOSOPHERS:
        philosopher.start()
