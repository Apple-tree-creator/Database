# import packages
import sqlite3 # SQL Package
from threading import Thread # Run multiple scripts at the same time
import time # pause for a few seconds
import os # Clear console
import random # Randint for game
import platform # Github codespace uses Linux to host

DATABASE = 'BigBertha.db' # The database to pull from

# set variables
Athletes = 0 
average = 0
Tallest = 0
Smallest = 1000
load = False

# Linux and Windows use different clear console commands
# to prevent a ugly console, this checks if the code has the correct Clear command
if platform.system() == 'Windows':
    clear = lambda: os.system('cls') # to clear console use 'clear()'
else:
    clear = lambda: os.system('clear')
    
def func1(): # Thread 1
    while True:
        clear()
        global load
        print('Available options:\naverage\ngame\nsearch\nexit\n')
        Req = input('Request?: ') # ask for which options
        if 'exit' in  Req:
            clear()
            print('exiting')
            os._exit(os.EX_OK)
        elif 'avg' in Req or 'average' in Req: # getting the average heights of athletes
            while True:
                global DATABASE
                clear()
                # Graph not done
                # Graph = input('Output graph?\ny\nn: ')
                # if Graph == 'y':
                #     Graph = True
                # elif Graph == 'n':
                #     Graph = False
                while True:
                    clear()
                    Querys = ('age','height','weight')
                    print('What to get average of?')
                    print('Age, Height, Weight')
                    Srch = input()
                    Srch = Srch.lower()
                    if Srch in Querys:
                        break
                    else:
                        print('Search not possible')
                        input('Press enter to continue...')
                Year1 = input("From what year? (1896 to 2016): ")
                Year2 = input(f"To what year? ({Year1} to 2016): ")
                try:
                    if int(Year2)<int(Year1):
                        print('"To" year smaller than "From" year.')
                        os._exit(os.EX_OK)
                    elif int(Year1) <= 1895 or int(Year2) >= 2017:
                        print('Input is must be in range') 
                        os._exit(os.EX_OK)
                except:
                    print('Input is not a number')
                    break
                break
            load = True
            with sqlite3.connect(DATABASE) as db:
                Graph = False
                cursor = db.cursor()
                sql = (f"SELECT {Srch}, Year FROM Athletics WHERE Year >= {Year1} and Year <= {Year2} ORDER BY Year; ") # SQL Statement
                cursor.execute(sql) # Run statement
                results = cursor.fetchall() # Get output of statement
                # Calculating the average
                global average
                if Graph == False:
                    for X in results:
                        global Athletes
                        global Tallest
                        global Smallest
                        height = X[0]
                        height = int(height or 0)
                        # The height of an athlete can be null so we want to avoid that by skipping the athlete if the height is null
                        if height != 0:
                            Athletes += 1
                            average += height
                            # This is for the tallest person and the shortest person output
                            if height > Tallest:
                                Tallest = height
                            elif height < Smallest and height != 0:
                                Smallest = height
                    # Do the average calculation
                    average = int(average / Athletes)
                    load = False # Disable loading screen
                    clear()
                    print(f'Average {Srch} is {average}\nSmallest {Srch} is {Smallest}\Largest {Srch} is {Tallest}')

                # The graph var is now uselesss
                elif Graph ==  True:
                    prevyear =  Year1
                    Athletes = 0
                    Calc = 0
                    Average = []
                    for X in results:
                        curyear =  X[1]
                        height = int(X[0] or 0)
                        if int(prevyear) == int(curyear):
                            if height != 0:
                                Calc += height
                                prevyear = X[1]
                                Athletes += 1
                            else:
                                prevyear = X[1]
                        else:
                            Average.append(int(Calc / Athletes))
                            prevyear =  X[1]
                            Athletes = 0
                            Calc = 0
                    Average.append(int(Calc / Athletes))
                    load = False # Disable loading screen        
                    clear()
                    for X in range(len(Average)):
                        print(Year1,'|'*(int(Average[X]*0.5)))
                        Year1 += 1
                input('Press enter to continue: ')

        # Quiz
        elif 'quiz' in Req or 'game' in Req:
            QName = []
            QYear = []
            QAns = []
            Correct = 0
            AthleteIDs = []
            clear()
            Anmount = int(input('Amount of questions: ')) # Anmount of questions
            load =  True
            for X in range(Anmount):
                while True:
                    Check = random.randint(1,135571)
                    if Check not in AthleteIDs:
                        AthleteIDs.append(Check) # Select random athletes
                        break

            for X in range(len(AthleteIDs)):
                with sqlite3.connect(DATABASE) as db:
                    cursor = db.cursor()
                    sql = (f"SELECT ID, Name, Age, Year FROM Athletics WHERE ID = {AthleteIDs[X]}; ")
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    # Add answers to answer sheets
                    for Z in results:
                        QName.append(Z[1])
                        QYear.append(Z[3])
                        QAns.append(Z[2])
            # The quiz
            load = False
            clear()
            for X in range(len(AthleteIDs)):
                print(f'How old was {QName[X]} in the year {QYear[X]}?')
                Rand = random.randint(-20, 20)
                print(f'If they were {QAns[X]+Rand} the year {QYear[X]+Rand}')
                # print(f'DEBUG ANS: {QAns[X]}') # Cheat
                while True:
                    msg = input('Answer: ')
                    
                    try:
                        msg = int(msg)
                    except:
                        print('Input is invalid\n')
                        input('press enter to continue')
                        break
                    if msg == QAns[X]:
                        print(f'\nCorrect. {QName[X]} is {QAns[X]} in {QYear[X]}\n')
                        Correct += 1
                        input('press enter to continue...')
                    elif QAns[X] == None:
                        print('The answer is unknown')
                        input('press enter to continue...')
                        Correct += 1
                    else:
                        print(f'\nIncorrect\n{QName[X]} was {QAns[X]}')
                        input('press enter to continue...')
                    clear()
                    break

            print(f'You got {Correct} out of {Anmount} answers correct')
            os._exit(os.EX_OK) # Exit script

        # Searching Database
        elif 'search' in Req or 'srch' in Req:
            clear()
            while True:
                Querys = ('age','name','height','games','sport','team')
                print('What to search?')
                print('Possible querys: Team(Country), Age, Name, Height, Games, Sport')
                Req =  input('Search: ')
                Req = Req.lower()
                if Req in Querys:
                    break
                else:
                    print('Search not possible')
                    input('Press enter to continue...')
                
            clear()
            print(f'What {Req} to search by?')
            print('Caps matter')
            Srch = input('Search: ')
            load = True
            with sqlite3.connect(DATABASE) as db:
                cursor = db.cursor()
                sql = (f'SELECT ID, Name, Year, Age, Height, Team FROM Athletics WHERE {Req} = "{Srch}" ORDER BY ID; ') # SQL Statement
                cursor.execute(sql) # Run statement
                results = cursor.fetchall() # Get output of statement
                load = False
                clear()
                print('ID, Country, Year, Age, Height, Name')
                for X in results:
                    print(X[0],X[5],X[2],X[3],X[4],X[1])
            print('ID, Country, Year, Age, Height, Name')
            input('press enter to continue...')

def func2(): # Loading screen
    global load
    global clear
    Time = 0
    while True:
        if int(Time) == 30: # time out error
            print('Error: Timed out') 
            os._exit(os.EX_OK)
        if load ==  True: # loading animations
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

# Start threads
if __name__ == "__main__":
    Thread(target = func1).start()
    Thread(target = func2).start()


