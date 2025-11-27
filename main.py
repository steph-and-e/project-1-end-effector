"""
This is a Python-based order processing system for a warehouse for ENGINEER 1P13 Project 1.
The system allows users to sign into the system, packs scanned products using a Q-arm,
updates a products and orders database, and prints an order summary when finished.

Jordan Sung - Sungy4
Stephanie Li - Li3424
Rachel Roberts - Roberr28
Evelyn Liu - Liu2906
Inuka Silva - Silvag6

ENGINEER 1P13, Team TUES-21, 2025
"""

# Import modules
import bcrypt
import random
from time import sleep
import sys
sys.path.append("../")

# Toggle qArm mode on and off
qArm = False # Change to True when testing with Q-Arm

# Q-arm setup
if qArm:
    from Common.qarm_interface_wrapper import *
    GRIPPER_IMPLEMENTATION = 1
    arm = QArmInterface(GRIPPER_IMPLEMENTATION)
    scan_barcode = BarcodeScanner.scan_barcode



## PICK UP SPONGE FUNCTION
def pick_up_sponge():
    """
    Executes Q-arm movements to pick up the sponge
    - Parameters: None
    - Input: None
    - Output: None
    - Return: None
    Author(s): Jordan Sung (Sungy4), Rachel Roberts (Roberr28)
    """
    arm.home()
    arm.rotate_base(16)
    arm.rotate_elbow(-22)
    arm.rotate_gripper(13)
    arm.rotate_shoulder(55)
    sleep(1)
    arm.rotate_gripper(-13)
    arm.rotate_shoulder(-50)
    arm.home()



## PICK UP BOTTLE FUNCTION
def pick_up_bottle():
    """
    Executes Q-arm movements to pick up the bottle
    - Parameters: None
    - Input: None
    - Output: None
    - Return: None
    Author(s): Jordan Sung (Sungy4), Rachel Roberts (Roberr28)
    """
    arm.home()
    arm.rotate_base(9)
    arm.rotate_elbow(-17)
    arm.rotate_gripper(10)
    arm.rotate_shoulder(53)
    sleep(1)
    arm.rotate_gripper(-10)
    arm.rotate_shoulder(-53)
    arm.home()



## PICK UP CHESS FUNCTION
def pick_up_chess():
    """
    Executes Q-arm movements to pick up the rook
    - Parameters: None
    - Input: None
    - Output: None
    - Return: None
    Author(s): Jordan Sung (Sungy4), Rachel Roberts (Roberr28)
    """
    arm.home()
    arm.rotate_base(3)
    arm.rotate_elbow(-17)
    arm.rotate_gripper(11)
    arm.rotate_shoulder(57)
    sleep(1)
    arm.rotate_gripper(-11)
    arm.rotate_shoulder(-57)
    arm.home()



## PICK UP DICE FUNCTION
def pick_up_dice():
    """
    Executes Q-arm movements to pick up the D12
    - Parameters: None
    - Input: None
    - Output: None
    - Return: None
    Author(s): Jordan Sung (Sungy4), Rachel Roberts (Roberr28)
    """
    arm.home()
    arm.rotate_base(-4)
    arm.rotate_elbow(-14)
    arm.rotate_gripper(13)
    arm.rotate_shoulder(55)
    sleep(1)
    arm.rotate_gripper(-13)
    arm.rotate_shoulder(-55)
    arm.home()



## PICK UP CONE FUNCTION
def pick_up_cone():
    """
    Executes Q-arm movements to pick up the witch hat
    - Parameters: None
    - Input: None
    - Output: None
    - Return: None
    Author(s): Jordan Sung (Sungy4), Rachel Roberts (Roberr28)
    """
    arm.home()
    arm.rotate_base(-10)
    arm.rotate_elbow(-17)
    arm.rotate_gripper(5)
    arm.rotate_shoulder(55)
    sleep(1)
    arm.rotate_gripper(-5)
    arm.rotate_shoulder(-55)
    arm.home()



