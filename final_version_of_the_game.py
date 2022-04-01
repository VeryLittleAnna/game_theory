def binsearch(cur_step):  # бинпоиск по массиву групп для поиска нужной
    l = 0
    r = len(variants)
    while r - l > 1:
        m = (r + l) // 2
        if variants[m][1] > cur_step:
            r = m
        else:
            l = m
    return l


def add_sign(string, sz):
    lab = Label(text=string, font=(None, sz))
    lab.grid(row=3, column=1)


def do_step(num, colour):
    global cnt, flag
    local_text = str(num)
    if (flag == 0 and colour == "green"):
        local_text += " Chances are"
    lab = Label(text=local_text, font=(None, 20), fg=colour)
    lab.grid(row=cnt, column=2)
    cnt += 1


def change_text(k):
    global text, used
    n = len(text)
    if k < 1 or k > n:
        assert False
    else:
        text = text[:k - 1] + "X" + text[k:]
        used[k] = 1
    if k >= 2:
        text = text[:k - 2] + "X" + text[k - 1:]
        used[k - 1] = 1
    if k <= n - 1:
        text = text[:k] + "X" + text[k + 1:]
        used[k + 1] = 1


def wrong_input():
    global flag_wrong_input, lab_wrong_input
    lab_wrong_input = Label(text="You've made wrong choice >:'(", font=(None, 40))
    lab_wrong_input.grid(row=3, column=1)
    flag_wrong_input = 1


def are_there_chances():
    global flag_chances, lab_chances
    if flag_chances:
        lab_chances = Label(text="Chances are you'll win", font=(None, 30))
        lab_chances.grid(row=3, column=1)
    else:
        lab_chances.destroy()
        lab_chances = Label(text="No chances XD", font=(None, 30))
        lab_chances.grid(row=3, column=1)


def draw(e):
    global used, a, b, text, m, variants, lab_wrong_input, flag_wrong_input

    def change(text):  # изменение label
        global b
        b.destroy()
        b = Label(text=text, font=(None, 60))
        b.grid(row=1, column=1)

    def reaction(event):  # на нее теперь завязано нажатие enter
        global a, text, lab_wrong_input, flag_wrong_input
        k = int(a.get())
        if used[k] == 1:
            wrong_input()
            return
        elif flag_wrong_input == 1:
            lab_wrong_input.destroy()
            flag_wrong_input = 0
        else:
            flag_wrong_input = 0
        pos2 = two_steps_of_game(k)  # ход компа
        change_text(k)
        do_step(k, "green")
        if pos2 is not None:
            change_text(pos2)
            do_step(pos2, "red")
        a.delete(0, END)
        change(text)
        print(k)

    m = int(a.get())
    text = '*' * m
    variants = []  # массив текущего деления очереди на группы
    used = [0] * (m + 1)
    used[0] = 1
    variants.append([m, 1])  # СНАЧАЛА количество элементов, ПОТОМ номер первого элемента
    b = Label(text=text, font=(None, 60))
    a.destroy()
    b.grid(row=1, column=1)
    root.unbind('<Return>')
    a = Entry()
    a.grid(row=2, column=1)
    a.bind('<Return>', reaction)


def two_steps_of_game(n):
    global variants, m, flag_chances, G, flag  # порядковый номер элемента, выбранного игроком в его ход (индексация С ЕДИНИЦЫ)
    numb = binsearch(n)  # нужный элемент массива групп (индексация С НУЛЯ)
    k = variants[numb][0]  # количество элементов/людей в нужной группе
    x = variants[numb][1]  # порядковый номер первого человека в нужной группе (индексация С ЕДИНИЦЫ)
    variants.pop(numb)  # удаление разделенной группы
    if n - x - 1 > 0:  # добавление в массив групп новых элементов после сделанного хода Возможность №1
        variants.insert(numb, [n - x - 1, x])
        numb += 1
    if x + k - n - 2 > 0:  # добавление в массив групп новых элементов после сделанного хода Возможность №2
        variants.insert(numb, [x + k - n - 2, n + 2])
    if len(variants) == 0:
        add_sign("You won!!!", 75)  # финальное сообщение о выигрыше оппонента
        return None
    res = 0
    for i in range(len(variants)):
        res ^= grundy[variants[i][0]]
    flag = 0
    step = variants[0][1]  # плохо работающая подстраховка на случай, если программа может проиграть
    numb = 0  # группа, в которой программа делает ход (индексация С НУЛЯ)
    for i in range(len(variants)):
        k = variants[i][0]  # количество элементов/людей в рассматриваемой группе
        x = variants[i][1]  # порядковый номер первого элемента рассматриваемой группы (индексация С ЕДИНИЦЫ)
        for j in range(1, variants[i][0] + 1):  # индексация номера в подгруппе С ЕДИНИЦЫ
            tempr = res  # далее магия функции Гранди
            tempr ^= grundy[variants[i][0]]
            if j - 2 > 0:
                tempr ^= grundy[j - 2]
            if k - j - 1 > 0:
                tempr ^= grundy[k - j - 1]
            if tempr == 0:
                step = j + x - 1  # порядковый номер элемента-хода программы (индексация С ЕДИНИЦЫ)
                numb = i  # группа, в которой программа делает ход
                flag = 1  # бесполезная, но приятная оптимизация
                break
        if flag == 1:
            break
    if flag == 0:
        flag_chances = 1
        #are_there_chances()
    elif flag_chances == 1:
        flag_chances = 0
        #are_there_chances()
    else:
        flag_chances = 0
    n = step  # порядковый номер элемента, выбранного игроком в его ход (индексация С ЕДИНИЦЫ)
    k = variants[numb][0]  # количество элементов/людей в нужной группе
    x = variants[numb][1]  # порядковый номер первого человека в нужной группе (индексация С ЕДИНИЦЫ)
    variants.pop(numb)  # удаление разделенной группы
    if n - x - 1 > 0:  # добавление в массив групп новых элементов после сделанного хода (Возможность №1)
        variants.insert(numb, [n - x - 1, x])
        numb += 1
    if x + k - n - 2 > 0:  # добавление в массив групп новых элементов после сделанного хода (Возможность №2)
        variants.insert(numb, [x + k - n - 2, n + 2])
    if len(variants) == 0:
        add_sign("YOU DIED!!!", 75)  # финальное сообщение о проигрыше оппонента
    return step


from tkinter import *

root = Tk()
a = Entry(root)
a.grid(row=1, column=1)
m = 0
cnt = 1
flag_wrong_input = 0
flag_chances = 0
flag = 0

grundy = [0, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 0, 5, 2, 2, 3, 3, 0, 1, 1, 3, 0, 2, 1, 1, 0, 4, 5, 2, 7, 4, 0, 1, 1,
          2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 4, 5, 5, 2, 3, 3, 0, 1, 1, 3, 0, 2, 1, 1, 0, 4, 5, 3, 7, 4, 8, 1, 1, 2, 0, 3,
          1, 1, 0, 3, 3, 2, 2, 4, 4, 5, 5, 9, 3, 3, 0, 1, 1, 3, 0, 2, 1, 1, 0, 4, 5, 3,
          7]  # великая и бесподобная функция Шпрага-Гранди (предподсчитана)
root.bind('<Return>', draw)
root.mainloop()
