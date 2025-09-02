import datetime
from read import read_furniture_data


#index
product_id=0
manufacturer_name = 1
product_name=2
available_quantity= 3
product_price = 4

shipment_cost=100

def display_furniture(furniture_data):
    """
    parameter: furniture_data
    returns: none
    displays furniture data in terminal
    """
    print('ID | Manufacturer                | Product Name    | Quantity    | Price')
    print("-"*72)
    for data in furniture_data:
        row_data=data[0]+" "*(3-len(data[0]))+'| '
        row_data+=data[1]+" "*(28-len(data[1]))+'| '
        row_data+=data[2]+" "*(16-len(data[2]))+'| '
        row_data+=data[3]+" "*(12-len(data[3]))+'| '
        row_data+=(data[4].replace("\n",""))
        print(row_data)
        print("-"*72)


def verify_quantity(order_quantity,order_index,is_employee,furniture_data):
    """
    parameter: (order_quantity,order_index,is_employee,furniture_data
    returns: order_quantity
    checks if there is sufficient amount of product for sales
    """
    while True:
        try:
            order_quantity=int(order_quantity)
            if(order_quantity<=0):# checks if quantity is negative or zero
                print("Enter a valid quantity")
                order_quantity=input('Enter quantity: ')
            elif (order_quantity<=int(furniture_data[order_index][available_quantity]) or is_employee):# checks if the quantity is available or is made by the employee
                return int(order_quantity)
            else:
                print("Sorry, we have only have "+(furniture_data[order_index][available_quantity])+ (' '+furniture_data[order_index][product_name]))
                order_quantity = input('Enter the quantity to be ordered: ')
        except ValueError:
            print("Enter a valid quantity")
            order_quantity=input('Enter quantity: ')



def get_order_index(order_product,furniture_data):
    """
    parameter:order_product,furniture_data
    returns:order_index
    checks if given product name or Id exists in our inventory and returns order_index if found
    """
    product_name_list=[]
    product_id_list=[]
    for datas in furniture_data:
        product_name_list.append(datas[product_name])
        product_id_list.append(datas[product_id])
    while True:
        try:
            if(order_product.isdigit()):# checks if the number is digit
                order_index = product_id_list.index(order_product)# returns order_index if id matches 
                return order_index
            else:
                order_index = product_name_list.index(order_product)# returns order_index if name matches 
                return order_index
        except ValueError :
            print('\nProduct not Found\n')
            order_product= input('Enter correct product name or ID:') # if the product name is not found, informs the user to re-enter


def create_line(invoice):
    """
    parameter: invoice
    returns: invoice
    adds a line in invoice
    """
    invoice+="            |"+"-"*100+"|\n" #generates line in the invoice
    return invoice 

        
def generate_invoice(order_name,order_cart,is_employee,furniture_data,is_shipment):
    """
    paramater:iorder_name,order_cart,is_employee,furniture_data,is_shipment
    returns: invoice, file_path
    stores invoice data into invoice variable and manages file_path 
    """
    sub_total_price=0
    current_date_time= datetime.datetime.now()
    order_date = current_date_time.strftime("%a %b %d %Y")
    order_time=current_date_time.strftime("%X")
    
    file_name=order_name +'_'+ current_date_time.strftime('%b%d%Y_%H%I%M%S') + '.txt'      #creating file name
    if(is_employee):
        file_path = 'transaction/Buy_'+file_name
    else:
        file_path = 'transaction/Sell_'+file_name
    invoice='''
             ____________________________________________________________________________________________________
            |                                           BRJFurniture                                             |
            |                                      Kamal Pokhari, Kathmandu                                      |
            |                                                                                                    |
            |                                   Contact : 0123456789                                             |
            |                                   Email :BRJFurniture@gmail.com                                    |
            |----------------------------------------------------------------------------------------------------|\n'''
    invoice+="            | Time: "+order_time+" "*64+"Date: "+order_date+"|\n"
    if(is_employee):
        invoice+="            | Employee Name:"+order_name+" "*(85-len(order_name))+"|\n"
    else:
        invoice+="            | Customer Name:"+order_name+" "*(85-len(order_name))+"|\n"
    invoice= create_line(invoice)
    invoice+="            | ID"+" "*10+"| Manufacturer"+" "*17+"| Product Name"+" "*4+"| Quantity"+" "*4+"| Rate"+" "*4+"| Amount"+" "*6+"|\n"
    invoice=create_line(invoice)
    for order_index,order_quantity in order_cart.items():
        amount_per_item= int(furniture_data[order_index][product_price].replace('\n','').replace('$',''))*order_quantity
        sub_total_price+=amount_per_item
        invoice+="            | "+str(furniture_data[order_index][product_id])+" "*(12-len(furniture_data[order_index][product_id]))+"| "
        invoice+=furniture_data[order_index][manufacturer_name]+" "*(29-len(furniture_data[order_index][manufacturer_name]))+"| "
        invoice+=furniture_data[order_index][product_name]+" "*(16-len(furniture_data[order_index][product_name]))+"| "
        invoice+=str(order_quantity)+" "*(12-len(str(order_quantity)))+"| "
        product_rate = furniture_data[order_index][product_price].replace('\n','')
        invoice+=(product_rate+" "*(8-len(product_rate))+"| ")
        invoice+="$"+str(amount_per_item)+" "*(11-len(str(amount_per_item)))+"|\n"

    invoice= create_line(invoice)
    invoice+="            |"+" "*(87-len(str(sub_total_price)))+'Subtotal : $'+str(sub_total_price)+' |\n'
    if(is_employee):
        if(is_shipment):
            final_price=sub_total_price+shipment_cost
            invoice+="            |"+" "*(87-len(str(shipment_cost)))+'Shipment : $'+str(shipment_cost)+' |\n'
        else:
            final_price=sub_total_price
        vat_amount = final_price*0.13
        invoice+="            |"+" "*(90-len(str(vat_amount)))+'VAT 13: $'+str(vat_amount)+' |\n'
        final_price+=vat_amount
    else:
        vat_amount = sub_total_price*0.13
        invoice+="            |"+" "*(89-len(str(vat_amount)))+'VAT 13%: $'+str(vat_amount)+' |\n'
        final_price=sub_total_price+vat_amount
        if(is_shipment):
            final_price+=shipment_cost
            invoice+="            |"+" "*(87-len(str(shipment_cost)))+'Shipment : $'+str(shipment_cost)+' |\n'
    
    invoice=create_line(invoice)
    invoice+="            | Grand Total : $"+str(final_price)+" "*(84-len(str(final_price)))+"|\n"
    invoice+="            |____________________________________________________________________________________________________|"
 
    return invoice, file_path

