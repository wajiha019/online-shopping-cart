from abc import ABC,abstractmethod
import sys
import datetime

class FileSaver:
    
    '''A Mix-in Class which saves the given list into a file'''
    
    def savetoFile(self,anylist,filename):
        
        ''' saves list to the file'''
        
        f=open(filename,'a')
        for item in anylist:
           f.write(str(item)+'\n')
        f.close()

class Product:

    '''Displays product list and arrange searching
      for productID's for details and shopping cart'''
    
    def __init__(self):
        self.quantity=0
           
    def displayProducts(self):
        
        '''Displays Product list'''
        
        print('\n\n\t\t====================================================')
        print('\t\t\tMULTI\t PURPOSE\t IOT\t DEVICES')
        print('\t\t====================================================\n')
        self.loadfromFile('Products.txt')
        
    def loadfromFile(self,fileName):

        '''Load products from File'''
        
        f=open(fileName,'r')
        f.seek(0)
        print('\n\t*************************************************************************************************************')
        print(f'\t\'PRODUCT ID\'\t\t\'PRODUCT NAME\'\t\t           \t\'PRICE IN RS.\'    ')
        print('\t*************************************************************************************************************')
        print()
        for line in f:
            line=eval(line.strip())
            print(f'\t{line[0]} \t\t\t{line[1]:10}\t\t{line[3]:10} ')
            print()
        f.close()
        print('\t*************************************************************************************************************')

    def getProductID(self):

        '''Search ProductID to add the product in the cart'''
        
        while True:
            product_id=input('\n\nEnter ID of Product which you want to add to cart:')
            f=open('Products.txt','a+')
            f.seek(0)
            for line in f:
                line=eval(line.strip())
                if product_id == line[0]:
                    pdname=line[1].upper()
                    self.quantity=int(input(f'\nEnter how much you want to buy:'))
                    print('\n\n================================================')
                    print(f'     {pdname}  HAS  BEEN   ADDED  TO  YOUR  CART')
                    print('================================================\n')
                    ShoppingCart.cartlist.append([line[0],line[1],line[3],self.quantity])
                    break
            buy=input('\nDo You Want To Buy More Products? Press \'y\' or \'n\'..')
            if buy=='n' or buy=='N':
                break


    def getProductDescription(self):

        '''Displays Product Discription'''
        
        while True:
            pd=input('\n\nEnter ID of Product which you want to see details:')
            f=open('Products.txt','a+')
            f.seek(0)
            for line in f:
                line=eval(line.strip())
                if pd == line[0]:
                    print('\n\nPRODUCT NAME:',line[1],'\nDETAILS:',line[2],'\n')
                    break
            details=input('\nDo you want to see more products details?Press\'y\' or \'n\'...')
            if details=='n' or details =='N':
                break

