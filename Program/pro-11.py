### [11] Create table team(tid, country, totalmatch, win,loss). Insert 8 team detail.
### Create trigger to verify totalmatch is not 0. export data into csv file.
### Read file using reader object and print record with winning %age.

import sqlite3 as sq
import csv

#### Connect to the database

conn = sq.connect("D:/sqlite/dbms/cricket.db")
cur = conn.cursor()

### Create table "team"


cur.execute('''
    CREATE TABLE IF NOT EXISTS team (
        tid INTEGER PRIMARY KEY,
        country TEXT,
        totalmatch INTEGER,
        win INTEGER,
        loss INTEGER
    )
 ''')
conn.commit()

### Create trigger " check_totalmatch"


cur.execute('''
    CREATE TRIGGER IF NOT EXISTS check_totalmatch
    BEFORE INSERT ON team
    FOR EACH ROW
    BEGIN
        SELECT CASE
            WHEN NEW.totalmatch <= 0 THEN
                RAISE(ABORT, 'Total matches must be greater than 0')
        END;
    END;
''')
conn.commit()

### Insert data

team_data = [
    (1, 'India', 100, 60, 40),
    (2, 'Australia', 120, 70, 50),
    (3, 'England', 95, 50, 45),
    (4, 'Pakistan', 110, 55, 55),
    (5, 'South Africa', 90, 60, 30),
    (6, 'New Zealand', 85, 45, 40),
    (7, 'Sri Lanka', 95, 40, 55),
    (8, 'West Indies', 80, 30, 50)
]

### Execute the data

cur.executemany('INSERT INTO team (tid, country, totalmatch, win, loss) VALUES (?, ?, ?, ?, ?)', team_data)
conn.commit()

### Print data


cur.execute('SELECT * FROM team')
rows = cur.fetchall()
print(rows)

### Export data to a csv file


with open("D:\\sqlite\\csv\\python1.txt","w", newline='') as f:
    writer = csv.writer(f)
    #header
    writer.writerow(['tid', 'country', 'totalmatch', 'win', 'loss'])  
    writer.writerows(rows)

### Read Data from CSV and Calculate Win Percentage

with open("D:\\sqlite\\csv\\python1.txt","r") as f:
    reader = csv.DictReader(f)
    print(f"{'Country':<15} {'Total Matches':<15} {'Wins':<10} {'Losses':<10} {'Win %':<10}")
    print("="*60)
    
    for row in reader:
        total_matches = int(row['totalmatch'])
        wins = int(row['win'])
        win_percentage = (wins / total_matches) * 100
        print(f"{row['country']:<15} {total_matches:<15} {wins:<10} {row['loss']:<10} {win_percentage:.2f}%")

        
