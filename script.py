import os, sys, shutil, re
path_userdata = os.path.join('c:/','Program Files (x86)','Steam','userdata')
path_steam = os.path.join('c:/','Program Files (x86)','Steam','steam.exe')
dota_code = '570'
backup = 'backup'
dotakeys = 'dotakeys_personal.lst'
pattern_struct = r'"HeroAttack"\s+{[A-Za-z0-9\s"]*}\n'
pattern_key = r'"Key"\s+"\w+"\n'
rewrite = '"Key"\t\t"S"\n'

# Проверяем путь к userdata
if not os.path.exists(path_userdata):
	print(f'Directory not found: {path_userdata}')
else:
	'''В директории userdata находятся несколько UserID
	Так как мы точно не знаем нужный ID, то в скрипт с помощью аргументов можно передать UserID
	Если мы не будем передавать данный параметр, то будем просматривать всех юзеров
	и менять конфигурацию у тех, кто играет в Dota
	Code директории настроек Dota = 570'''
	dirs = []
	if len(sys.argv) == 2:
		if os.path.exists(os.path.join(path_userdata,sys.argv[1])):
			dirs.append(sys.argv[1])
		else:
			print(f'Directory not found: {os.path.join(path_userdata,sys.argv[1])}')
	else:
		dirs = os.listdir(path_userdata)
	for directory in dirs:
		if os.path.exists(os.path.join(path_userdata,directory,dota_code)):
			# word_directory = 'c:\Program Files (x86)\Steam\userdata\UserID\570\remote\cfg
			# В данной директории в файле dotakeys_personal.lst находят настройки пользователя с UserID
			word_directory = os.path.join(path_userdata,directory,dota_code,'remote','cfg')

			# Создадим каталог backup и поместим туда исходную версию dotakeys_personal.lst
			if not os.path.exists(os.path.join(word_directory,backup)):
				os.mkdir(os.path.join(word_directory,backup))
			shutil.copy(os.path.join(word_directory, dotakeys), os.path.join(word_directory,backup, 
				dotakeys + '_' + backup))

			# Считываем основной файл
			lines = ''
			with open(os.path.join(word_directory,dotakeys), 'rt') as file:
				lines = file.read()

			''' Производим замену в управлении
			С помощью паттерна находим необходимую структуру команды HeroAttack{}
			С помощью паттерна выделяем из неё ключ "Key"  "Symbol" и заменяем его на "Key" "S"
			Далее производим замену все структуры в исходном тексте и выводи сообщение 
			об осуществлённо операции'''
			strcut_attack = re.search(pattern_struct,lines)
			if strcut_attack is not None:
				new_struct = re.sub(pattern_key, rewrite, strcut_attack[0])
				lines = re.sub(strcut_attack[0], new_struct, lines)
				print(f'Change of control in: {os.path.join(word_directory,dotakeys)}')

				# Перезаписываем файл
				with open(os.path.join(word_directory,dotakeys), 'wt') as file:
					file.write(lines)
# Запускаем steam
if os.path.exists(path_steam):
	os.startfile(path_steam)