class ShoppingCart(FileSaver):

    ''' A class that manages all the functions of the cart'''

    cartlist=[]
    shop_history=[]
    
    def __init__(self):
       self.instproduct=Product()
       self.now=datetime.datetime.now()

    def addtoCart(self):

        ''' Add Products to the cart'''
        
        self.instproduct.displayProducts()
        print('\n\n\t\t***********************************************')
        print('\t\tWHAT DO YOU WANT TO DO?\n')
        print(' \t\t1. ADD TO CART ')
        print(' \t\t2. VIEW PRODUCT DETAILS ')
        print('\t\t***********************************************\n\n')
        add=int(input('Enter your choice:'))
        if add==1:
            self.instproduct.getProductID()
        elif add == 2:
            self.instproduct.getProductDescription()
            self.instproduct.displayProducts()
            self.instproduct.getProductID()
        else:
            print('\nEnter Valid Choice')
        print('\n\n================================================')
        print('    PRODUCTS  HAVE  BEEN  ADDED  TO  YOUR CART')
        print('================================================\n\n')

    def  viewCart(self):

        '''Displays the current cart'''
        
        try:
            print('\n\n==========================\nTHIS IS YOUR CURRENT CART\n==========================\n')
            print('************************************************************************************************************************')
            print(f'\'PRODUCT ID\'\t\t\'PRODUCT NAME\'\t\t\t\'PRICE IN RS.\' \t\'QUANTITY\' ')
            print('************************************************************************************************************************\n')
            for line in ShoppingCart.cartlist:
                print(f'{line[0]} \t\t\t{line[1]:15}\t{line[2]:10}\t\t{line[3]} ')
                print()
        except:
            print('\nYour Cart is Empty......Please Buy Something\n')


    def DeleteCart(self):

        '''Delete items from Cart'''
        
        self.viewCart()
        choice=input('Enter product ID which you want to delete:')
        for items in ShoppingCart.cartlist:
            if choice==items[0]:
                self.cartlist.remove(items)
        print('\nItem has been removed successfully\n')

    def UpdateCart(self):

        '''Add more products in the cart after deletion of products'''
        
        self.viewCart()
        self.instproduct.getProductID()
        print('\nYour Cart Has Been Updated Successfully\n')

    def saveHistory(self):

        ''' Saves all the shopping history of the customer
           in the file with his username'''
        
        try:
            f=open('Shopping History.txt','a')
            ShoppingCart.shop_history.append([User.username,self.now.strftime('%d-%m-%y'),self.now.strftime('%H:%M:%S')])
            for item in ShoppingCart.cartlist:
                ShoppingCart.shop_history.append([item[1],item[3],item[2]])
        except:
            print('\nERROR SAVING HISTORY\n')
        else:
            f.write(str(ShoppingCart.shop_history))
            f.write('\n')
        finally:
            f.close()
        
    def checkout(self):
        
        '''When the user checkout it calls the saveHistory
          function and calls the viewHistory function'''
        
        self.saveHistory()
        print('\nYOUR SHOPPING HISTORY HAS BEEN SAVED SUCCESSFULLY\n')
        self.ViewHistory()

        
    def ViewHistory(self):

        '''Displays Customer's Shopping History'''
        
        count=0
        f1=open('Shopping History.txt','a+')
        confirm=input('\nEnter your Username:')
        f1.seek(0)
        for line in f1:
            line=eval(line)
            for i in range(1):
                if confirm in line[0]:
                    count+=1
            if count == 1:
                print('\n\n*************************************************************************')
                print('\t\tBILL RECIEPT')
                print('*************************************************************************\n')
                print('*************************************************************************')
                print(f'USERNAME\tDATE\t\tTIME')
                print('*************************************************************************')
                print(f'\n{line[0][0]}\t\t{line[0][1]}\t\t{line[0][2]}')
                print('\n***************************************************************************')
                print(f'PRODUCTS\tQTY\t\tPRICE')
                print('***************************************************************************')
                length=len(line)
                c=1
                totalbill=[]
                q=0
                for j in range(0,length-1):
                    print(f'\n{line[c][0]}\t\t{line[c][1]}{line[c][2]}Rs.')
                    q+=line[c][1]
                    a=line[c][2].strip()
                    bill=int(a)*line[c][1]
                    totalbill.append(bill)
                    c+=1
                print('***************************************************************************')
                print('TOTAL\t\t',q,'\t\t',sum(totalbill),'Rs.')
                print('***************************************************************************')
        if count==0:
            print('\nWRONG USERNAME')



    
                    
class User(ABC):

    '''An Abstract Class that manages the verification
    of username and password'''

    customer_info=[]
    username=''
    passw=''
        
    @abstractmethod
    def Login(self):
        
        '''An abstract method that verifies userid and password'''
        
        count=0
        print('\n****VERIFY YOUR ACCOUNT****\n')
        User.username=input('Enter your user name:')
        User.passw=input('Enter your password:')
        f=open('RECORDS.txt','a+')
        f.seek(0)
        for line in f:
            line=eval(line.strip())
            if User.username in line[0] and User.passw in line[1]:
                    print('\nLOGIN SUCCESSFULLY!!\n')
                    count+=1
        if count==1:
            return True
        else:
            print('\nSORRY!!!, YOU HAVE NO PREVIOUS ACCOUNT\n')
            return False
        

      
