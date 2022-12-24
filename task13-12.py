from threading import Thread, Condition, Lock
from time import sleep
from random import choice


class Writer(Thread):

    WRITING = .1
    RESTING = 1

    def __init__(self, name: str, text: str):
        """

        Args:
            name (str): the name of the writer
            text (str): the final string, that the writer want to write
        """
        super().__init__(name=name)
        self.name = name
        self.text = text

    def run(self):
        global page, lock, notifier
        while True:
            print('Писатель №{0} хочет написать: {1}'.format(self.name, self.text))
            lock.acquire()
            print('Писатель №{0} приступает к работе и убирает предыдущий текст'.format(self.name))
            page = ''
            for sym in self.text:
                with notifier:
                    page += sym
                    print('Писатель №{0} пишет: {1}'.format(self.name, page))
                    notifier.notify_all()    # снимает блокировку со всех остановленных методом wait() потоков
                sleep(Writer.WRITING)
            print('Писатель №{0} закончил писать: {1}'.format(self.name, self.text))
            lock.release()
            sleep(Writer.RESTING)


class Reader(Thread):

    def __init__(self, name: str):
        """

        Args:
            name (str): the name of the reader
        """
        super().__init__(name=name)
        self.name = name

    def run(self):
        global page, notifier
        while True:
            with notifier:
                notifier.wait()
                print('Читатель №{0} читает: {1}'.format(self.name, page))


READERS_NUMBER = 1
WRITERS_NUMBER = 5
TEXT = ['Компьютер — это велосипед для нашего сознания.',
        'Пройденный путь и есть награда.',
        'Сделай шаг, и дорога появится сама собой.',
        'Лучше взять и изобрести завтрашний день, чем переживать о том, что вчерашний был так себе.']

if __name__ == '__main__':
    notifier = Condition(Lock())
    lock = Lock()
    for num in range(READERS_NUMBER):
        Reader(str(num)).start()
    for num in range(WRITERS_NUMBER):
        Writer(num, choice(TEXT)).start()
