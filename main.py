# import modules
import random
import time
import bcrypt
import os
import csv

## HELPER FUNCTION
def print_colour(colour, text):
    """
    Helper function that prints to the screen with a specified colour
    """
    colours = {"black":30, "red":31, "green":32, "yellow":33, "blue":34, "magenta":35, "cyan":36, "white":37}
    colour_id = colours[colour]
    print(f"\033[{colour_id}m{text}")
    print("\033[37m", end="") # prints empty white line to reset colour


## SIGN UP FUNCTION
def sign_up():
    """
    """
    print_colour("blue", "\n\n\nSIGN UP")
    users_file = "users.csv"
    ## Create CSV file with header if it does not exist
    if not os.path.exists(users_file):
        with open(users_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["userid", "encrypted_password"])
    ## Prompt user
    userid = input("Enter a new userid: ").strip() #removes extra space
    password = input("Enter a new password: ").strip()

    ## Check if userid already exists
    with open(users_file) as file:
        reader = csv.reader(file)
        next(reader)  # skip header

        for row in reader:
            if row and row[0] == userid:
                print("User ID already exists")
                return

    ## Check password length first (as in flowchart)
    if len(password) < 6:
        print("Password too short!")
        return

    ## Check password rules
    # 'for c in password' means check every letter in the system
    capital = any(c.isupper() for c in password)
    lower = any(c.islower() for c in password)
    digit = any(c.isdigit() for c in password)
    special_chars = "!.@#$%^&*()_[]"
    special = any(c in special_chars for c in password)

    if not (capital and lower and digit and special):
        print("Password Invalid. Include spedcial letters in your password.")
        return

    ## Encrypt password
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    ## Save userid and hashed password
    with open(users_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([userid, hashed])

    print("Account created Successfully")

## AUTHENTICATE FUNCTION
def authenticate():
    """
    - Logs the user in, creating an account first if needed.
    - Prompts the user for userid and password, then checks them against bcrypt-hashed passwords in users.csv.
      Repeats until valid credentials are entered.
    - Returns: userid upon successful login
    """
    print_colour("blue", "\n\n\nAUTHENTICATION")

    # Ask user if they have an account
    has_account = input("Do you have an account? (Y/N): ").upper().strip()
    # Input validation
    while has_account not in ["Y", "N"]:
        has_account = input("Please enter a valid response. Do you have an account? (Y/N): ").upper()
    # If user does not have an account, redirect them to sign up
    if has_account == "N":
        print("Redirecting to sign up...")
        time.sleep(1)
        sign_up()
        print_colour("blue", "\n\n\nAUTHENTICATION") # show user when they return to Authenticate

    # Loop until successful authentication
    while True:
        # Ask user to enter userid and password
        userid = input("\nPlease enter your userid: ").strip()
        password = input("Please enter your password: ").strip()
        
        # Try to find userid in users.csv
        found = False
        file = open("users.csv", "r")
        for line in file:
            row = line.split(",")
            stored_userid = row[0]
            stored_hash = row[1].strip()
            # If userid matches, check if password matches
            if userid == stored_userid:
                found = True
                # If password matches, login is successful
                if bcrypt.checkpw(password.encode('utf-8'),
                                      stored_hash.encode('utf-8')):
                    print_colour("green", "Login successful!")
                    return userid
                # Password does not match --> Try again
                else:
                    print_colour("red", "Incorrect password. Please try again.")
                    break # break out of for loop, stay in while loop

        # Userid does not match --> Try again
        if not found:
            print_colour("red", "Userid not found. Please try again.")

        # Close file
        file.close()
            
## LOOKUP PRODUCTS FUNCTION
def lookup_products(productNames):
    """Reads products.csv, and compares it to a string of scanned items it recieves from a user. Prints a warning message if item scanned is not in products.csv, and returns a list of product names with their prices that match the scanned string"""

    fileList = []
    productList = []
    finalList = []

    productNames = productNames.replace(' and ', ',')
    productNames = productNames.replace(', ', ',')# replace space-comma with comma
    productList = productNames.split(",")

    file = open("products.csv")
    for product in file: #Turns the string from file into a two by two list
        product = product.strip()
        product = product.split(",")
        product[1] = float(product[1]) #Turns the string number into a float
        fileList.append(product)
    file.close()

    for i in range (len(productList)): #Goes through all indexes of productList
        for j in range(len(fileList)): #Goes through all indexes of fileList, if doesn't enter if statement'
            if productList[i] == fileList[j][0]: #Item in productList appears in file, so add to finalList
                finalList.append(fileList[j])
                break
            if j == 5: #If j gets to 5 then product doesn't appear in file because have only 6 products in file
                print(f"WARNING! We don't sell {productList[i]}'s. Only scan items that are sold in products.csv.")

    return finalList

##
def complete_order():
    """
    """
    pass

##
def customer_summary(userid: str):
    """
    Prints the order history of <userid> from orders.csv.
    prints off the userid, number of orders, total cost, and
    the number of each product they have ordered, formatted in 
    a receipt.
    """
    s = f"" # this is a output string
    total_cost = 0 # total money spent
    num_of_orders = 0 # total number of orders
    output_list_products = [] # list of all the products the user has ordered
    output_list_quantity = [] # list of the number of each product the user has ordered
    filename = "orders.csv" # name of file

    try:
        f = open(filename, 'r') # trys to open the file (if exists)
    except:
        # error is thrown if file doesn't exist
        print("File not found, unable to retrieve order history")
    else:

        # for each line in the file
        for line in f:
            l = line.strip().split(",") # removes whitespaces and new lines, then turns into a list

            # checks for correct user
            if l[0] == userid:
                # tries to convert the cost into a float, if that works
                try:
                    total_cost += float(l[1]) # adds to the cost accumulator
                    num_of_orders += 1 # adds to the number of order accumulator
                    for i in l[2:]:
                        # iterate through the rest of the list
                        # if the product hasn't already been seen, make a new entry in the accumulator lists
                        if i not in output_list_products:
                            output_list_products.append(i)
                            output_list_quantity.append(1)
                        else:
                            output_list_quantity[output_list_products.index(i)] += 1
                except:
                    print("An error has occured while compiling order history")

        # formats the string 
        s += f"User: {userid}\n"
        s += f"Total number of orders: {num_of_orders}\n"
        s += f"Total: ${total_cost:.2f}\n"
        s += "===================================\n"
        for i in range(len(output_list_products)):
            s += f"{output_list_products[i]}{output_list_quantity[i]:>30}\n"
        s += "===================================\n"
        print(s)

def pack_products(products_list):
    """
    """
    # Iterate through product list
    for product_row in products_list:
        # Get product name from the product-price pair
        product_name = product_row[0]
        # Execute appropriate Q-arm movements depending on product
        if product_name == "Sponge":
            print_colour("green", "Successfully packed Sponge!")
        elif product_name == "Bottle":
            print_colour("green", "Successfully packed Bottle!")
        elif product_name == "Rook":
            print_colour("green", "Successfully packed Rook!")
        elif product_name == "D12":
            print_colour("green", "Successfully packed D12!")
        elif product_name == "Bowl":
            print_colour("green", "Successfully packed Bowl!")
        elif product_name == "WitchHat":
            print_colour("green", "Successfully packed WitchHat!")
        else:
            print_colour("red", f"{product_name} not in directory!")


def main():
    """
    g.	main(): (team function) this function runs the entire warehouse ordering system. It begins by welcoming the user, then calls authenticate() to log them in and/or sign them up. If then allows the user to place as many orders as they like by scanning bar codes. It uses lookup_products() to find prices for scanned products, then calls pack_products() to load them with the Q-Arm and complete_order() to finalize payment and store the order. When the user is finished filling orders, it prints the customer_summary().
    i.	Parameters: None
    ii.	Input: User input, barcode scanner input.
    iii.	Output: Printed messages from authentication, invoices, summaries, and Q-Arm actions
    iv.	Return Value: None

    """
    # Get userid from authenticate function
    userid = authenticate()

    # Run warehouse system until user decides to quit
    shouldContinue = True
    while shouldContinue:
        # Display Menu
        print_colour("blue", "\n\n\nWELCOME TO THE WAREHOUSE!")
        print("[1] Order Items")
        print("[2] Quit")
        try:
            userChoice = int(input(""))
        except TypeError:
           print("Please enter the number corresponding to the option :D")
        else:
            if userChoice == 1:
                print("please scan a barcode...")
                orderString = scan_barcode() #TODO: Change to proper function
                orderList = lookup_products(orderString) #TODO: Change to proper function
                pack_products(orderList)#TODO: Change to proper function
                #y
                # complete_order(userid, orderList)#TODO: Change to proper function
            elif userChoice == 2:
                # user chooses to exit
                print("quitting warehouse program...")
                shouldContinue = False
            else:
                print("You didn't enter a valid number, please try again") 
        
    print("Thank you for using our warehouse system :D")
    customer_summary(userid)

def scan_barcode():
    return ""

main()