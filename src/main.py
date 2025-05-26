from .core import InventoryManager

def display_menu():
    print("\n=== Inventory Management System ===")
    print("1. Add Product")
    print("2. Add User")
    print("3. List Products")
    print("4. List Users")
    print("5. Withdraw Product")
    print("6. Generate Monthly Report")
    print("7. Exit")

def main():
    manager = InventoryManager()
    
    while True:
        display_menu()
        choice = input("Select an option: ")
        
        try:
            if choice == "1":
                name = input("Product name: ")
                quantity = int(input("Initial quantity: "))
                price = float(input("Unit price: "))
                manager.add_product(name, quantity, price)
                print("Product added successfully!")
                
            elif choice == "2":
                name = input("User name: ")
                email = input("Email: ")
                manager.add_user(name, email)
                print("User registered successfully!")
                
            elif choice == "3":
                print("\n--- Registered Products ---")
                # Implement listing as needed
                
            elif choice == "4":
                print("\n--- Registered Users ---")
                # Implement listing as needed
                
            elif choice == "5":
                user_id = int(input("User ID: "))
                product_id = int(input("Product ID: "))
                quantity = int(input("Quantity: "))
                manager.withdraw_product(user_id, product_id, quantity)
                print("Withdrawal recorded successfully!")
                
            elif choice == "6":
                month = int(input("Month (1-12): "))
                year = int(input("Year: "))
                result = manager.generate_monthly_report(month, year)
                print(result)
                
            elif choice == "7":
                print("Exiting system...")
                break
                
            else:
                print("Invalid option!")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()