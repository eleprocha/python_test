
from pathlib import Path
import re
import mysql.connector

x = Path('./python_texts')
files = list(filter(lambda y:y.is_file(), x.iterdir()))

dict = {str(i):{'The official name':0,
        'date webside registration':0,'website':0} for i in range(10)}
for k in range(10):
    try:
        with open(str(files[k]),'r',encoding='utf-8') as f:
            data = f.readlines()
            data = data[5:]
            

            data = [i.replace('Αθάνα','Αθήνα') for i in data ]
            data = [i.upper().replace('ΕΠΩΝΥΜΙΑ','ΕΠΩΝΥΜΊΑ').strip()
                    .replace('Αθάνα','Αθήνα')
                    .replace(':','')
                    .replace('«','')
                    .replace('»','')
                    .replace("Γ.Ε.ΜΗ.","ΓΕΜΗ") for i in data]
            
            
            #data = list(set(data))

        
        #επωνυμια
        for j,i in enumerate([re.search('επωνυμία'.upper(),str) for str in data]):
            if i is not None:
                d = data[j] + data[j+1] +data[j+2]
                d = d.split('AΡΙΘΜΌΣ')[0]
                dict[str(k)]['The official name']=d.split('επωνυμία'.upper())[1].split('και αριθμό'.upper())[0].replace(':','')
                dict[str(k)]['The official name'] = dict[str(k)]['The official name'].strip()
                dict[str(k)]['The official name'] = dict[str(k)]['The official name'].replace('\u03a2','').replace("Α..Κ.","A.K.")
                break
        #ΓΕΜΗ
        try:
            for j,i in enumerate([re.search('επωνυμία'.upper(),str) for str in data]):
                if i is not None:
                  d = data[j] + data[j+1] + data[j+2]
                  dict[str(k)]['The GEMH number'] = d.split('επωνυμία'.upper())[1].split('αριθμό'.upper())[1].replace('.','').split('ΓΕΜΗ')[1].replace('AΡΙΘΜΌΣ ΓΕΜΗ','')
                  dict[str(k)]['The GEMH number'] = dict[str(k)]['The GEMH number'].replace("\n","").strip()
                  break
        except:
            dict[str(k)]['The GEMH number'] = [str for str in data if re.search("AΡΙΘΜΌΣ ΓΕΜΗ",str) is not None][0].split("ΓΕΜΗ")[1].strip()
        #dict[str(k)]['The GEMH number'] = [str for str in data if re.search("AΡΙΘΜΌΣ ΓΕΜΗ",str) is not None][0].split("ΓΕΜΗ")[1].strip()
            
                
                
        #registration date
        for j,i in enumerate([re.search('ΑΘΉΝΑ',str) for str in data]):
            if i is not None:
                dict[str(k)]['date webside registration'] = data[j].split('ΑΘΉΝΑ')[1].replace(',','').strip()
                #print(dict)
                
        #website
        for j,i in enumerate([re.search('ΙΣΤΟΣΕΛΊΔΑΣ',str) for str in 
                              data]):
            if i is not None:
                d = data[j] + data[j+1]
                dict[str(k)]['website'] = d.split('ΙΣΤΟΣΕΛΊΔΑΣ')[1].strip().split()[0].lower()
                #dict['website'] = [str for str in dict['website'] if re.search('WWW',str) is not None][0].lower()
        if dict[str(k)]['website'] == 'εταιρείας':
            dict[str(k)]['website'] = [str for str in data if re.search("ΙΣΤΟΣΕΛΊΔΑ",str) is not None][1].split("ΙΣΤΟΣΕΛΊΔΑ")[1].lower()
            
    except:
        print(k)
        





#mydb = mysql.connector.connect(host = "localhost",user = "root", password = "montecarlo01")

#mycursor.execute("CREATE DATABASE mydatabase")

mydb = mysql.connector.connect(host = "localhost",user = "root", password = "montecarlo01", database = "mydatabase")

mycursor = mydb.cursor()

mycursor.execute("create table kataxoriseis ( id INT  PRIMARY KEY,name VARCHAR(255), date_website_registration VARCHAR(255), \
                 website VARCHAR(255), GEMH TEXT)")

    
mycursor.execute("ALTER TABLE `kataxoriseis` CONVERT TO CHARACTER SET 'utf8'")

sql = "INSERT INTO kataxoriseis VALUES (%s,%s,%s,%s,%s)"

for j in dict.keys():
    k = [int(j)]
    for i in ['The official name', 'date webside registration', 'website', 'The GEMH number']:
        k.append(dict[str(j)][i])
    val = tuple(k)
    print(val)
    mycursor.execute(sql,val) 

mydb.commit() 

     

mycursor.execute("SELECT * FROM kataxoriseis")
myresult = mycursor.fetchall()

