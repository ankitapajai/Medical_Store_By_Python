import mysql.connector
from bcrypt import hashpw, gensalt, checkpw

# Connect to the MySQL database
def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medical"
    )
    return connection

# Register a new user
def register_user(conn):
    cursor = conn.cursor()
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    email = input("Enter Email: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    is_admin = input("Is this an admin account? (yes/no): ").strip().lower() == 'yes'

    # Hash the password
    password = hashpw(password.encode('utf-8'), gensalt())

    query = "INSERT INTO login (first_name, last_name, email, username, password, is_admin) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (first_name, last_name, email, username, password, is_admin)

    try:
        cursor.execute(query, values)
        conn.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Log in an existing user
def login_user(conn):
    cursor = conn.cursor()
    username = input("Enter username: ")
    password = input("Enter password: ")

    query = "SELECT id, password, is_admin FROM login WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        print(f"Welcome, {username}!")
        return user[2]  # Return is_admin (True/False)
    else:
        print("Invalid username or password!")
        return None

# Add a medicine
def add_medicine(conn):
    cursor = conn.cursor()
    name = input("Enter medicine name: ")
    batch_no = input("Enter batch number: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    expiry_date = input("Enter expiry date (YYYY-MM-DD): ")

    query = "INSERT INTO medicines (name, batch_no, price, quantity, expiry_date) VALUES (%s, %s, %s, %s, %s)"
    values = (name, batch_no, price, quantity, expiry_date)

    try:
        cursor.execute(query, values)
        conn.commit()
        print("Medicine added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Update a medicine
def update_medicine(conn):
    cursor = conn.cursor()
    medicine_id = int(input("Enter the medicine ID to update: "))
    print("1. Update name\n2. Update batch number\n3. Update price\n4. Update quantity\n5. Update expiry date\n6. Update all")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        new_value = input("Enter new name: ")
        query = "UPDATE medicines SET name = %s WHERE id = %s"
        cursor.execute(query, (new_value, medicine_id))
    elif choice == 2:
        new_value = input("Enter new batch number: ")
        query = "UPDATE medicines SET batch_no = %s WHERE id = %s"
        cursor.execute(query, (new_value, medicine_id))
    elif choice == 3:
        new_value = float(input("Enter new price: "))
        query = "UPDATE medicines SET price = %s WHERE id = %s"
        cursor.execute(query, (new_value, medicine_id))
    elif choice == 4:
        new_value = int(input("Enter new quantity: "))
        query = "UPDATE medicines SET quantity = %s WHERE id = %s"
        cursor.execute(query, (new_value, medicine_id))
    elif choice == 5:
        new_value = input("Enter new expiry date (YYYY-MM-DD): ")
        query = "UPDATE medicines SET expiry_date = %s WHERE id = %s"
        cursor.execute(query, (new_value, medicine_id))
    elif choice == 6:
        new_name = input("Enter new name: ")
        new_batch_no = input("Enter new batch number: ")
        new_price = float(input("Enter new price: "))
        new_quantity = int(input("Enter new quantity: "))
        new_expiry_date = input("Enter new expiry date (YYYY-MM-DD): ")
        
        query = """
            UPDATE medicines 
            SET name = %s, batch_no = %s, price = %s, quantity = %s, expiry_date = %s 
            WHERE id = %s
        """
        cursor.execute(query, (new_name, new_batch_no, new_price, new_quantity, new_expiry_date, medicine_id))
    else:
        print("Invalid choice!")
        return

    conn.commit()
    print("Record updated successfully!")


# Delete a medicine
def delete_medicine(conn):
    cursor = conn.cursor()
    medicine_id = int(input("Enter the ID of the medicine to delete: "))

    query = "DELETE FROM medicines WHERE id = %s"
    try:
        cursor.execute(query, (medicine_id,))
        conn.commit()
        print("Medicine deleted successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# View medicines
def view_medicines(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM medicines"
    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print("No medicines found!")
    else:
        print("\nID | Name | Batch No | Price | Quantity | Expiry Date")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")


# Admin menu
def admin_menu(conn):
    while True:
        print("\n--- Medical Store ---")
        print("1. Add Medicine\n2. Update Medicine\n3. Delete Medicine\n4. View Medicines\n5. Logout")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_medicine(conn)
        elif choice == 2:
            update_medicine(conn)
        elif choice == 3:
            delete_medicine(conn)
        elif choice == 4:
            view_medicines(conn)
        elif choice == 5:
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# User menu
def user_menu(conn):
    while True:
        print("\n--- User Menu ---")
        print("1. View Medicines\n2. Buy Medicines\n3. Logout")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            view_medicines(conn)
        elif choice == 2:
            buy_medicines(conn)
        elif choice == 3:
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")



# Function to remove medicines with zero stock
def remove_zero_stock_medicines(conn):
    cursor = conn.cursor()
    query = "DELETE FROM medicines WHERE quantity = 0"
    cursor.execute(query)
    conn.commit()

# Updated buy_medicines function
def buy_medicines(conn):
    cursor = conn.cursor()
    cart = []
    total_cost = 0

    while True:
        view_medicines(conn)  # Show available medicines
        medicine_id = int(input("Enter the ID of the medicine to add to your cart: "))
        quantity = int(input("Enter the quantity to buy: "))

        # Fetch medicine details
        query = "SELECT name, price, quantity FROM medicines WHERE id = %s"
        cursor.execute(query, (medicine_id,))
        medicine = cursor.fetchone()

        if not medicine:
            print("Invalid medicine ID! Please try again.")
            continue

        name, price, available_quantity = medicine

        if quantity > available_quantity:
            print(f"Only {available_quantity} units of {name} are available.")
            continue

        # Add to cart and reduce inventory
        cart.append((name, price, quantity))
        total_cost += price * quantity

        # Update inventory in database
        update_query = "UPDATE medicines SET quantity = quantity - %s WHERE id = %s"
        cursor.execute(update_query, (quantity, medicine_id))
        conn.commit()

        print(f"\nAdded {quantity} units of {name} to your cart.")
        
        # Ask to continue or checkout
        more = input("Do you want to add more medicines? (yes/no): ").strip().lower()
        if more != 'yes':
            break

    # Clean up medicines with zero stock
    remove_zero_stock_medicines(conn)

    # Generate a ticket
    if cart:
        print("\n--- Purchase Ticket ---")
        print("Medicine Name | Price per Unit | Quantity | Total Price")
        print("-" * 50)
        for item in cart:
            print(f"{item[0]} | {item[1]} | {item[2]} | {item[1] * item[2]}")
        print(f"\nTotal Cost: {total_cost}")
        print("-" * 50)
        print("Thank you for your purchase!")
    else:
        print("No items purchased.")



# Main menu with login functionality
def main_menu(conn):
    while True:
        print("\n--- Welcome to Medical Store Management System ---")
        print("1. Register\n2. Login\n3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            register_user(conn)
        elif choice == 2:
            user_role = login_user(conn)
            if user_role is not None:  # Successful login
                if user_role:  # is_admin is True
                    admin_menu(conn)  # Admin menu
                else:
                    user_menu(conn)  # User menu
            else:
                print("Please try logging in again.")
        elif choice == 3:
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    conn = connect_to_database()
    main_menu(conn)
    conn.close()
