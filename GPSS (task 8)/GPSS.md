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
	transfer 0,3 mevm2
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
Важно расставить правильно флаги, их будет два в момент передачи на каналы, а также в момент когда пакеты уже в 1 канале.

Ответ:
```
	generate (exp(1, L1))
	transfer  ,uz1 ; слияние потоков
	generate (exp(1, L2)) 
	
uz1 seize h1
	advance t1
	release h1
	gate ls 1, mc2
	transfer 1-PC, ,mc1

mc2 seize c2
	advance TC2
	release c2
	seize h3
	advance TH3
	release h3
	terminate 

mc1 seize c1
	advance TC1
	release c1
	gate ls 1
	seize h2
	advance TH2
	release h2
	terminate
	
	
	generate 0, 0, 0, 1
beg logic s 1
	advance TR
	logic r 1
	advance TD
	transfer  ,beg	
```

![[Pasted image 20260720221621.png]]

Ответ:
```
h2 storage 3
	
	generate (exp(1, l1))
	seize h1
	advance t1
	release h1
	seize c1
	advance tc1
	release c1
	transfer  ,uz2
	
	generate (exp(1, l2))
	seize h1
	advance t1
	release h1
	seize c2
	advance tc2
	release c2
	
uz2 enter h2
	advance th2
	leave h2
	terminate
	
```

![[Pasted image 20260720224014.png]]
Статистику надо собрать!

Ответ:
```
h2 storage 5
	generate (exp(1, l1))
	transfer ,uz1
	generate (exp(1, l2))

uz1 queue preb ; начало сбора статы
	seize h1
	advance t1
	release h1
	transfer 1-pc, mc1

mc2 seize c2
	advance tc2
	release c2
	transfer ,uz2

mc1 seize c1
	advance tc1
	release c1

uz2 enter h2
	advance th2
	leave h2
	depart preb ; конец сбора статы
	terminate

```

![[Pasted image 20260720223239.png]]

Ответ:
```
	generate (exp(1, l1))
	seize h1
	advance t1
	release h1

mc1 seize c1
	advance tc1
	release c1
	transfer 1-ps, mc1
	transfer ,uz2

	generate (exp(1, l2))
	seize h1
	advance t1
	release h1
	
mc2 seize c2
	advance tc2
	release c2
	transfer 1-ps, mc2

uz2 seize h2
	advance th2
	release h2
	terminate

```

![[Pasted image 20260720231652.png]]

Ответ:
```
	generate (exp(1, l1))
	seize h1
	advance t1
	release h1

mc1 seize c1
	advance tc1
	release c1
	transfer 1-ps, end
	transfer ,uz2

	generate (exp(1, l2))
	seize h1
	advance t1
	release h1
	
mc2 seize c2
	advance tc2
	release c2
	transfer 1-ps, end

uz2 seize h2
	advance th2
	release h2
end	terminate
```

![[Pasted image 20260720232730.png]]

Ответ:
```
	generate (exp(1, l1))
	transfer ,uz1
	generate (exp(1, l2))

uz1 seize h1
	advance t1
	release h1
	transfer pc, mc2

mc1 seize c1
	advance tc1
	release c1
	transfer 1-ps, mc1
	transfer ,uz2

mc2 seize c2
	advance tc2
	release c2
	transfer 1-ps, mc2

uz2 seize h2
	advance th2
	release h2
	terminate
```

![[Pasted image 20260720233352.png]]

Ответ:
```
	generate (exp(1, l1))
	transfer ,uz1
	generate (exp(1, l2))

uz1 seize h1
	advance t1
	release h1
	transfer pc, mc2

mc1 seize c1
	advance tc1
	release c1
	transfer 1-ps, end
	transfer ,uz2

mc2 seize c2
	advance tc2
	release c2
	transfer 1-ps, end

uz2 seize h2
	advance th2
	release h2
end	terminate
```
