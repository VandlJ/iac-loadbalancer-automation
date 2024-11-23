import sys

def remove_first_and_last_lines(file_name):
    try:
        # Read the file's content
        with open(file_name, 'r') as file:
            lines = file.readlines()
        
        # Ensure the file has enough lines to remove both the first and last
        if len(lines) < 2:
            print(f"Error: {file_name} does not have enough lines to remove.")
            return
        
        # Write back all lines except the first and last
        with open(file_name, 'w') as file:
            file.writelines(lines[1:-1])
        
        print(f"First and last lines removed successfully from {file_name}.")
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 remove_first_and_last_lines.py <file-name>")
    else:
        file_name = sys.argv[1]
        remove_first_and_last_lines(file_name)