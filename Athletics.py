import sqlite3
from threading import Thread
import time
import os

DATABASE = 'BigBertha.db'
Athletes = 0 
average = 0
Tallest = 0
Smallest = 1000
load = False
clear = lambda: os.system('cls')
    
def func1():
    while True:
        global Year1
        global year2
        global DATABASE
        global load
        clear()
        Year1 = input("From what year? (1896 to 2016): ")
        Year2 = input(f"To what year? ({Year1} to 2016): ")
        try:
            if int(Year2)<int(Year1):
                print('"To" year smaller than "From" year')
                pass

        except:
            print('Input is not a number')
            pass
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
            year = X[1]
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
        print(f'Average height is {average}\nSmallest height is {Smallest}\nBiggest height is {Tallest}')
        os._exit(os.EX_OK)

def func2():
    global load
    global clear
    Time = 0
    while True:
        if int(Time) == 30: # time out error
            print('Error: Timed out\nMaybe there something broken?') 
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


