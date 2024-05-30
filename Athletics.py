import sqlite3
from threading import Thread
import time
import os
import random

DATABASE = 'BigBertha.db'
Athletes = 0 
average = 0
Tallest = 0
Smallest = 1000
load = False
clear = lambda: os.system('cls')
    
def func1():
    clear()
    Req = input('Request?: ')
    if ('avg' or 'average') in Req:
        while True:
            global DATABASE
            global load
            clear()
            Year1 = input("From what year? (1896 to 2016): ")
            Year2 = input(f"To what year? ({Year1} to 2016): ")
            try:
                if int(Year2)<int(Year1):
                    print('"To" year smaller than "From" year.')
                    os._exit(os.EX_OK)
                elif (int(Year1) or int(Year2)) < 1000:
                    print('Input is must be above 1000') 
                    os._exit(os.EX_OK)
            except:
                print('Input is not a number')
                os._exit(os.EX_OK)
            break
        load = True
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            sql = "SELECT Height, Year FROM Athletics WHERE Year >= ? and Year <= ? ORDER BY Year; "
            cursor.execute(sql, (Year1,Year2))
            results = cursor.fetchall()
            #print them nicely
            global average
            for X in results:
                global Athletes
                global Tallest
                global Smallest
                height = X[0]
                height = int(height or 0)
                if height != 0:
                    Athletes += 1
                    average += height
                    if height > Tallest:
                        Tallest = height
                    elif height < Smallest and height != 0:
                        Smallest = height
            average = int(average / Athletes)
            load = False
            clear()
            print(f'Average height is {average}\nShortest height is {Smallest}\nTallest height is {Tallest}')
            os._exit(os.EX_OK)
    elif 'game' in Req:
        QName = []
        QYear = []
        QAns = []
        Correct = 0
        AthleteIDs = []
        Anmount = 4 # Anmount of questions
        for X in range(Anmount):
            AthleteIDs.append(random.randint(1,135571))
        for X in range(len(AthleteIDs)):
            with sqlite3.connect(DATABASE) as db:
                cursor = db.cursor()
                sql = (f"SELECT ID, Name, Age, Year FROM Athletics WHERE ID = {AthleteIDs[X]}; ")
                cursor.execute(sql)
                results = cursor.fetchall()
                for Z in results:
                    QName.append(Z[1])
                    QYear.append(Z[3])
                    QAns.append(Z[2])
        for X in range(len(AthleteIDs)):
            print(f'In {QYear[X]} how old is {QName[X]}?')
            print(f'DEBUG ANS: {QAns[X]}')
            msg = int(input())
            if msg == QAns[X]:
                print(f'Correct. {QName[X]} was {QAns[X]} in {QYear[X]}\n\n')
                Correct += 1
                time.sleep(2)
            else:
                print('Incorrect')
                time.sleep(2)
            clear()


        



def func2():
    global load
    global clear
    Time = 0
    while True:
        if int(Time) == 30: # time out error
            print('Error: Timed out\nMaybe something is missing?') 
            os._exit(os.EX_OK)
        if load ==  True:
            clear()
            print(f'| Proccessing    [{int(Time)}]')
            time.sleep(0.1)
            Time += 0.1
            if load ==  True:
                clear()
                print(f'/ Proccessing.   [{int(Time)}]')
                time.sleep(0.1)
                Time += 0.1
                if load ==  True:
                    clear()
                    print(f'- Proccessing..  [{int(Time)}]')
                    time.sleep(0.1)
                    Time += 0.1
                    if load ==  True:
                        clear()
                        print(f'\ Proccessing... [{int(Time)}]')
                        time.sleep(0.1)
                        Time += 0.1


if __name__ == "__main__":
    Thread(target = func1).start()
    Thread(target = func2).start()


