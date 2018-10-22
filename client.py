import socket
import json


def print_format():
    tasks_to_print = json.loads(server.recv(1024).decode()) #deserializacja obiektu w formacie json do Pyhton obj
    for t in tasks_to_print['tasks']:
        print('ID: ' + str(t["ID"]) + '\t Opis: ' + t["Description"] + '\t Priorytet: ' + t["Priority"])


host = socket.gethostname()
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET - Gniazdo IPv4, pomiędzy dwoma procesami, SOCK_STREAM - dla gniazd TCP
                                                        #gniazda IPv4 reprezentowane są parą(host, port), gdzie host to łańcuch a port to liczba całkowita - numer portu.
server.connect((host, port)) #nawiazanie polaczenia
print(server.recv(1024).decode())  #dbior danych (max 1024 bajtów), wyswietlenie ich


while True:

    print('MENU:')
    print('1) Wyświetl listę zadań')
    print('2) Dodaj nowe zadanie')
    print('3) Usuń zadanie')
    print('4) Wyświetl listę zadań z danym priorytetem')
    print('5) Wyjście')

    client_choice = input("->")
    server.send(client_choice.encode())

    if client_choice == '1':
        print_format()
    elif client_choice == '2':
        server.send(input('Opis zadania: ').encode())
        server.send(input('Priorytet: ').encode())
        print(server.recv(1024).decode())
    elif client_choice == '3':
        server.send(input("ID zadania: ").encode())
        print(server.recv(1024).decode())
    elif client_choice == '4':
        server.send(input('Priorytet: ').encode())
        print_format()
    elif client_choice == '5':
        server.close()
        exit()
    else:
        print(server.recv(1024).decode())
