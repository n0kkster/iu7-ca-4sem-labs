from ui import print_menu, read_choice
from handler import process_choice

def main() -> None:
    
    while (True):
        print_menu()
        choice = read_choice()
        process_choice(choice)

if __name__ == '__main__':
    main()