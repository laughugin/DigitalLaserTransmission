# Open the first file and read the lines into variable1
with open('binaryTest.txt', 'r') as file1:
    variable1 = file1.read().splitlines()

# Open the second file and read the lines into variable2
with open('receiverBinaryWordList.txt', 'r') as file2:
    variable2 = file2.read().splitlines()

# Ensure both lists have the same length
if len(variable1) != len(variable2):
    print("Error: The lists have different lengths.")
else:
    # Iterate through the lists and compare strings at the same index
    for i in range(len(variable1)):
        index = i + 1  # Adjust index to start from 1 instead of 0
        str1 = variable1[i]
        str2 = variable2[i]

        # Find positions where strings are different
        different_positions = [pos + 1 for pos, (char1, char2) in enumerate(zip(str1, str2)) if char1 != char2]

        if different_positions:
            print(f"Index {index}: Strings are different at positions {different_positions}.")
        else:
            print(f"Index {index}: Strings are identical.")
