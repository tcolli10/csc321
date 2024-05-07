import math
import string


def caesarDecode(text, outFile):
    shifted = {}
    f = open(outFile, "a")
    for i in range(26):
        shifted[i] = ""
        for letter in text:
            if letter.isalpha():
                if letter.islower():
                    shifted[i] += chr((ord(letter) - i - 97) % 26 + 97)
                elif letter.isupper():
                    shifted[i] += chr((ord(letter) - i - 65) % 26 + 65)
            else:
                shifted[i] += letter
        f.write("Shifted " + str(i) + " | " + shifted[i])
    f.close()
    return 0




def __main__():
    file = input("Enter the file name to decrypt by caesar : ")
    outFile = input("Enter the file name to write the decrypted text : ")
    filePath = "encrypted 4/" + file
    fileToDecrypt = open(filePath, "r")
    text = fileToDecrypt.read()
    caesarDecode(text, outFile)
    print(text)
    fileToDecrypt.close()


if __name__ == "__main__":
    __main__()

