import  socket
import datetime
import sqlite3






conn = sqlite3.connect('sweeping25')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS student (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        batch INTEGER
                    )''')
conn.commit()
def getdate():
    curntdate = datetime.date.today()
    print(curntdate)
    if(curntdate.weekday() == 4):
        tomorow=curntdate + datetime.timedelta(days=3)
        return curntdate,tomorow
    elif(curntdate.weekday() == 5):
        tomorow=curntdate + datetime.timedelta(days=2)
        return curntdate,tomorow
    else:
        tomorow=curntdate + datetime.timedelta(days=1)
        return '2024-03-10',tomorow
def studentable():
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS student(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        batch INTEGER
                    )''')
    conn.commit()
def dateaviable(curntdate):
    cursor.execute("select count (*) from  swepingtbl where date = ? ",(curntdate,))
    count=cursor.fetchone()[0]
    return count>0
def getstunamebydate(date):
   
    cursor.execute("SELECT name FROM swepingtbl where date = ? ",(date,))

    upname=cursor.fetchone()
    conn.commit()
    return upname
def getlastdate():
    c,t=getdate()
    cursor.execute("SELECT id, date FROM swepingtbl WHERE date = (SELECT MAX(date) FROM swepingtbl)")
    id1 = cursor.fetchone()[0]
    dt = cursor.fetchone()[1]

    if(dt==c):
        print('today is lasted so we haave to up date that')
        print(dt,c)
        nm=getstuname(id1+1)
        cursor.execute('INSERT INTO swepingtbl (id,date,name) values (?,?,?)',(id1,t,nm))

        

def updatesweeping():
    c ,t =getdate()
    print(t)
    if not dateaviable(c):
       nowtoday = "today no student avilabel"
         
    else:    
        nowtoday=getstunamebydate(c)
        print(nowtoday)
    nxtdate=dateaviable(t)
    return nowtoday,nxtdate

    
    
    
def getstuname(ncount):
    cursor.execute("SELECT name FROM student where id = ? ",(ncount,))
    upname=cursor.fetchone()[0]
    conn.commit()
    return upname

def swepupdate():
   
    cursor.execute("SELECT COUNT(*) FROM swepingtbl")
    count=cursor.fetchone()[0]
    print(count)
    ncount=count+1
    getstuname(ncount)
    
    
    print(count+1)

    conn.commit()
def tablexist(date1):
   
    cursor.execute('''CREATE TABLE IF NOT EXISTS swepingtbl (
                        id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        date DATE
                    )''')
    cursor.execute("SELECT * FROM swepingtbl WHERE date = ? ", (date1,))
    if(cursor.fetchone()):
        stuname=cursor.fetchone()
    else:
        stuname="no student yet"
    conn.commit()
    return stuname
def sokt(data,address):
    fk.sendto(data.encode(),address)
print('Welcome to ict sweepinG')
print('db created sucess fully')
fk=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

print('socket sucesss fulllly created')
print('mm')
print(getdate())
cdate,tdate=getdate()
#cdate="2024-03-10"
print(cdate)
# tablexist(cdate)
# print(tdate)
# print(getdate())
# print(updatesweeping())
# swepupdate()
# print(cdate.strftime('%Y-%m-%d'))
print(tdate.strftime('%Y-%m-%d'))

try:
    fk.bind(('192.168.1.23',8001))
    fk.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    print(f'sucessfully with localhost and {8001}')
    
    # fk.listen(3)

    print('fk listening')
    data, address = fk.recvfrom(1024)
    print(f"Received data from {address}: {data.decode()}")

    while True:
        # skt, add = fk.accept()
        # print(f'connected with {add}')
        # print(f"Received data from {address}: {data.decode()}")
        # fk.sendto(data, address)
        # print("Echoed data back to the sender")
        # fk.sendto(b'welcome knkcc',)
        name=tablexist(cdate)
        # updatesweeping()
        swepupdate()
        today,nextdate=updatesweeping()
        tname = getstunamebydate(nextdate)

        if isinstance(today,tuple):
            cname = getstunamebydate(nextdate)
            data=f"{today} for {cname}"
            fk.sendto(data.encode(), address)
        else:
            data=f"{today}"
            fk.sendto(data.encode(), address)
        sokt(data,address)
        nxname=getstunamebydate(tdate.strftime('%Y-%m-%d'))
        nxdata=f"{tdate.strftime('%Y-%m-%d')} for {nxname}"
        sokt(nxdata,address)
        # print('data send ')
except socket.error as e:
    print(e)