## PICK UP BOWL FUNCTION
def pick_up_bowl():
    """
    Executes Q-arm movements to pick up the bowl
    - Parameters: None
    - Input: None
    - Output: None
    - Return: None
    Author(s): Jordan Sung (Sungy4), Rachel Roberts (Roberr28)
    """
    arm.home()
    arm.rotate_base(-18)
    arm.rotate_elbow(-17)
    arm.rotate_gripper(13)
    arm.rotate_shoulder(55)
    sleep(1)
    arm.rotate_gripper(-13)
    arm.rotate_shoulder(-55)
    arm.home()



## DROP OFF OBJECT FUNCTION
def drop_off_object():
    """
    Executes Q-arm movements to drop off objects in the packing basket
    - Parameters: None
    - Input: None
    - Output: None
    - Return: None
    Author(s): Jordan Sung (Sungy4), Rachel Roberts (Roberr28)
    """
    arm.home()
    arm.rotate_base (-60)
    arm.rotate_elbow(40)
    arm.rotate_shoulder(15)
    sleep(0.5)
    arm.rotate_gripper(25)
    sleep(0.5)
    arm.rotate_gripper(-25)
    arm.rotate_shoulder(-15)
    arm.home()



## PRINT COLOUR FUNCTION
def print_colour(colour, text):
    """
    Helper function that prints to the screen with a specified colour
    - Parameters: Colour, text to print
    - Input: None
    - Output: Text in specified colour
    - Return: None
    Author(s): Stephanie Li (Li3424)
    """
    colours = {"black":30, "red":31, "green":32, "yellow":33, "blue":34, "magenta":35, "cyan":36, "white":37}
    colour_id = colours[colour]
    print(f"\033[{colour_id}m{text}")
    print("\033[37m", end="") # prints empty white line to reset colour



## SIGN UP FUNCTION
def sign_up():
    """
    Creates a new user account and logs the userid and hashed password in users.csv
    - Parameters: None
    - Input: User credentials, users.csv
    - Output: Writes a new line to users.csv
    - Return: None
    Author(s): Jordan Sung (Sungy4)
    """
    print_colour("blue", "\n\n\nSIGN UP")

    # Loop until successful signup
    while True:

        # Ask user for new userid and password
        userid = input("Enter a new userid: ").strip()
        password = input("Enter a new password: ").strip()

        # Check if userid already exists
        try:
            file = open("users.csv", "r")
            existing_users = []
            for line in file:
                row = line.split(",")
                stored_userid = row[0]
                existing_users.append(stored_userid)
            if userid in existing_users:
                print_colour("red", "UserID already exists. Please try again.\n")
                continue # skip remaining code, go back to beginning of while loop
            file.close()
        except: # if file does not exist, userid does not already exist
            pass

        # Check password length
        if len(password) < 6:
            print_colour("red", "Password must be 6 chars or longer! Please try again.\n")
            continue # skip remaining code, go back to beginning of while loop

        # Check that password contains all required characters
        capital = any(c.isupper() for c in password) 
        lower = any(c.islower() for c in password)
        digit = any(c.isdigit() for c in password)
        special_chars = "!.@#$%^&*()_[]"
        special = any(c in special_chars for c in password)
        if not (capital and lower and digit and special):
            print_colour("red", "Password invalid. Make sure your password includes at least one uppercase, one lowercase, one number, and one specoal character.\n")
            continue # skip remaining code, go back to beginning of while loop

        # If user gets here, the signup input has passed all checks
        # Encrypt password
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Save userid and hashed password
        file = open("users.csv", "a") # Append mode: creates new csv if file doesn't exist
        file.write(f"{userid}, {hashed}\n") # Write user id and password on new line
        file.close()
        print_colour("green","Account created successfully!")
        return # Exit out of function