def need_another_product():
    """
    paramater:none
    returns: True or False
    asks user if they want to order another product
    """
    while True:
        choice = input('\nDo you want to purchase another item?(y/n): ')#presents user the option if they want to buy another product
        if choice.lower()=='y':
            return True 
        elif choice.lower()=='n':
            return False
        else:
            print("Please enter ('y') or ('n')")

        

def welcome_screen_and_handle_order(inventory_file_name):
    """
    parameter: inventory_file_name
    returns: invoice , furniture_data, file_path
    displays welcome screen and adds product to cart ordered by the user
    """
    furniture_data = read_furniture_data(inventory_file_name)# reads data from the inventory file
    if furniture_data is None:
        return "Inventory Not Found"
    order_cart={}# creates empty dictionary for order
    while True:
        print('''
                     ___________________________________________________________
                    |                       BRJFurnitures                       |
                    |                  Kamal Pokhari, Kathmandu                 |
                    |                                                           |
                    |                   Contact : 0123456789                    |
                    |              Email : BRJFurniture@gmail.com               |
                    |-----------------------------------------------------------|
                    |                    WELCOME TO BRJ FURNITURE               |
                    |-----------------------------------------------------------|
                    |           PLEASE SELECT FROM ONE OF THE OPTIONS           |
                    |-----------------------------------------------------------|
                    |  1) Buying Furniture                                      |
                    |  2) Selling Furniture                                     |
                    |  3) Exit                                                  |
                    |___________________________________________________________|
                    ''')
        option = input("Enter your Option: ")# provides input on whether to run program for the employee or the customer
        if option=='1': 
            is_employee= True   
        elif option=='2':
            is_employee= False
        elif option=='3':
            return 
        else:
            print("Please enter option 1,2 or 3")
            continue
        order_name = input('Enter name: ')
        print("\nHi "+order_name+",")
        print("What do you wanna buy today?\n")
        while True:
            print("Displaying Furniture Data:\n")
            display_furniture(furniture_data)# prints available product
            print(' ')
            order_product= input('Enter product name or ID:')# provides input for the user to enter product name
            order_index= get_order_index(order_product,furniture_data)# returns index of the product
            order_quantity=input('Enter quantity: ')
            order_quantity=verify_quantity(order_quantity,order_index,is_employee,furniture_data)
            if(not order_index in order_cart):#checks in product already ordered
                order_cart[order_index]=order_quantity#adds to cart
            else:
                print("\nProduct already ordered")
                if(need_another_product()):
                    continue
                else:
                    break
            if is_employee:
                furniture_data[order_index][available_quantity]= str(int(furniture_data[order_index][available_quantity])+ order_quantity)#adds item to the stock if done by employee
            else:   
                furniture_data[order_index][available_quantity]= str(int(furniture_data[order_index][available_quantity])- order_quantity)#subtracts item from the stock if done by employee
            print("\nCurrent Cart List:\n")
            for order_index, quantity in order_cart.items():
                print(furniture_data[order_index][product_name],"--->", quantity)
            if(need_another_product()):
                continue
            else:
                break
        while True:
            is_shipment_required = input("Do you require shipment(y/n), charge:100$: ")# asks user if they need shipment
            if(is_shipment_required=="y"):
                is_shipment = True
                break
            elif(is_shipment_required=="n"):
                is_shipment= False
                break
            else:
                print("Please enter ('y') or ('n')")

        transaction_data = generate_invoice(order_name,order_cart,is_employee,furniture_data,is_shipment)
        invoice = transaction_data[0]
        file_path=transaction_data[1]
        print("\n            __________________________________________Digital-Invoice____________________________________________")
        print(invoice)
        return invoice , furniture_data, file_path
            
            

