import sys

def remove_first_line(file_name):
    try:
        # Read the file's content
        with open(file_name, 'r') as file:
            lines = file.readlines()
        
        # Ensure the file is not empty
        if not lines:
            print(f"Error: {file_name} is empty.")
            return
        
        # Write back all lines except the first
        with open(file_name, 'w') as file:
            file.writelines(lines[1:])
        
        print(f"First line removed successfully from {file_name}.")
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 remove_first_line.py <yml-file-name>")
    else:
        file_name = sys.argv[1]
        remove_first_line(file_name)