## AUTHENTICATE FUNCTION
def authenticate():
    """
    Logs the user in, creating an account first if needed
    - Parameters: None
    - Input: User credentials, users.csv;
    - Output: Success or failure messages
    - Return: userid (string) upon successful authentication
    Author(s): Stephanie Li (Li3424)
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
        sleep(1)
        sign_up()
        print_colour("blue", "\n\n\nAUTHENTICATION") # show user when they return to Authenticate

    # Loop until successful authentication
    while True:
        # Ask user to enter userid and password
        userid = input("Please enter your userid: ").strip()
        password = input("Please enter your password: ").strip()
        
        # Try to find userid in users.csv
        found = False
        file = open("users.csv", "r")
        for line in file:
            row = line.split(",")
            if len(row) < 2: # If row is incorrectly formatted, skip and go to next line
                continue
            stored_userid = row[0]
            stored_hash = row[1].strip()
            # If userid matches, check if password matches
            if userid == stored_userid:
                found = True
                # If password matches, login is successful
                if bcrypt.checkpw(password.encode('utf-8'),
                                      stored_hash.encode('utf-8')):
                    print_colour("green", "Login successful!")
                    file.close()
                    return userid
                # Password does not match --> Try again
                else:
                    print_colour("red", "Incorrect password. Please try again.\n")
                    break # break out of for loop, stay in while loop

        # Userid does not match --> Try again
        if not found:
            print_colour("red", "Userid not found. Please try again.\n")

        # Close file
        file.close()
            


## LOOKUP PRODUCTS FUNCTION
def lookup_products(productNames):
    """
    Compares a string of scanned items to products.csv and returns a 2D list of products with their prices
    - Parameters: products (string of product names)
    - Input: products.csv
    - Output: Warning message when product not found
    - Return: 2D list of products: [[name, price], ...
    Author(s): Rachel Roberts (Roberr28)
    """

    # Initialize empty lists
    fileList = []
    productList = []
    finalList = []

    # Split product string into a list
    productList = productNames.split() # Splits on whitespace

    # 
    file = open("products.csv")
    for product in file: # Turns the string from file into a two by two list
        product = product.strip()
        product = product.split(",")
        product[1] = float(product[1]) #Turns the string number into a float
        fileList.append(product)
    file.close()

    # Iterate through product list and add each product's info to final list
    for i in range (len(productList)): # Goes through all indexes of productList
        for j in range(len(fileList)): # Goes through all indexes of fileList, if doesn't enter if statement'
            if productList[i] == fileList[j][0]: # Item in productList appears in file, so add to finalList
                finalList.append(fileList[j])
                break
            if j == 5: # If j gets to 5 then product doesn't appear in file because have only 6 products in file
                print_colour("red", f"WARNING! We don't sell {productList[i]}s. Only scan items that are sold in products.csv.")

    # Return final list with products and their prices
    return finalList



## COMPLETE ORDER FUNCTION
def complete_order(userID, product_list):
    """
    Outputs product info in a receipt format and updates orders.csv
    - Parameters: userid (string), product_list (2D list of [[name, price], ...])
    - Input: None
    - Output: Printed invoice and order summary; updates orders.csv with new order
    - Return: None
    Author(s): Evelyn Liu (Liu2906)
    """

    total = 0
    user_cart = []
    num_orders = 0
    receipt = "\n" + "Warehouse".center(50) + "\n" + "-"*50 + "\n" + "-"*50 + "\n" + "Items:"

    file = open("orders.csv", "a") # Append mode: appends rows to already existing file

    for i in range(len(product_list)):
        # Product_list is a list from the lookup_products function
        total += product_list[i][1]
        # Add up the total price of the items in the list [[name, price][name, price]]
        user_cart.append(product_list[i][0])
        # Adds the item name to the list for return later
        price = f"${product_list[i][1]:.2f}"
        receipt += f"\n{product_list[i][0]:<44}{price}"
        # includes the item into the reciept in a nice way

    ## Write into order.csv
    order = [userID, str(round(total, 2))] + user_cart
    file.write(",".join(order) + "\n") # add the order to orders.csv - converts everything to a string (appears in individual boxes in excel)
    file.close()

    file2 = open("orders.csv")
    for line in file2:
        line = line.split(",")
        if userID == line[0]:
            num_orders += 1
        # How many orders has this user made so far
    file2.close()

    ## Calculations
    subtotal = total
    discount = -(total * (random.randint(5, 50)/100))
    subtotal2 = subtotal + discount
    HST = subtotal*0.13
    total = subtotal + discount + HST

    fsubtotal = f"${subtotal:.2f}"
    fdiscount = f"${discount:.2f}"
    fsubtotal2 = f"${subtotal2:.2f}"
    fHST = f"${HST:.2f}"
    ftotal = f"${total:.2f}"

    divider = "-"*50
    receipt += f"\n{divider}\nSubtotal{fsubtotal:>42}\nDiscount{fdiscount:>42}\nSubtotal{fsubtotal2:>42}\nHST{fHST:>47}\n{divider}\n{divider}\nTotal{ftotal:>45}"
    # The receipt format - for the subtotal, discount(percentage not listed, just the amount that is discounted), tax (HST), and total
    print(f"{receipt}\n{userID} has made {num_orders} orders so far")



## CUSTOMER SUMMARY FUNCTION
def customer_summary(userid: str):
    """
    Prints the order history of the user from orders.csv in a receipt format
    - Parameters: userid (string)
    - Input: orders.csv
    - Output: Printed order history summary
    - Return: None
    Author(s): Inuka Silva (Silvag6)
    """
    print_colour("blue", "\n\n\nCUSTOMER SUMMARY")

    s = f"" # this is a output string
    total_cost = 0 # total money spent
    num_of_orders = 0 # total number of orders
    output_list_products = [] # list of all the products the user has ordered
    output_list_quantity = [] # list of the number of each product the user has ordered
    filename = "orders.csv" # name of file

    try:
        f = open(filename, 'r') # tries to open the file (if exists)
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



## PACK PRODUCTS FUNCTION
def pack_products(products_list):
    """
    Executes Q-arm movements to pick up and drop off each product in the product list
    - Parameters: product_list (2D list of products [[name, price], ...])
    - Input: None
    - Output: Q-Arm motor commands. Printed messages confirming each product packed.
    - Return: None
    Author: Stephanie Li (Li3424)
    """
    # Iterate through product list
    for product_row in products_list:
        # Get product name from the product-price pair
        product_name = product_row[0]
        # Execute appropriate Q-arm movements depending on product
        if product_name == "Sponge":
            if qArm:
                pick_up_sponge()
                drop_off_object()
            print_colour("green", "Successfully packed Sponge!")
        elif product_name == "Bottle":
            if qArm:
                pick_up_bottle()
                drop_off_object()
            print_colour("green", "Successfully packed Bottle!")
        elif product_name == "Rook":
            if qArm:
                pick_up_chess()
                drop_off_object()
            print_colour("green", "Successfully packed Rook!")
        elif product_name == "D12":
            if qArm:
                pick_up_dice()
                drop_off_object()
            print_colour("green", "Successfully packed D12!")
        elif product_name == "Bowl":
            if qArm:
                pick_up_bowl()
                drop_off_object()
            print_colour("green", "Successfully packed Bowl!")
        elif product_name == "WitchHat":
            if qArm:
                pick_up_cone()
                drop_off_object()
            print_colour("green", "Successfully packed WitchHat!")
        else:
            print_colour("red", f"{product_name} not in directory!")



## MAIN FUNCTION
def main():
    """
    Runs the entire warehouse ordering system in a loop until user decides to exit
    - Parameters: None
    - Input: User input, barcode scanner input
    - Output: Printed messages from authentication, invoices, summaries, and Q-Arm actions
    - Return: None
    Author(s): Inuka Silva (Silvag6)
    """
    # Get userid from authenticate function
    userid = authenticate()

    # Run warehouse system until user decides to quit
    shouldContinue = True
    while shouldContinue:
        # Display Menu
        print_colour("blue", "\n\n\nWAREHOUSE MENU")
        print("[1] Order Items")
        print("[2] Quit")
        try:
            userChoice = int(input("What would you like to do? [1, 2]: "))
        except ValueError:
           print("That is not a valid option! Please enter the number corresponding to the option :D")
        else:
            if userChoice == 1:
                print_colour("blue", "\n\n\nORDER ITEMS")
                print("Please scan a barcode:")
                if qArm:
                    orderString = input(scan_barcode())
                else:
                    orderString = input()
                print("Processing order...\n")
                sleep(1)
                orderList = lookup_products(orderString)
                pack_products(orderList)
                sleep(1)
                complete_order(userid, orderList)
            elif userChoice == 2:
                # user chooses to exit
                print("Quitting warehouse program...")
                sleep(1)
                shouldContinue = False
            else:
                print("You didn't enter a valid number. Please try again.") 
        
    customer_summary(userid)

main()