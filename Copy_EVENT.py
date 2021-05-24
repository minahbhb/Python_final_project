import datetime
import time
import logging
import os
import csv
import user
import pandas as pd

# my_logger_1 = logging.getLogger('Admin_logger')
# my_logger_1.setLevel(logging.DEBUG)

# my_logger_2 = logging.getLogger('Event_logger')
# my_logger_2.setLevel(logging.DEBUG)

# my_logger_3 = logging.getLogger('Costumer_logger')
# my_logger_3.setLevel(logging.DEBUG)

# file_Admin_handler = logging.FileHandler('Admin_log.log')
# file_Event_handler = logging.FileHandler('Event_log.log')
# file_Costumer_handler = logging.FileHandler('Costumer_log.log')

# file_Admin_handler.setLevel(logging.INFO)
# file_Event_handler.setLevel(logging.INFO)
# file_Costumer_handler.setLevel(logging.INFO)

# std_handler = logging.StreamHandler()
# std_handler.setLevel(logging.ERROR)

# log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# file_Admin_handler.setFormatter(log_format)
# file_Event_handler.setFormatter(log_format)
# file_Costumer_handler.setFormatter(log_format)
# std_handler.setFormatter(log_format)

# my_logger_1.addHandler(file_Admin_handler)
# my_logger_2.addHandler(file_Event_handler)
# my_logger_3.addHandler(file_Costumer_handler)
# my_logger.addHandler(std_handler)

# my_logger.handlers

class Event:
    
    def __init__(self,name,date,time,place,total_capacity,price,left_capacity=None):
        
        self.name=name
        self.date=date #2021,12,12
        self.time=time #20,00,00
        self.place=place
        self.total_capacity=total_capacity
        self.price=price
        self.left_capacity=left_capacity
        

    @staticmethod
    def creat_event(file_event_csv):
        """
        with this function only Admin can create new event by getting input from Admin and call class Event
        also the reslut will be saved in the csv file

        Returns
        None

        """
        name=input('event_name: ')
        date=input('event_date: ') # you need to make the format for time and date the same for comparison    #2021,12,12
        time=input('event_time: ')          #20,00,00
        place=input('event_place: ') 
        total_capacity=int(input('event_total_capcity: ') )
        price=int(input('event_price: ') )
        left_capacity=int(input('event_left_capacity: '))
        
        try:
            #if os.stat(file_event_csv).st_size == 0:
            if os.path.isfile(file_event_csv)==False:
                with open(file_event_csv,'a',newline='') as f:
                    fieldnames=['name', 'date', 'time', 'place','total_capacity','price','left_capacity']
                    csv_file = csv.DictWriter(f,fieldnames=fieldnames, delimiter=',')
                    csv_file.writeheader()
                    csv_file.writerow({
                            'name': name,
                            'date':date,
                            'time':time,
                            'place':place,
                            'total_capacity':total_capacity,
                            'price':price,
                            'left_capacity':left_capacity})
            else:
                with open(file_event_csv,'a',newline='') as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow([name,date,time,place,total_capacity,price,left_capacity])
        except:
            print('File error')
        event= Event(name,date,time,place,total_capacity,price,left_capacity)
        return event
    
    
    def creat_discount(file_discount_csv):
        discount_gorup=input('please input the group of discount: ')
        percentage=int(input('please input the percentage of discount: '))
        try:
            #if os.stat(file_discount_csv).st_size == 0:
            if os.path.isfile(file_discount_csv)==False:
                with open(file_discount_csv,'a',newline='') as f:
                    fieldnames=['discount_gorup', 'percentage']
                    csv_file = csv.DictWriter(f,fieldnames=fieldnames)
                    csv_file.writeheader()
                    csv_file.writerow({
                            'discount_gorup': discount_gorup,
                            'percentage':percentage})
            else:
                with open(file_discount_csv,'a',newline='') as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow([discount_gorup, percentage])
        except:
            print('File error')
    
    # edit discount function###########################
    def edit_discount(file_discount_csv):
        
        try:
            with open(file_discount_csv, 'r') as data_file:
                csv_data = csv.reader(data_file,delimiter='\t')
                
                for index,line in enumerate(csv_data):
                    print(f'id={index}',line)
        except:
            print('file error')
        else:
            try:
                id=int(input('which discount do you want to edit? enter its id '))
                percentage=int(input('what is the new percentage of discount:  '))
            except:
                print('invalid input')
            else:
                try:
                    with open(file_discount_csv, 'r') as data_file:
                        csv_data = csv.DictReader(data_file,delimiter=',')
                        for index,line in enumerate(csv_data):
                            if index==id:
                                line['percentage']=percentage
                                with open(file_discount_csv, 'w') as f:
                                    csv_writer=csv.writer(f,delimiter=',')
                                    for line in csv_data:
                                        csv_writer.writerow(line)
                except:
                    print('file error')
                   
         
   
    def buy_ticket(buyer,file_event_csv,file_discount_csv):
        try:
            with open('file_event_csv', 'r') as data_file:
                csv_data = csv.reader(data_file)
                #next(csv_data)
                for index,line in enumerate(csv_data):
                    print(f'id={index}',line)
                try:
                    id=int(input(('which event do you want to buy? enter its id ')))
                    ticket=int(input('How many tickets do you need: '))
                    try:
                        df=pd.read_csv('file_event_csv', sep=',',header=None)
                        dt=df.values
                        a=dt[id]
                        event=Event(*a)
                    except:
                        print('file error')
                    
                    try:
                        assert (ticket<int(event.left_capacity)) # you can add here checking time and date
                    except AssertionError:
                        print(f'{event.left_capacity} tickets are left you can not buy more ticket than left capacity')
                except:
                    print('invalid input')
                    
                else:
                    try:
                        with open('file_event_csv', 'r') as data_file:
                            #csv_data = csv.DictReader(data_file,delimiter=',')
                            csv_data =csv.reader(data_file,delimiter=',')
                            for index,line in enumerate(csv_data):
                                #print(index,line)
                                if index==id:
                                    print(line)
                                    line[6]=int(line[6])-ticket
                                    # event.left_capacity=event.left_capacity-ticket
                                    
                            with open('file_event_csv', 'w') as f:
                                csv_writer=csv.writer(f,delimiter=',')
                                for line in csv_data:
                                    csv_writer.writerow(line)
                    except:
                        print('file error')
                    else:
                        try:
                            with open('file_discount_csv', 'r') as data_file:
                                csv_data = csv.reader(data_file)
                                list_discount=[]
                                for index,line in enumerate(csv_data):
                                    print(f'id={index}',line)
                                    list_discount.append(line)
                        except :
                            print('file error')
                                
                        else:
                            try:
                                id=int(input('Can you use discount based on your account type? if yes press the correspondance index: '))
                                try:
                                    kind_costumer=user.Costumer.buyer.type_discount()
                                    assert(list_discount[id][0]==kind_costumer)
                                    event.price=int(event.price)-((int(event.price)*int(list_discount[id][1]))/100)
                                    total_price=event.price*ticket
                                    print(f'ecah ticket cost {event.price} and you need to pay {total_price} in total')
                                except:
                                    print('your discount type is not valid')
                            except :
                                print('invalid input')
                
        except :
            print('file error')
        return

    
        
    def display_event(file_event_csv):
        try:
            with open(file_event_csv, 'r') as data_file:
                csv_data = csv.reader(data_file,delimiter='\t')
                #next(csv_data)
                for index,line in enumerate(csv_data):
                    print(f'id={index}',line)
        except :
            print('file error')
        
    
        

         
        
    


            
        
        
