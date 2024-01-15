import serial

ser = serial.Serial('COM6', 57600)

file_path = "receiverBinaryWordList.txt"

while True:
    if ser.in_waiting > 0:
        data = ser.readline().strip()
        if data:  # Check if data is non-empty
            print(data.decode("utf-8"))
            try:
                with open(file_path, "ab") as file:  # 'ab' mode for writing bytes
                    file.write(data + b"\n")
                    file.flush()
                f = open("messages.txt", "ab")
                f.write(data+b"\n")
                f.close()
            except Exception as e:
                print(f"Error writing to file: {e}")