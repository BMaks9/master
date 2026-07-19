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
generate 0, 0, 0, 10
advance T
assign 1, (duniform(1, 1, 10))
```