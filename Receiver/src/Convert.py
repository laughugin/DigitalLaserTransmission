class Convert:
    def __init__(self):
        pass  
    
    def binary_to_text(self, binary_message):
        try:
            if len(binary_message) % 8 != 0:
                raise ValueError("Error: Binary message length is not divisible by 8")
        except Exception as e:
            print(e)
            return None
    
        text = ""
        for i in range(0, len(binary_message), 8):  
            binary_chunk = binary_message[i:i+8]
            text += self._binary_to_decimal(binary_chunk)
    
        return text
    
    def _binary_to_decimal(self, binary_str):
        decimal_value = int(binary_str, 2)
        print(decimal_value)
        return self._decimal_to_ascii(decimal_value) 
    
    def _decimal_to_ascii(self, decimal_value):
        ascii_text = chr(decimal_value)
        return ascii_text


def main():
    binary_converter = Convert()
    binary_message = "01100100011000011000111100000000"
    text = binary_converter.binary_to_text(binary_message)
    print("Text:", text)


if __name__ == "__main__":
    main()
