import hashlib

# Константы
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Начальные значения восьми переменных
H = [
    0x6a09e667, 0xbb67ae85,
    0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c,
    0x1f83d9ab, 0x5be0cd19
]

# Функция циклического сдвига вправо
def right_rotate(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff

# Основная функция SHA-256
def sha256(message):
    # 1. Преобразуем исходное сообщение в байты
    data = bytearray(message.encode("utf-8"))
    original_length = len(data) * 8   # запоминаем исходную длину сообщения в битах
    data.append(0x80)                 # добавляем один байт 10000000 (бит окончания сообщения)
    while len(data) % 64 != 56:       # добавляем нули, пока длина не станет равна 56 по модулю 64
        data.append(0)
    data += original_length.to_bytes(8, byteorder="big") # добавляем исходную длину сообщения в виде 64-битного числа
    h = H.copy()   # создаём копию начальных значений SHA-256

    # 2. Разбиваем сообщение на блоки по 512 бит
    for block_start in range(0, len(data), 64):
        block = data[block_start:block_start + 64]   # получаем один блок размером 64 байта
        w = []     # создаём расписание сообщения W из 64 элементов
        # первые 16 элементов получаем непосредственно из блока
        for i in range(16):
            word = int.from_bytes(
                block[i * 4:i * 4 + 4],
                byteorder="big"
            )
            w.append(word)
        # вычисляем остальные 48 элементов расписания
        for i in range(16, 64):
            s0 = (
                right_rotate(w[i - 15], 7)
                ^ right_rotate(w[i - 15], 18)
                ^ (w[i - 15] >> 3)
            )

            s1 = (
                right_rotate(w[i - 2], 17)
                ^ right_rotate(w[i - 2], 19)
                ^ (w[i - 2] >> 10)
            )

            word = (
                w[i - 16] + s0 + w[i - 7] + s1
            ) & 0xffffffff

            w.append(word)

        # 3. Подготавливаем восемь рабочих переменных
        a, b, c, d, e, f, g, hh = h
        # выполняем 64 раунда SHA-256
        for i in range(64):
            choice = (e & f) ^ (~e & g)   # Функция выбора
            majority = (a & b) ^ (a & c) ^ (b & c)   # Функция большинства
            # 1-ое промежуточное значение
            sum1 = (
                right_rotate(e, 6)
                ^ right_rotate(e, 11)
                ^ right_rotate(e, 25)
            )
            # 2-ое промежуточное значение
            sum0 = (
                right_rotate(a, 2)
                ^ right_rotate(a, 13)
                ^ right_rotate(a, 22)
            )
            # вычисляем значение T1
            t1 = (
                hh + sum1 + choice + K[i] + w[i]
            ) & 0xffffffff
            # вычисляем значение T2
            t2 = (sum0 + majority) & 0xffffffff
            # обновляем 8 рабочих переменных
            hh = g
            g = f
            f = e
            e = (d + t1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xffffffff

        # прибавляем результаты раундов к предыдущим значениям
        h[0] = (h[0] + a) & 0xffffffff
        h[1] = (h[1] + b) & 0xffffffff
        h[2] = (h[2] + c) & 0xffffffff
        h[3] = (h[3] + d) & 0xffffffff
        h[4] = (h[4] + e) & 0xffffffff
        h[5] = (h[5] + f) & 0xffffffff
        h[6] = (h[6] + g) & 0xffffffff
        h[7] = (h[7] + hh) & 0xffffffff

    # 4. Преобразуем восемь чисел в 1 шестнадцатеричную строку
    result = ""
    for value in h:
        result += format(value, "08x")

    return result   # готовый хеш


# 5. Получаем произвольное сообщение
user_text = input("Введите произвольное сообщение: ")
# создаём список из трёх сообщений для проверки
messages = [
    ("Пустая строка", ""),
    ("Строка abc", "abc"),
    ("Сообщение пользователя", user_text)
]
# проверяем все три сообщения
for name, message in messages:
    # вычисляем хеш с помощью собственной реализации
    my_hash = sha256(message)
    # вычисляем хеш с помощью библиотеки hashlib
    library_hash = hashlib.sha256(
        message.encode("utf-8")
    ).hexdigest()

    # 6. Выводим результаты проверки
    print("Название:", name)
    print("Исходное сообщение:", repr(message))
    print("Хеш собственной реализации:", my_hash)
    print("Хеш из hashlib:", library_hash)
    # сравниваем два полученных хеша
    if my_hash == library_hash:
        print("Результат сравнения: Хеши совпадают")
    else:
        print("Результат сравнения: Хеши НЕ совпадают")