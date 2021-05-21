import json
import hashlib
from getpass import getpass
import sys
import os
import base64
import os
import csv

class User:
    
    def __init__(self,name,username,family,email,phone,kind=None):
        self.name = name
        self.username=username
        self.email=email
        self.family=family
        self.phone=phone
        self.kind=kind
        
        
    def get_info():
        """
            this function get info from input for every user 
        """

        name,username,family,email,phone,kind= input("*Enter* name, username, family, email, phone, kind: \n").split(',')
        try:
            #if os.stat('user_info.csv').st_size == 0:
            with open('user_info.csv', 'a',newline='') as new_file:
                fieldnames=['name','username','family','email','phone','kind']
                csv_file = csv.DictWriter(new_file,fieldnames=fieldnames)
                csv_file.writeheader()
                csv_file.writerow({
                    'name': name,
                    'username':username,
                    'family':family,
                    'email':email,
                    'phone':phone,
                    'kind':kind})
                
        except:
            print('File error')
        user = User(name,username,family,email,phone,kind)
        return user #########################3

        
    def sign_in(self,file_signin):
        """
        This function wants to check user and passw for log in
        Parameters
        ----------
        file : *.json
            DESCRIPTION: we have one saved json file with the username and pass all user you need
            to give this as a input to sign_in function to check user info

        Returns
        -------
        None.

        """
        
        user=input( 'please enter you username: \n')
        passwd=input('please enter you password: \n') 
        
        try:
            with open('signin') as f:    
                new = json.load(f)
        except:
            print('file error') 
            
        else:
            ls_user=[]
            for i in range(len(new['Users'])):
                ls_user.append(new['Users'][i]['username'])
                if ((new['Users'][i]['username'])==self.username):
                    j=i
            try:
                assert (user in ls_user)and(user==self.username)
                #if (user in ls_user)and(user==self.username):
                key_decoded=base64.b64decode(new['Users'][j]['key'])  
                salt_decod=base64.b64decode(new['Users'][j]['salt']) 
                key =  new['Users'][j]['key']
                new_key = hashlib.pbkdf2_hmac('sha256', passwd.encode('utf-8'), salt_decod, 100000)
                try:
                    assert (key_decoded == new_key)
                    print(f'welcome {self.name} {self.family}')
                except:
                    print ("Sorry, the password is not correct")               
            except AssertionError:
                print ("Sorry, the username is not correct")
                    

    
    def change_passwd(self,file_signin):
        """
        This function wants to check user and passw for log in
        Parameters
        ----------
        json_file : *.json
            DESCRIPTION: we have one saved json file with the username and pass all user you need
            to give this as a input to sign_in function to check user info

        Returns
      
        """
        user=input( 'please enter you username: \n')
        passwd=input('please enter you password: \n') 
        
        try:
            with open('signin') as f:    
                new = json.load(f)
        except:
            print('file error') 
            
        
        else:
            ls_user=[]
            for i in range(len(new['Users'])):
                ls_user.append(new['Users'][i]['username'])
                if ((new['Users'][i]['username'])==self.username):
                    j=i
            try:
                assert (user in ls_user)and(user==self.username)
                key_decoded=base64.b64decode(new['Users'][j]['key'])  
                salt_decod=base64.b64decode(new['Users'][j]['salt']) 
                key =  new['Users'][j]['key']
                new_key = hashlib.pbkdf2_hmac('sha256', passwd.encode('utf-8'), salt_decod, 100000)
                try:
                    assert (key_decoded == new_key)
                    print(f'welcome {self.name} {self.family}, you can change your password now')
                    new_passwd= passwd=input('please enter your new password: \n')
                    update_key = hashlib.pbkdf2_hmac('sha256', new_passwd.encode('utf-8'), salt_decod, 100000)
                    update_key_encoded = base64.b64encode(update_key)  # b'ZGF0YSB0byBiZSBlbmNvZGVk' (notice the "b")
        
                    try:
                        with open(file_signin,'r') as f: #here I want to edit password
                            json_reader=json.load(f)
                            json_reader['Users'][j]=users={'username':user,'salt': new['Users'][j]['salt'],'key': update_key_encoded.decode('ascii')}
                            with open(file_signin,'w') as f1:
                                json.dump(json_reader,f1,indent=4)
                                
                                
                    except :
                        print('file error')   
                except AssertionError:
                    print ("Sorry, the password is not correct") 
            except AssertionError:
                    print ("Sorry, the username is not correct")
                            
                  
    def sign_up(self,file,file_signin):
            """
            This function is for adding new user. get user and password and add it to jason file
       
            Parameters
            ----------
            file_json : TYPE
                DESCRIPTION.

            Returns
            -------
            None.
            """
            #Add a user
            users={}
            username=self.username
            # unique username
            try:
                with open(file_signin,'r') as f1:
                    data=json.load(f1)
                    ls_user=[]
                    for i in range(len(data['Users'])):
                        ls_user.append(data['Users'][i]['username'])
                        
                    while username in ls_user:
                    
                        print(f'your selected username {username} is already taken you need to choose another username')
                        username=input('please enter new username: ')
            except: 
                print('file error')
                print('You can continue')
                
            passwd=input('please enter you password: ')
            #self.username=username
            salt = os.urandom(32) # A new salt for this user
            key = hashlib.pbkdf2_hmac('sha256', passwd.encode('utf-8'), salt, 100000)
            salt_encoded = base64.b64encode(salt)  # b'ZGF0YSB0byBiZSBlbmNvZGVk' (notice the "b")
            key_encoded = base64.b64encode(key)  # b'ZGF0YSB0byBiZSBlbmNvZGVk' (notice the "b")
            # users['Users']=[]
            #users['Users'].append({'username':username,'salt': salt_encoded.decode('ascii'),'key': key_encoded.decode('ascii')})
            users={'username':self.username,'salt': salt_encoded.decode('ascii'),'key': key_encoded.decode('ascii')}
            # with open(file,'a') as f:
            #     jason.dump(users)
            with open(file,'a') as f0:
                 json.dump(users,f0,indent=4)
                 
            with open(file,'r')as f2:
                new=json.load(f2)
                try:
                    with open(file_signin,'r') as f1:
                        data=json.load(f1)
                        data['Users'].append(new)
                        with open(file_signin,'w') as f5:
                            json.dump(data,f5,indent=4)
                except:
                    print(f'the {file_signin} is not exist')
                    data={}
                    data['Users']=[]
                    data['Users'].append(new)
                    with open(file_signin,'a') as f1:
                        json.dump(data,f1,indent=4)
            return 
                        
      
            
    def __str__(self):
        return f'Welcome {self.name} {self.family}'
    
        
class Admin(User):
    def __init__(self,name,username,family,email,phone,kind='Admin'):
        super().__init__(self,name,username,family,email,phone,kind)
        

    

class Costumer(User):
   def __init__(self,name,username,family,email,phone,kind):
        super().__init__(self,name,username,family,email,phone,kind)

        
   def type_discount(self):
        self.kind=input('what is your job you can get discount based on your job: student, worker, teenager,scienctist: ')
        return self.kind
        

# #################
# Mina=User('mina','hab','email','12')
# Mina.sign_up('signup','signin')

# Ali=User('ali','ss','ss','ss')
# Ali.sign_up('signup','signin')

Ali_2=User('ali','hasani','44','44')
Ali_2.sign_up('signup','signin')

