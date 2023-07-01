import sqlite3

def modify_score(username, new_score):
    with sqlite3.connect('leaderboard.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE scores SET score = ? WHERE username = ?', (new_score, username))
        conn.commit()

def change_name(username, new_name):
    with sqlite3.connect('leaderboard.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE scores SET username = ? WHERE username = ?', (new_name, username))
        conn.commit()

def delete_score(username):
    with sqlite3.connect('leaderboard.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM scores WHERE username = ?', (username,))
        conn.commit()

def main():
    print("Welcome to the leaderboard management CLI.")
    while True:
        print("\nOptions:")
        print("1. Modify score")
        print("2. Change name")
        print("3. Delete score")
        print("4. Exit")

        choice = input("Enter your choice: ")
        
        if choice == "1":
            username = input("Enter the username: ")
            new_score = int(input("Enter the new score: "))
            modify_score(username, new_score)
            print("Score modified successfully!")
        elif choice == "2":
            username = input("Enter the username: ")
            new_name = input("Enter the new name: ")
            change_name(username, new_name)
            print("Name changed successfully!")
        elif choice == "3":
            username = input("Enter the username: ")
            delete_score(username)
            print("Score deleted successfully!")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
