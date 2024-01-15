from App import TransmitterApp
import os

file_path = r"Transmitter\dist\wordList.txt"
binary_file_path = r"Transmitter\dist\binaryWordList.txt"
receiver_binary_file_path = r"Receiver\src\receiverBinaryWordList.txt"

def writeBinary(binary, file_path):
    with open(file_path, "a") as f:
        f.write(binary + "\n")

app_instance = TransmitterApp()

try:
    
    if os.path.getsize(receiver_binary_file_path) > 0:
        with open(receiver_binary_file_path, "w"):
            pass  # This leaves the file empty

    if os.path.getsize(binary_file_path) > 0:
        with open(binary_file_path, "w"):
            pass  # This leaves the file empty    

    with open(file_path, "r") as f:
        for line in f:
            bin_str = line.strip()
            
            
            
            binary = app_instance.make_binary(bin_str)
            
            
            writeBinary(binary, binary_file_path)
            
            
            writeBinary(binary, receiver_binary_file_path)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
