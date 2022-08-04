# coding=utf-8

class RingBuffer:
    """
    Буфер на списке проинициалилзирован сразу, но доступ к элементам закрыт пока
    self.__length == 0
    Элементы списка перезаписываются с начала по переполниии. Сложность операций
    на буфере O(1)

    add(x) - добавляет значение x в конец

    remove() - удаляет значение из начала

    pop() - возвращает удаляемый из начала элемент

    get(number) - возвращает элемент по номеру number, если он корректный, по
    умолчанию первый
    """

    def __init__(self, size=1):
        self.__size = size
        self.__start = 0
        self.__end = 0
        self.__buffer = [None] * size
        self.__length = 0

    # добавить элемент
    def add(self, x):
        self.__buffer[self.__end] = x
        self.__end = (self.__end + 1) % self.__size
        if self.__start + 1 == self.__end and self.__length == self.__size:
            self.__start = (self.__start + 1) % self.__size
        if self.__length < self.__size:
            self.__length += 1

    # удалить элемент
    def remove(self):
        if self.__length == 0:
            raise StopIteration("buffer index out of range")
        self.__start = (self.__start + 1) % self.__size
        self.__length -= 1

    # вернуть и удалить элемент
    def pop(self):
        if self.__length == 0:
            raise StopIteration("buffer index out of range")
        x = self.__buffer[self.__start]
        self.__start = (self.__start + 1) % self.__size
        self.__length -= 1
        return x

    # вернуть текущий или на некотором расстоянии элемент
    def get(self, num=-1):
        if self.__length == 0:
            raise StopIteration("buffer index out of range")
        if num == -1:
            num = self.__start
        elif num >= self.__length or num < 0:
            raise StopIteration("buffer index out of range")
        else:
            num = (num + self.__start) % self.__size
        return self.__buffer[num]


class RingNodeBuffer:
    """
    Буфер на узлах.
    Элементы перезаписываются с начала по переполниии. Сложность операций на
    буфере O(1). Так как списка нет, нет индексов, потому получить элемент с
    номером потребует N операций, потому реализовывать не стал. Функции ниже
    также имеют сложность по времени и по памяти O(1).
    Из преимуществ, в среднем она будет использовать меньше памяти, чем список
    фиксированной длины. Взамен при добавлении всегда создается новый объект,
    что может отъедать скорость. Ещё плюс - меньше указателей, простое
    определение начала и конца.

    add(x) - добавляет значение x в конец

    remove() - удаляет значение из начала

    get() - возвращает первый элемент, если он существует
    """

    class __Node:
        def __init__(self, value, next=None):
            self.value = value
            self.next = next

    def __init__(self, size=1):
        self.__head = None
        self.__length = 0
        self.__size = size
        self.__tail = self.__head

    def add(self, value):
        if self.__length == self.__size:
            self.__head = self.__head.next
            self.__length -= 1
        if self.__head is None:
            self.__head = self.__Node(value)
            self.__tail = self.__head
            self.__length = 1
        else:
            self.__tail.next = self.__Node(value)
            self.__tail = self.__tail.next
            self.__length += 1

    def remove(self):
        if self.__head is None:
            raise BufferError("buffer is empty")
        self.__length -= 1
        self.__head = self.__head.next
        if self.__length == 0:
            self.__tail = None

    def get(self):
        if self.__head is None:
            raise BufferError("buffer is empty")
        return self.__head.value


def test_one(x):
    try:
        print x.get()
    except Exception:
        print "буфер пуст"
    try:
        delete_and_get(x)
    except Exception:
        print "буфер пуст"
    x.add(2)
    print x.get()
    if isinstance(x, RingBuffer):
        try:
            print x.get(1)
        except Exception:
            print "второго элемента ещё нет"
    else:
        print "Не реализовано"
    x.add(3)
    delete_and_get(x)
    print ""


def test_two(x):
    x.add(1)
    x.add(2)
    x.add(3)
    print x.get()
    if isinstance(x, RingBuffer):
        try:
            print x.get(3)
        except Exception:
            print "элементов меньше 4"
    else:
        print "Не реализовано"
    x.add(4)
    if isinstance(x, RingBuffer):
        print x.get(3)
        try:
            print x.get(4)
        except Exception:
            print "элементов меньше 5"
    else:
        print "Не реализовано"
    x.add(5)
    print x.get()
    x.remove()
    delete_and_get(x)
    delete_and_get(x)
    delete_and_get(x)
    try:
        delete_and_get(x)
    except Exception:
        print "буфер пуст"
    print ""


def delete_and_get(x):
    if isinstance(x, RingBuffer):
        print x.pop()
    else:
        print x.get()
        x.remove()


def main():
    x = RingBuffer()
    test_one(x)
    x = RingBuffer(4)
    test_two(x)

    x = RingNodeBuffer()
    test_one(x)
    x = RingNodeBuffer(4)
    test_two(x)


main()
