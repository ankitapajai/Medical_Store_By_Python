# List to store medicine details
medicines = []

# Add medicine
def add_medicine():
    name = input("Enter medicine name: ")
    batch_no = input("Enter batch number: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    expiry_date = input("Enter expiry date (YYYY-MM-DD): ")

    medicine = {
        "id": len(medicines) + 1,
        "name": name,
        "batch_no": batch_no,
        "price": price,
        "quantity": quantity,
        "expiry_date": expiry_date
    }
    medicines.append(medicine)
    print("Medicine added successfully!")

# Update medicine
def update_medicine():
    medicine_id = int(input("Enter the medicine ID to update: "))
    medicine = next((m for m in medicines if m["id"] == medicine_id), None)

    if medicine:
        print("1. Update name\n2. Update batch number\n3. Update price\n4. Update quantity\n5. Update expiry date")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            medicine["name"] = input("Enter new name: ")
        elif choice == 2:
            medicine["batch_no"] = input("Enter new batch number: ")
        elif choice == 3:
            medicine["price"] = float(input("Enter new price: "))
        elif choice == 4:
            medicine["quantity"] = int(input("Enter new quantity: "))
        elif choice == 5:
            medicine["expiry_date"] = input("Enter new expiry date (YYYY-MM-DD): ")
        else:
            print("Invalid choice!")
            return
        print("Medicine updated successfully!")
    else:
        print("Medicine not found!")

# Delete medicine
def delete_medicine():
    medicine_id = int(input("Enter the medicine ID to delete: "))
    global medicines
    medicines = [m for m in medicines if m["id"] != medicine_id]
    print("Medicine deleted successfully!")

# View medicines
def view_medicines():
    if not medicines:
        print("No medicines found!")
    else:
        print("\nID | Name | Batch No | Price | Quantity | Expiry Date")
        print("-" * 50)
        for med in medicines:
            print(f"{med['id']} | {med['name']} | {med['batch_no']} | {med['price']} | {med['quantity']} | {med['expiry_date']}")

# Menu
def menu():
    while True:
        print("\n--- Welcome to Medical Store Management System ---")
        print("1. Add Medicine\n2. Update Medicine\n3. Delete Medicine\n4. View Medicines\n5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_medicine()
        elif choice == 2:
            update_medicine()
        elif choice == 3:
            delete_medicine()
        elif choice == 4:
            view_medicines()
        elif choice == 5:
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    menu()
