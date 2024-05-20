import sqlite3

DATABASE = 'BigBertha.db'
Athletes = 0 
average = 0
Tallest = 0
Smallest = 1000

def print_year_athletes():
    while True:
        global Year1
        global year2
        Year1 = input("From what year?: ")
        Year2 = input("To what year?: ")
        try:
            if int(Year2)<int(Year1):
                print('To year smaller than From year')
                pass


        except:
            print('Input is not a number')
            pass
        break
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = "SELECT Height, Year FROM Athletics WHERE Year >= ? and Year <= ?; "
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
        average = average / Athletes
        print(f'Average height is {average}\nSmallest height is {Smallest}\nBiggest height is {Tallest}')

if __name__ == "__main__":
    print_year_athletes()