class Customer(FileSaver,User):
    
    '''Child class of User that Saves the record of the customer '''

    def __init__(self):
        
        User.__init__(self)
        self.first_name=''
        self.last_name=''
        self.address=''
        self.phone_number=''
        self.instcart=ShoppingCart()

        

    def Verification(self):

        '''Verify if the customer is a previous customer or a new one'''
        
        verify=input('\nARE YOU A REGISTERED CUSTOMER? PRESS \'y\' or \'n\'....')
        if verify=='y' or verify=='Y':
            self.Login()
        else:
            acc=input('\nDO YOU WANT TO CREATE ACCOUNT?PRESS \'y\' or \'n\'......')
            if acc=='y' or acc=='Y':
                self.createAccount()
                self.Login()
            else:
                sys.exit()
              
    def createAccount(self):
        
        '''creates account of the customer if he has no previous account'''
        
        print('\n****CREATE YOUR ACCOUNT****\n')
        User.username=input('Create User Name:')
        User.passw=input('Create Password:')
        self.first_name=input('Enter first name:')
        self.last_name=input('Enter last name:')
        self.address=input('Enter your Address where the products will deliver:')
        self.phone_number=input('Enter your phone number:')
        User.customer_info.append([User.username,User.passw,self.first_name,self.last_name,self.address,self.phone_number])
        self.savetoFile(User.customer_info,'RECORDS.txt')
        print('\nYOUR ACCOUNT HAS BEEN CREATED SUCCESSFULLY!!\n')
        

    def Login(self):

        '''Inherits User's Login method'''
        
        if User.Login(self)==True:
            try:
                while True:
                    print('\n\n\t\t***********************************************')
                    print('\t\tWHAT DO YOU WANT TO DO?\n')
                    print('\t\t1. VIEW ACCOUNT DETAILS\n\t\t2. UPDATE PROFILE\n\t\t3. SHOPPING')
                    print('\t\t***********************************************\n\n')
                    view=int(input('Enter your choice:'))
                    if view==1:
                       self.ViewAccountInfo()
                    elif view==2:
                       self.updateProfile()
                    else:
                        self.instcart.addtoCart()
                    break
            except:
                print('\nEnter Input in integers')
                sys.exit()
                
        else:
            account=input('\nDO YOU WANT TO CREATE YOUR ACCOUNT?PRESS \'y\' or \'n\'...')
            if account=='y':
                self.createAccount()
                self.Login()
            else:
                sys.exit()
                
    def ViewAccountInfo(self):

        '''Displays Account information of the customer'''
        
        count=0
        user_name=input('\n\nEnter your username:')
        f=open('Records.txt','a+')
        f.seek(0)
        for item in f:
            item=eval(item.strip())
            if user_name == item[0]:
                print('\nUSER NAME VERIFIED')
                print('\nUSERNAME:',item[0],'\nPASSWORD:',item[1],'\nFIRSTNAME:',item[2],'\nLASTNAME:',item[3],\
                      '\nADDRESS:',item[4],'\nPHONE NUMBER:',item[5],'\n')
                count+=1
        if count==0:
            print('\nWRONG USER NAME\n')
        print('\n\n AGAIN SIGN IN TO THE APPLICATION\n')
        self.Login()

    def updateProfile(self):
        
        '''Updates Customer's account information '''
        
        User.username=input('Create User Name:')
        User.passw=input('Create Password:')
        self.address=input('Enter your Address where the products will deliver:')
        self.phone_number=input('Enter your phone number:')
        User.customer_info.append([User.username,User.passw,self.first_name,self.last_name,self.address,self.phone_number])
        self.savetoFile(User.customer_info,'RECORDS.txt')
        print('\nYour Data has been saved Successfully!\n')
        self.Login()



      
class UserInterface(Customer):

    ''' A class that is responsible for all the functions
      and is interlinked with almost all the classes'''
    
    def __init__(self):
        super().__init__()
        self.LoginSystem()
        self.Shopping()
        
    def LoginSystem(self):
        print('\n\n\t\t===========================================')
        print('\t\t         WELCOME     TO     ONLINE     SHOPPING   ')
        print('\t\t===========================================\n\n')
        print('\n\t\t************************************************************************')
        print('\t\t    WHAT DO YOU WANT TO DO?')
        print('\n\t\t   1. LOGIN OR CREATE YOUR ACCOUNT TO PURCHASE.')
        print('\t\t   2. VIEW   PREVIOUS   SHOPPING   HISTORY.')
        print('\t\t   3. EXIT.   ')
        print('\t\t************************************************************************')
        ch=int(input('\nEnter your choice:'))
        if ch==1:
            self.Verification()
        elif ch==2:
            self.instcart.ViewHistory()
            self.LoginSystem()
        else: 
            sys.exit()
            
            
    def Shopping(self):
        while True:
            print('\n\n\t\t***********************************************')
            print('\t\tWHAT DO YOU WANT TO DO?\n')
            print(' \t\t1. VIEW CURRENT  CART ')
            print(' \t\t2. DELETE ITEMS FROM CART ')
            print(' \t\t3. UPDATE CART ')
            print(' \t\t4 . CHECKOUT ')
            print('\t\t***********************************************\n')
            choose=int(input('\nEnter your choice:'))
            if choose == 1:
                self.instcart.viewCart()
            elif choose == 2:
                self.instcart.DeleteCart()
            elif choose == 3:
                self.instcart.UpdateCart()
            elif choose == 4:
                self.instcart.checkout()
                self.LoginSystem()
            else:
                print('\nEnter Valid Choice')

        
        

u=UserInterface()


