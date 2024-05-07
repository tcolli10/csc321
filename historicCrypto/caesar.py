import math
import string

caesarDict = {}


def caesarDecrypt(text):
    text = string.ascii_lowercase
    for i in range(26):
        caesarDict[i] = ""
        for j in text:
            if j.isalpha():
                if j.islower():
                    caesarDict[i] += chr((ord(j) - i - 97) % 26 + 97)
                elif j.isupper():
                    caesarDict[i] += chr((ord(j) - i - 65) % 26 + 65)
            else:
                caesarDict[i] += j
    return




def __main__():
    file = input("Enter the file name to decrypt by caesar : ")
    filePath = "encrypted 4/" + file
    fileToDecrypt = open(filePath, "r")
    text = fileToDecrypt.read()
    # caesarDecrypt(text)
    print(text)


if __name__ == "__main__":
    __main__()

