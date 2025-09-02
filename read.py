
def read_furniture_data(inventory_file_name):
    """parameter: inventory_file_name
        returns: furniture_data
        takes in file name and returns data in the textfile in form of 2d array
    """
    furniture_data=[]# creates empty arraylist
    try:
        with open(inventory_file_name,'r') as file:#opening file in write mode
            for line in file:
                part= line.split(', ')# single line in the text is split list
                furniture_data.append(part)
        return furniture_data# returns 2d arraylist of all the product detail in the file
    except FileNotFoundError:
        print("Inventory file(inventory.txt) not found")
        return
