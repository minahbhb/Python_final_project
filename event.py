import logging
import os
import csv
import user
import pandas as pd
import logging
###########################################
my_logger_event = logging.getLogger(__name__)
my_logger_event.setLevel(logging.DEBUG)
file_logging_handler = logging.FileHandler('even_log.log')
file_logging_handler.setLevel(logging.INFO)
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_logging_handler.setFormatter(log_format)
my_logger_event.addHandler(file_logging_handler)
#############################################


class Event:
    
    def __init__(self,name,date,time,place,total_capacity,price,left_capacity=None):
        """
        

        Parameters
        ----------
        name : TYPE str
            event name.
        date : TYPE str
            date of event.
        time : TYPE str
            time of event.
        place : TYPE str
            place of event.
        total_capacity : TYPE int
            the capacity of event.
        price : TYPE int
            the price of ticket for event.
        left_capacity : TYPE int, optional
            DESCRIPTION. The default is None
                         The left capacity for event.

        Returns
        -------
        None.

        """
        
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
        

        Parameters
        ----------
        file_event_csv : TYPE csv.file
            the file include the info for created event.

        Returns
        -------
        event : TYPE instance of Event class
            By takinf info of vent from admin return an event as an instance of Event class.

        """
      
        name=input('event_name: ')
        date=input('event_date: ') # you need to make the format for time and date the same for comparison    #2021,12,12
        time=input('event_time: ')          #20,00,00
        place=input('event_place: ') 
        total_capacity=int(input('event_total_capcity: ') )
        price=int(input('event_price: ') )
        left_capacity=int(input('event_left_capacity: '))
        
        try:
            if os.path.isfile(file_event_csv)==False:
                try:
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
                except :
                    print('file error')
                    my_logger_event.error('file event error', exc_info=True)
            else:
                try:
                    with open(file_event_csv,'a',newline='') as f:
                        writer = csv.writer(f, delimiter=',')
                        writer.writerow([name,date,time,place,total_capacity,price,left_capacity])
                except :
                    my_logger_event.error('file event error', exc_info=True)
                    print('file error')
        except:
            print('File error')
            my_logger_event.error('file event error', exc_info=True)
        event= Event(name,date,time,place,total_capacity,price,left_capacity)
        my_logger_event.info('creat an event and an object for Event class', exc_info=True)
        return event
    
    
    def creat_discount(file_discount_csv):
        """
        

        Parameters
        ----------
        file_discount_csv : TYPE csv.file
            by taking the info from admin return new discount category and save it in discount file.

        Returns
        -------
        None.

        """
        discount_gorup=input('please input the group of discount: ')
        percentage=int(input('please input the percentage of discount: '))
        try:
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
            my_logger_event.error('file discount error', exc_info=True)
        my_logger_event.info('new discount category added to file discount', exc_info=True)
    
    # edit discount function###########################
    def edit_discount(file_discount_csv):
        
        try:
            with open(file_discount_csv, 'r') as data_file:
                csv_data = csv.reader(data_file)
                list_index=[]
                for index,line in enumerate(csv_data):
                    print(f'id={index}',line)
                    list_index.append(index)
        except:
            print('file error')
            my_logger_event.error('file disount error', exc_info=True)
        else:
            try:
                id=int(input('which discount do you want to edit? enter its id '))
                percentage=int(input('what is the new percentage of discount:  '))
                assert (id in list_index)
            except AssertionError:
                print('invalid input')
                my_logger_event.error('invalid input error', exc_info=True)
            else:
                try:
                    df=pd.read_csv(file_discount_csv, sep=',',header=None)
                    df.at[id,1]=percentage
                    df.to_csv(file_discount_csv,index=False,header=False)
                except:
                    print('file error')
                    my_logger_event.error('file edisount error', exc_info=True)
        my_logger_event.info('discount edited', exc_info=True)
            
         
   
    def buy_ticket(costumer_kind,file_event_csv,file_discount_csv):
        """
        

        Parameters
        ----------
        costumer_kind : TYPE the attribute from instance of User class
            check if the costumer kind equall to kind in discount file to offer discount to costumer.
        file_event_csv : TYPE csv.fiel
            DESCRIPTION. display the list of event to costumer from event file
        file_discount_csv : TYPE csv.file
            DESCRIPTION. display the discount file to see whether the costumer kind equall to discount category to offer discount to costumer

        Returns
        -------
        None.

        """
        try:
            with open(file_event_csv, 'r') as data_file:
                csv_data = csv.reader(data_file)
                #next(csv_data)
                for index,line in enumerate(csv_data):
                    print(f'id={index}',line)
                try:
                    id=int(input(('which event do you want to buy? enter its id ')))
                    ticket=int(input('How many tickets do you need: '))
                    try:
                        # making an object from the selected event
                        df=pd.read_csv(file_event_csv, sep=',',header=None)
                        dt=df.values
                        a=dt[id]
                        event=Event(*a)
                    except:
                        print('file error')
                        my_logger_event.error('file event error', exc_info=True)
                    else:

                        try:
                            assert (ticket<int(event.left_capacity)) # you can add here checking time and date
                            try:
                                df.at[id,6]=df.loc[id][6]-ticket
                                df.to_csv(file_event_csv,index=False,header=False)
                        
                            except:
                               print('file error')
                               my_logger_event.error('file event error', exc_info=True)
                            else:
                                try:
                                    with open(file_discount_csv, 'r') as data_file:
                                        csv_data = csv.reader(data_file)
                                        list_discount=[]
                                        list_index=[]
                                        for index,line in enumerate(csv_data):
                                            print(f'id={index}',line)
                                            list_discount.append(line)
                                            list_index.append(index)
                                except :
                                    print('file error')
                                    my_logger_event.error('file disount error', exc_info=True)
                                
                                else:
                                    try:
                                        id_2=int(input('Can you use discount based on your account type? if yes press the correspondance index: '))
                                        assert (id_2 in list_index)
                                        try:
                                            #kind_costumer=user.Costumer.buyer.type_discount()
                                            assert(list_discount[id_2][0]==costumer_kind)
                                            price=int(event.price)-((int(event.price)*float(list_discount[id_2][1]))/100)
                                            total_price=price*ticket
                                            print('Your discount code is accepted\n')
                                            print(f'ecah ticket cost {event.price} and you need to pay {total_price} in total for {ticket} tickets')
                                        except:
                                            price=int(event.price)*ticket
                                            print('your discount type is not valid')
                                            print(f'you need to pay {price}')
                                    except :
                                        print('invalid input')
                                        my_logger_event.error('Assertion error. the selected index is not exist', exc_info=True)
                            
                        except AssertionError:
                            print(f'{event.left_capacity} tickets are left you can not buy more ticket than left capacity')
                            my_logger_event.error('Assertion error. the left capacity is less than numbers of ticket', exc_info=True)
                except:
                    print('invalid input')
                    my_logger_event.error('Assertion error. the selected index is not exist', exc_info=True)
                    
                #else:
                    
                
        except :
            print('file error')
            my_logger_event.error('file error', exc_info=True)
        my_logger_event.info('tickets are sold successfully', exc_info=True)
            
        return

    
        
    def display_event(file_event_csv):
        """
        

        Parameters
        ----------
        file_event_csv : TYPE csv.file
            DESCRIPTION. by calling event file display the previously defiend event

        Returns
        -------
        None.

        """
        try:
            with open(file_event_csv, 'r') as data_file:
                csv_data = csv.reader(data_file,delimiter='\t')
                #next(csv_data)
                for index,line in enumerate(csv_data):
                    print(f'id={index}',line)
        except :
            print('file error')
            my_logger_event.error('file event error', exc_info=True)
        my_logger_event.inf('evnt are displayed sucessfully', exc_info=True)
        
    
        

         
        
    


            
        
        
        
        
        
    

