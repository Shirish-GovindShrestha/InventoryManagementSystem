
def update_inventory(furniture_data,inventory_file_name):
    """parameter: furniture_data, inventory_file_name
        returns: none
        writes updated data into txt file
    """
    try:
        with open(inventory_file_name,'w') as update:
            for item in furniture_data:#for each item in the transaction_data
                update.write(', '.join(item))#rewrites data into file
        return
    except IOError:
        print("Error while updating inventory file")


def write_invoice(invoice, file_path):
    """parameter: invoice, file_path
        returns: none
        writes invoice into txt file
    """
    try:
        with open(file_path,'w') as file: #creates invoice
            file.write(invoice)
    except FileNotFoundError:
        print("directory transaction not found")
    except IOError:
        print("Error while writing invoice")
   

