"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""
# вариант thread - с ускорением
# пингование (занимает больше всего времени) выводим отдельным потоком
# line81: thread = threading.Thread(target=ping, args=(ipv4, result, get_list), daemon=True)
# этот вариант лучше task_1.py

import os
import platform
import subprocess
import time
import threading
from ipaddress import ip_address
from pprint import pprint

result = {'Доступные узлы': "", "Недоступные узлы": ""}  # словарь с результатами

DNULL = open(os.devnull, 'w')  # заглушка, чтобы поток не выводился на экран
# https://stackoverflow.com/questions/52435965/difference-between-os-devnull-and-subprocess-pipe


def check_is_ipaddress(value):
    """
    Проверка является ли введённое значение IP адресом
    :param value: присланные значения
    :return ipv4: полученный ip адрес из переданного значения
        Exception ошибка при невозможности получения ip адреса из значения
    """
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return ipv4


def ping(ipv4, result, get_list):
    """
    создание сабпроцесса с нужным ip
    :param ipv4: ip-адрес
    :param result: доступные/недоступные узлы
    :param get_list: результаты возвращать/нет в словарь
    :return res: доступен/нет узел
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    response = subprocess.Popen(["ping", param, '1', str(ipv4)], stdout=subprocess.PIPE)
    if response.wait() == 0:
        result["Доступные узлы"] += f"{str(ipv4)}\n"
        res = f"{str(ipv4)} - Узел доступен"
        if not get_list:  # если результаты не надо добавлять в словарь, значит отображаем
            print(res)
        return res
    else:
        result["Недоступные узлы"] += f"{ipv4}\n"
        res = f"{str(ipv4)} - Узел недоступен"
        if not get_list:  # если результаты не надо добавлять в словарь, значит отображаем
            print(res)
        return res


def host_ping(hosts_list, get_list=False):
    """
    Проверка доступности хостов
    :param hosts_list: список хостов
    :param get_list: признак нужно ли отдать результат в виде словаря (для задания #3)
    :return словарь результатов проверки, если требуется
    """
    print("Начинаю проверку доступности узлов...")
    threads = []  # создаём список потоков
    for host in hosts_list:  # проверяем, является ли значение ip-адресом
        try:
            ipv4 = check_is_ipaddress(host)
        except Exception as e:
            print(f'{host} - {e} воспринимаю как доменное имя')
            ipv4 = host

        # создаём поток по кажд хосту
        thread = threading.Thread(target=ping, args=(ipv4, result, get_list), daemon=True)
        thread.start()  # запускаем поток по кажд хосту
        threads.append(thread)   # добавляем поток в список

    for thread in threads:  # чтобы иметь результат, нам нужно присоединиться к потоку
        thread.join()  # присоединяемся осн поток программы к каждому потоку
        # присоединяемся ко всем потокам вне цикла <for host in hosts_list>,
        # поскольку в цикле join() задержит подключение след потока до завершения предыдущего

    if get_list:  # если требуется вернуть словарь (для задачи №3), то возвращаем
        return result


if __name__ == '__main__':
    # список проверяемых хостов
    hosts_list = ['192.168.8.1', '8.8.8.8', 'yandex.ru', 'google.com',
                  '0.0.0.1', '0.0.0.2', '0.0.0.3', '0.0.0.4', '0.0.0.5',
                  '0.0.0.6', '0.0.0.7', '0.0.0.8', '0.0.0.9', '0.0.1.0']
    start = time.time()
    host_ping(hosts_list)
    end = time.time()
    print(f'total time: {int(end - start)}')
    pprint(result)
