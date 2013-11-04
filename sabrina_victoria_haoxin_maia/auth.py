from pymongo import MongoClient
client = MongoClient()
users = client.db.users

def clear():
    users.remove()

def authenticate(username,pw):
    return users.find({"username":username,"pw":pw},field={"_id":False}).count() != 0

def changepw(username,pw):
    users.update({'username':username},{"$set":{'pw':pw}},upsert=False)

def register(fname,lname,username,pw,pw2):
    if users.find({"username":username}).count() != 0:
        return 1
    elif pw != pw2:
        return 2
    elif users.find().count() == 0:
        users.insert({"username":username,"pw":pw,'fname':fname,'lname':lname,"ADMIN":True})
    else:
        users.insert({"username":username,"pw":pw,'fname':fname,'lname':lname,"ADMIN":False})
    return 0

def admin(username):
    return users.find({"username":username,"ADMIN":True}).count() != 0

def getName(username):
    name = []
    l = [x for x in users.find({"username":username},fields={'_id':False,'username':False,'pw':False,'ADMIN':False})][0]
    name.append(l['fname'])
    name.append(l['lname'])
    return name
    
if __name__ == "__main__":
    register('kevin','lin','kevinlin','asd','asd')
    register('brian','liu','brianliu','zxc','zxc')
    register('jason','chen','jasonchen','qwe','qwe')

    if authenticate('kevinlin','asd'):
        print("kevinlin passed \n")
    if not authenticate('kevinlin','qwe'):
        print('kevinlin did not pass \n')

    changepw('kevinlin','qwe')
    if authenticate('kevinlin','qwe'):
        print('kevinlin"s pw is now qwe \n')

    if admin('kevinlin'):
        print('kevinlin is the admin \n')
    if not admin('brianliu'):
        print('brianliu is not the admin \n')
        
    name = getName('jasonchen')
    print("first name: %s \n" %(name[0]))
    print("last name: %s \n" %(name[1]))

        

