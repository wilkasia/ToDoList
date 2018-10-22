import socket
import json

json_file = 'tasks.json'


def send_all_tasks():
    with open(json_file, 'r') as read_file:
        data = read_file.read()

    conn.send(data.encode())


def add_new_task():
    with open(json_file, 'r') as read_file:
        current_tasks = json.load(read_file)

    with open(json_file, 'w') as write_file:
        new_task = {'ID':current_tasks['tasks'][-1]["ID"] + 1 , 'Description': conn.recv(1024).decode(), 'Priority': conn.recv(1024).decode()}
        current_tasks['tasks'].append(new_task)
        write_file.write(json.dumps(current_tasks, indent=2, separators=(',', ': '))) #dumps-serializacja obiektu do formatu json


def delete_task(task_id):
    with open(json_file, 'r') as read_file:
        all_tasks = json.load(read_file)

    for element in all_tasks['tasks']:
        if element["ID"] == int(task_id):
            all_tasks['tasks'].remove(element)

    with open(json_file, 'w') as write_file:
        write_file.write(json.dumps(all_tasks, indent=2, separators=(',', ': ')))


def send_chosen_priority_tasks(priority):
    with open('tasks.json', 'r') as read_file:
        all_tasks = json.load(read_file)

    chosen_tasks = {'tasks': []}
    for element in all_tasks['tasks']:
        if element['Priority'] == priority:
            chosen_tasks['tasks'].append(element)
    tasks_to_send = json.dumps(chosen_tasks, indent=2, separators=(',', ': '))
    conn.send(tasks_to_send.encode())


host = socket.gethostname()
port = 5000

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Metoda "socket()" zwraca obiekt "socket"
mySocket.bind((host, port)) #przypisanie socketa do adresu
mySocket.listen(1)  #maximum number of queued connections

conn, address = mySocket.accept() #zaakceptowanie polaczenia, conn - nowy obiekt socket uzywany do wysylania i odbierania dannych, addr - adres przywiazany do socketa na drugim koncu polaczenia
print("Connection from: " + str(address))
conn.send("Connection successful".encode()) #wysylanie zakodowanej wiadomosci do socketa conn

while True:
    client_choice = conn.recv(1024).decode() #odbior danych od socketa, max = 1024 bajty, dekodowanie ich do stringa,
    if not client_choice:
        break

    if client_choice == '1':
        send_all_tasks()
    elif client_choice == '2':
        add_new_task()
        conn.send("Zadanie utworzono pomyślnie".encode())
    elif client_choice == '3':
        delete_task(conn.recv(1024).decode())
        conn.send("Wybrane zadanie zostało usunięte".encode())
    elif client_choice == '4':
        send_chosen_priority_tasks(conn.recv(1024).decode())
    elif client_choice == '5':
        conn.close()
        exit()
    else:
        conn.send("Nieprawidlowy wybór".encode())

conn.close()


