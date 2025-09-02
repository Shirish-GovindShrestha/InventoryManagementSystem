from operation import welcome_screen_and_handle_order
from write import update_inventory, write_invoice


inventory_file_name='inventory.txt'# change name

def main():
    """parameter: none
        returns: none
        calls function from other python files in a loop
    """
    while True:
        transaction_data = welcome_screen_and_handle_order(inventory_file_name)
        if transaction_data is None:
            print("Thank you for shopping") # ending program
            break
        elif (transaction_data=="Inventory Not Found"): # ends program when inventory file is not found
            break 
        else:   
            invoice= transaction_data[0]
            furniture_data=transaction_data[1]
            file_path = transaction_data[2]
            update_inventory(furniture_data,inventory_file_name)
            write_invoice(invoice, file_path)
        
main()
