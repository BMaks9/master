Типы задач:
1. Работоспособность канала
![[Pasted image 20260719174242.png]]
Ответ:
```
	generate exp(1, l) ; пуассоновский пакет
	gate ls 1 ; устанавливаем ключ на поломку
	seize can ; занимаем канал
	advance 15, 5 ; передаем пакеты (центр, отклонение)
	release can ; отпускаем канал
	terminate ; передача завершена
	
	generate 0, 0, 0, 1 - запускаем 1 транзакту в начальный момент времени
beg logic s 1; канал работоспособен
	advance t работает
	logic r 1; ломаем канал
	advance n ; чиним
	transfer ,beg ; повторяем
	
```
Справка, как работает:
![[Pasted image 20260719174114.png|419]]

![[Pasted image 20260719175858.png]]
Ответ:
```
	generate (exp(1, l))
	gate ls 1
	seize can
	advance 60, 20
	release can
	terminate
	
generate 0, 0, 0, 1
beg logic s 1
	advanсe tr
	logic r 1
	advance td
	transfer , beg
```

2. Обработка очереди
![[Pasted image 20260719181508.png]]
Ответ:
```
grp storage 10
	 generate (exp(1, l))
	 enter grp
	 advance 4, 1
	 leave grp
	 terminate
	 
	 generate 0, 0, 0, 10
beg  advance 150, 50
	 enter grp
	 advance 10
	 leave grp
	 transfer , beg
```

3. Обработка в зависимости от сложности
![[Pasted image 20260719182219.png]]

Ответ:
```
beg	generate 0, 0, 0, 10
	advance T
	assign 1, (duniform(1, 1, 10))
	gate ls 1
	seize evm
	advance p1
	release evm
	transfer , beg

met generate 0, 0, 0, 1
	logic s 1
	advance tr
	logic r 1
	advance td
	transfer , met
```

без сложности
![[Pasted image 20260719184039.png]]
Ответ:
```
	generate 0, 0, 0, 5
beg advance T
	gate ls 1
	seize server
	advance (exp(1, l))
	release server
	transfer  ,server

	generate 0, 0, 0, 1	
met logic s 1
	advance tr
	logic r 1
	advance td
	transfer  ,met
```

4. Переходы в зависимости от состояний \ вероятностей
![[Pasted image 20260719185551.png]]
Ответ:
```
	generate (exp(1, l))
	gate ls 1, mevm2
	transfer both  , , mevm2
	seize evm1
	advance 6, 3
	release evm1
	terminate

mevm2 seize evm2
	  advance 15, 3
	  release evm2
	  terminate
	
	generate 0, 0, 0, 1
beg logic s 1
	advance tr
	logic r 1
	advance td
	transfer ,beg 

```

![[Pasted image 20260719190750.png]]
Ответ:
```
	generate (exp(1, l))
	gate ls 1, mevm2
	transfer 0,7 mevm2
	seize evm1
	advance 15, 5
	relese evm1
	terminate

mevm2 seize evm2
	  advance 8, 5
	  relese evm2
	  terminate

	generate 0, 0, 0, 1
beg logic s 1
	advance tr
	logic r 1
	advance td
	transfer ,beg
	
```

5. Картинки
![[Pasted image 20260719193053.png]]

Ответ:
```

```
Билеты:
1 - ✅
2 - ✅
3 - ✅
4 - ✅
5 - ✅
6 - ✅
7 - ✅
8 -
9 -
10 -
11 - 
12 -
13 - 
14 - 
15 - ✅
17 - ✅
