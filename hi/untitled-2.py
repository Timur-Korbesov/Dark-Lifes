total = 0
print('Вводите цены; для остановки введите -1.')
price = float(input())
while price > -1:
    total = total + price  # можно заменить на аналогичную запись
    # total += price
    price = float(input())
print('Общая стоимость равна', total)