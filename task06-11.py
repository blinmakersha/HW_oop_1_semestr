from multiprocessing import Queue, Process, Lock, Event
from time import sleep, strftime
from random import randint, choice


class Client:
    def __init__(self, name: str, service: str):
        self.name = name
        self.service = service


class Barber:

    WAITING_TIME = 20
    WORKING_TIME = 3,6

    def __init__(self):
        self.client_coming = Event()

    def sleep(self):
        print('Парикмахер отдыхает 😎')
        return self.client_coming.wait(timeout=Barber.WAITING_TIME)

    def call(self):
        self.client_coming.set()

    def work(self, client: Client):
        print('Парикмахер оказывает услугу: {}, для №{}'.format(client.service, client.name))
        sleep(randint(*Barber.WORKING_TIME))

    def greet(self, client: Client):
        print('Парикмахер приступает к работе №{} в {}'.format(client.name, strftime('%X')))
        self.client_coming.clear()
        self.work(client)
        print('Клиент №{} рад и уходит 😎'.format(client.name))


class HairSalon:
    def __init__(self, q_size: int, lock: Lock):
        self.q_size = q_size
        self.lock = lock
        self.__worker = Barber()
        self.__process = Process(target=self.work)
        self.__queue = Queue(maxsize=q_size)

    def open(self):
        print('Парикмахерская открывается в {}, с {} местами в очереди'.format(strftime('%X'), self.q_size))
        self.__process.start()

    def close(self):
        print('Клиентов нет, парикмахерская закрывается в {}'.format(strftime('%X')))

    def work(self):
        while True:
            self.lock.acquire()
            if self.__queue.empty():
                self.lock.release()
                work_result = self.__worker.sleep()
                if not work_result:
                    self.close()
                    break
            else:
                self.lock.release()
                client = self.__queue.get()
                self.__worker.greet(client)

    def enter(self, client: Client):
        with lock:
            print('Клиент №{} пришел в парикмахерскую, ждет своей очереди'.format(client.name))
            if self.__queue.full():
                print('Людей в очереди слишком много, клиент №{} уходит'. format(client.name))
            else:
                print('Клиент №{} выбрал услугу: {}'.format(client.name, client.service))
                self.__queue.put(client)
                self.__worker.call()


SIZE_QUEUE = 1
CLIENT_ENTER_INTERVAL = (1, 2)

SERVICES = [
    'Стрижка',
    'Окрашивание',
    'Стрижка + Окрашивание',
    'Наращивание волос',
    'Укладка']

if __name__ == '__main__':
    lock = Lock()
    names = [str(i) for i in range(5)]
    clients = [Client(name, choice(SERVICES)) for name in names]
    hair_salon = HairSalon(SIZE_QUEUE, lock)
    hair_salon.open()
    for client in clients:
        sleep(randint(*CLIENT_ENTER_INTERVAL))
        hair_salon.enter(client)
