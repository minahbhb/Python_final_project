import json
import event
import user
import os
import csv
from user import Admin
from user import Costumer
import logging
###########################################
my_logger_main = logging.getLogger(__name__)
my_logger_main.setLevel(logging.DEBUG)
file_logging_handler = logging.FileHandler('main_log.log')
file_logging_handler.setLevel(logging.INFO)
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_logging_handler.setFormatter(log_format)
my_logger_main.addHandler(file_logging_handler)
####################################################################

def check_passwd(file_signin,file_signup,user_info):
    """
    

    Parameters
    ----------
    file_signin : TYPE csv.file
        DESCRIPTION. get sing_in file as an input to check username and passwd for each user
    file_signup : TYPE csv.file
        DESCRIPTION. get user info to sign up in system
    user_info : TYPE csv.file
        DESCRIPTION. check inof for each user from csv file

    Returns
    -------
    list
        DESCRIPTION. return type of user and an instnace of that user from class User [user type, instance of User class]

    """
    num=int(input('Please enter\n 1.Admin\n 2.Costumer\n 3. New_Costumer\n 4.New Admin\n  '))
    try:
        assert (num==1 or num==2 or num==3 or num==4)
        
        if num==1:
            try:
                load_user = user.Admin.check_info(user_info)
                load_user.sign_in(file_signin)
                return ['Admin',load_user]
            except:
                print('Incorrect Input')
                my_logger_main.error('sign_in or checkinfo error', exc_info=True)
                return [False,False]
            
        elif num==2:
            try:
              load_user=user.Costumer.check_info(user_info)
              load_user.sign_in(file_signin)
              return ['Costumer',load_user]
            except:
              print('Incorrect Input')
              my_logger_main.error('sign_in or checkinfo error', exc_info=True)
              return [False,False]
              
            
        elif num==3:
            try:
                new_costumer=user.Costumer.get_info(user_info,file_signin)
                new_costumer.sign_up(file_signup,file_signin)
                os.remove(file_signup)
                return ['Costumer',new_costumer]
            except:
              print('Incorrect Input')
              my_logger_main.error('sign_up or getinfo error', exc_info=True)
              return [False,False]
        
        elif num==4:
            try:
                new_Admin=user.Admin.get_info(user_info,file_signin)
                new_Admin.sign_up(file_signup,file_signin)
                os.remove(file_signup)
                return ['Admin',new_Admin]   
            except:
              print('Incorrect Input')
              my_logger_main.error('sign_up or getinfo error', exc_info=True)
              return [False,False]
 
        
    except AssertionError:
        print('invalid input')
        my_logger_main.error('asssertion error, wrong input', exc_info=True)
        return [False,False]  
        
        
#####################################
# check user and pass for three times
count=0
b=[False,False]
while (count<3) and b[0]==False:
    print('Hello! Welcome to Event system\n')
    b=check_passwd('signin','signup','user_info')
    #b=input('b:')
    count+=1
    
######################


Value=True
while Value:
    if count==3:
        print('You had three failed attemp\n')
        print('Sorry you need to try log in after 60 minutes')
        my_logger_main.error('wrong username or paswwd more than three times error', exc_info=True)
        Value=False
    #timer
    else:
        if b[0]=='Admin':
            try:
                num=int(input('what do you want to do: \n 1. Creat New Event\n 2. See previous defiend event\n 3. change password\n 4.edit discount \n 5.create new discount \n 6.Exit\n'))
                if num==1:
                    event.Event.creat_event('file_event_csv')
                    my_logger_main.info('creat event by admin', exc_info=True)
                ############################    
                elif num==2:
                    event.Event.display_event('file_event_csv')
                    my_logger_main.info('display event for admin', exc_info=True)
                    
                elif num==3:
                    b[1].change_passwd('signin')
                    my_logger_main.info('change password for admin', exc_info=True)
                    
                elif num==4:
                    event.Event.edit_discount('file_discount_csv')
                    my_logger_main.info('edit disount by admin', exc_info=True)
                
                elif num==5:
                    event.Event.creat_discount('file_discount_csv')
                    my_logger_main.info('creat discount by admin', exc_info=True)
                    
                elif num==6:
                    my_logger_main.info('admin exit', exc_info=True)
                    Value=False
                    break
            except :
                print('wrong input')
                my_logger_main.error('assertion error, wrong input by admin', exc_info=True)
                    
        elif b[0]=='Costumer':
            try:
                num=int(input('what do you want to do: \n 1. See current Event\n 2. Buy ticket\n 3. Exit\n '))
                if num==1:
                    event.Event.display_event('file_event_csv')
                    my_logger_main.info('display event for costumer', exc_info=True)
                    
                elif num==2:
                    costumer_kind=b[1].type_discount()
                    event.Event.buy_ticket(costumer_kind,'file_event_csv','file_discount_csv')
                    my_logger_main.info('but ticket by costumer', exc_info=True)
                
                elif num==3:
                    my_logger_main.info('costumer exit', exc_info=True)
                    Value=False
                    break
                
            except :
                print('Wrong input')
                my_logger_main.error('assertion error by costumer, wrong input', exc_info=True)
                 

    
        