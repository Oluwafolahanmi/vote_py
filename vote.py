import mysql.connector as connection
import random
import string
import time
from collections import Counter
adminid = 123456
password = "password"
mydb = connection.connect(host="127.0.0.1", user = "root", password = "Ademola.12", database = "mydatabase")
mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE studentv(Sn INT PRIMARY KEY AUTO_INCREMENT, fname CHAR(55), lname CHAR(30), gender CHAR(10), phoneNum VARCHAR(11), department CHAR(50), password VARCHAR(20), voter_id VARCHAR(20), vote INT, president VARCHAR(30), vp VARCHAR(30), gen_sec VARCHAR(30), fin_sec VARCHAR(30), treasurer VARCHAR(30))")
# mycursor.execute("CREATE TABLE votes(president INT, vp INT, TreasurerINT, gen_sec INT, fin_sec INT, total_votes)")
# mycursor.execute("DROP TABLE studentv")
def reg():
    b = ""; 
    for i in range(4):
        k = (random.choice(string.ascii_letters)).upper(); b+=k
    print("\nRegister for this program")
    details, voterId, detail, det = ["First name: ", "Last name: ", "Gender: ", "Phone number: ", "department: ", "Password: ", "Confirm password: "], (str(random.randint(1234567898765432, 3000000000000000))+b), [], [0, 0, 0, 0, 0, 0]
    for i in details:
      if i == "department: ":
          print("department: "); dept = ["Frontend eng (FE)", "Backend eng (BE)", "UI/UX", "Data analysis (DA)", "Data science (DS)", "Project mgt (PM)", "Graphics design (GD)"]; ab = 0
          for i in dept:
              print(str(ab+1)+". "+i); ab+=1
          decision = int(input(">>>>> ")); k = dept[decision-1]; detail.append(k)
      else:     
          k = input(i); detail.append(k)
    while True:
        if detail[5] != detail[6]:
            print("password does not match"); b = input("confirm password: "); detail[6] = b
        else:
            break
    print("congratulations", detail[0], detail[1], "You have successfully registered for this program. Your voter Id is", voterId)
    detail[6] = voterId; detail.extend(det); detail = tuple(detail)
    querry = "INSERT INTO studentv (fname, lname, gender, phoneNum, department, password,  voter_id, vote, president, vp, gen_sec, fin_sec, treasurer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(querry, detail); mydb.commit(); login()
def login():
    print("\nLOGIN"); print("\nwelcome to login"); global Id; Id  = input("Voter Id: "); fetch()
    if details != None:
        password = input("password: ")
        if password == details[6]:
            print("welcome", details[1], details[2])
            homepage()
        else:
            print("invalid id. try again")
            login()
    else:
        print("User details not found"); start()
def start():
    print("VOTING PLATFORM"); decision = input("\n1. REGISTER       2. LOGIN    \n>>>>> ")
    if decision == "1":
        reg()
    else:
        login()
def fetch():
    sq = "SELECT * FROM studentv WHERE voter_id = %s"; mycursor.execute(sq, (Id,)); global details; details = mycursor.fetchone(); return details    
def homepage():
    decision = input("\n1. VOTE      2. CHECK RESULT\n >>>> ")
    if decision == "1":
        vote()
    else:
        checkresult()
def vote():
    fetch(); print("Cast your vote"); time.sleep(2)
    if details[8] < 1:
        count = 0; posts = ["\nPRESIDENT", "\nVICE PRESISENT", "\nTREASURER", "\nFINANCIAL SECRETARY", "\nGENERAL SECRETARY"]; post = ["president", "vp", "treasurer", "fin_sec", "gen_sec"]
        contestants = [["Niyi Osundare (UI/UX)", "Wole Soyinka (PM)", "Chinua Achebe (FE)", "Chimamanda Adichie (DS)"], ["Yinka Adebajo (DA)", "Jeremy Johnson (PM)", "Tayo Oviosu (GD)",
                     "Shola Akinlade (BE)"], ["Gbenga Agboola (DA)", "Bankole Oluwafemi (BE)", "Adewale Yussuf (FE)", "Gbenga Sesan (GD)"], ["Omobola Johnson (DS)", "Seun Onigbinde (FE)", 
                    "Iyin Aboyeji (UI/UX)", "Kola Aina (PM)"], ["Kunmi Demuren (DS)", "Bosun Tijani (GD)", "Femi Longe (BE)", "Mark Esien (PM)"]]
        
        for i in posts:
            index = posts.index(i); print(posts[index])
            for con in contestants[index]:
                get = contestants[index].index(con); print(get + 1, end=". ");  print(contestants[index][get])
            response = int(input(">>>> "))
            sql = f"UPDATE studentv SET {post[index]} = %s WHERE voter_id = %s";  voters = (contestants[index][response-1], Id); mycursor.execute(sql, voters); mydb.commit()
        count +=1; sql = "UPDATE studentv SET vote = %s WHERE voter_id = %s"; mycursor.execute(sql, (count, Id)); mydb.commit()
        time.sleep(2); print("Voting complete. check result"); checkresult()
    else:
        print("You have voted. \nResult loading..."); time.sleep(2); checkresult()
def checkresult():
    decision = input("\n1. BY DEPARTMENT          2. TOTAL     \n>>>>"); dept = ["Frontend eng (FE)", "Backend eng (BE)", "UI/UX", "Data analysis (DA)", "Data science (DS)", "Project mgt (PM)", "Graphics design (GD)"]
    if decision == "1":
        for i in dept:
            k = dept.index(i); print(k+1, end=". "); print(i)
        ans = int(input(">>>> "))
        sql = "select * from studentv where department = %s"
        mycursor.execute(sql, (dept[ans-1], ))
        set_info = mycursor.fetchall()
        relist = list(zip(*set_info))
        total_voter = sum(relist[8]); print(f"Total votes = {total_voter}")
        posts = ["\nPRESIDENT", "\nVICE PRESISENT", "\nTREASURER", "\nFINANCIAL SECRETARY", "\nGENERAL SECRETARY"]
        for j in range(5):
          frequency = {}; print(posts[j])
          for item in relist[9+j]:
              if item in relist[9+j]:
                  frequency[item] = frequency.get(item, 0) + 1
          for key, value in frequency.items():
              print(f"{key} = {value} votes")
          count = Counter(relist[9+j]); winner = count.most_common(1)[0][0]
          print(f"The winner is {winner}")
        time.sleep(2); start()
    else:
        sql = "select * from studentv"
        mycursor.execute(sql)
        set_info = mycursor.fetchall()
        relist = list(zip(*set_info))
        total_voter = sum(relist[8]); print(f"Total votes = {total_voter}")
        posts = ["\nPRESIDENT", "\nVICE PRESISENT", "\nTREASURER", "\nFINANCIAL SECRETARY", "\nGENERAL SECRETARY"]
        for j in range(5):
          frequency = {}; print(posts[j])
          for item in relist[9+j]:
              if item == "0":
                  continue
              elif item in relist[9+j]:
                  frequency[item] = frequency.get(item, 0) + 1
          for key, value in frequency.items():
              print(f"{key} = {value} votes")
          count = Counter(relist[9+j]); winner = count.most_common(1)[0][0]
          print(f"The winner is {winner}")
        time.sleep(2); start(); 


        
       
start()
# reg()