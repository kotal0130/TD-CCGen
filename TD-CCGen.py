#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import getopt
import time
import os
import sys
import datetime
from random import randint

version = "1.0.0"
# Message
os.system("clear")
real = raw_input("\033[1;33mEnter your nickname: \033[0m")
print("")
print "\033[1;31mHello \033[0m" + real + "\033[1;35m nice to meet you :)\033[0m"
time.sleep(3)
print("")
print("\033[1;32mACCESS GRANTED!!\033[1;32m")
time.sleep(2)
print("")
# Help Information
def usage():
    print("TD-CCGen.py version:{}".format(version))
    print("")
    print("\033[1;31m               +------------------------------+")
    print("               +\033[1;32m       ThonyDroid-CCGen       \033[1;31m+")
    print("               +------------------------------+")
    print("")
    print("+---------------+")
    print("+\033[1;32m Usage Method\033[1;31m +")
    print("+---------------+")
    print("")
    print("\033[1;36m     python2 TD-CCGen.py -b     [Usage Options]")
    print("     python2 TD-CCGen.py -h     Help Message")
    print("\033[1;31m")
    print("+-----------------+")
    print("+\033[;32m Usage Options\033[1;31m +")
    print("+-----------------+")
    print("")
    print("\033[1;36m     -b, -bin          Bin format")
    print("     -u, -quantity     Number of cards to generate")
    print("     -d, -date         Generate random dates")
    print("     -c, -ccv          Generate random ccv")
    print("     -g, -save         Save the cards to a file")
    print("\033[1;31m")
    print("+----------------+")
    print("+\033[;32m Usage Example\033[1;31m +")
    print("+----------------+")
    print("")
    print("\033[1;33m     QUANTITY 20\033[0m")
    print("")
    print("\033[1;36m     python2 TD-CCGen.py -b 483039xxxxxxxxxx -u 20 -d -c ")
    print("")
    print("\033[1;31m")
    print("+---------------+")
    print("+\033[;32m Edited by TD\033[1;31m +")
    print("+---------------+\033[0m")
    print("")
   

# Argument Parser
def parseOptions(argv):
    bin_format = ""
    saveopt = False
    limit = 10
    date = False
    ccv = False
    check = False

    try:
        opts, args = getopt.getopt(argv, "h:b:u:gcd", ["help", "bin", "save", "quantity", "date", "cvv"])
        for opt, arg in opts:
            if opt in ("-h"):
                usage()
                sys.exit()
            elif opt in ("-b", "-bin"):
                bin_format = arg
            elif opt in ("-g", "-save"):
                saveopt = True
            elif opt in ("-u", "-quantity"):
                limit = arg
            elif opt in ("-d", "-date"):
                date = True
            elif opt in ("-c", "-ccv"):
                ccv = True

        return (bin_format, saveopt, limit, ccv, date)

    except getopt.GetoptError:
        usage()
        sys.exit(2)

# LUHN Algorithm Based Checker
def cardLuhnChecksumIsValid(card_number):
    """ checks to make sure that the card passes a luhn mod-10 checksum """

    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1

    for count in range(0, num_digits):
        digit = int(card_number[count])

        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        sum = sum + digit

    return ( (sum % 10) == 0 )

# GENERATE A BIN BASE XXXXXXXXXXXXXXXX
def ccgen(bin_format):
    out_cc = ""
    if len(bin_format) == 16:
        # Iteration over the bin
        for i in range(15):
            if bin_format[i] in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                out_cc = out_cc + bin_format[i]
                continue
            elif bin_format[i] in ("x"):
                out_cc = out_cc + str(randint(0, 9))
            else:
                print("\nInvalid character in the format: {}\n".format(bin_format))
                print("The bin format is: xxxxxxxxxxxxxxxx of 16 digits\n")
                print("Help: python2 TD-CCGen.py -h \n")
                sys.exit()

        # Generate checksum (last digit) -- IMPLICIT CHECK
        for i in range(10):
            checksum_check = out_cc
            checksum_check = checksum_check + str(i)

            if cardLuhnChecksumIsValid(checksum_check):
                out_cc = checksum_check
                break
            else:
                checksum_check = out_cc

    else:
        print("\033[1;32m")
        print("\nERROR: Insert a valid bin\n")
        print("SOLUTION: The bin format is: 483039xxxxxxxxxx of 16 digits\n")
        print("HELP: python2 TD-CCGen.py -h\n")
        sys.exit()

    return (out_cc)

# Write on a file that takes a list for the argument
def save(generated):
    now = datetime.datetime.now()
    file_name = "cc-gen_output_{0}.txt".format(str(now.day) + str(now.hour) + str(now.minute) + str(now.second))
    f = open(file_name, 'w')
    for line in generated:
        f.write(line + "\n")
    f.close

# Random exp date
def dategen():
    now = datetime.datetime.now()
    date = ""
    month = str(randint(1, 12))
    current_year = str(now.year)
    year = str(randint(int(current_year[-2:]) + 1, int(current_year[-2:]) + 6))
    date = month + "|" + year

    return date

# Random ccv gen
def ccvgen():
    ccv = ""
    num = randint(10, 999)

    if num < 100:
        ccv = "0" + str(num)
    else:
        ccv = str(num)

    return (ccv)

# The main function
def main(argv):
    bin_list = []
    # get arg data
    (bin_format, saveopt, limit, date, ccv) = parseOptions(argv)
    if bin_format is not "":
        for i in range(int(limit)):
            if date and ccv:
                bin_list.append(ccgen(bin_format) + "|" + dategen() + "|" + ccvgen())
                print(bin_list[i])
            elif date and not ccv:
                bin_list.append(ccgen(bin_format) + "|" + dategen())
                print(bin_list[i])
            elif date and not ccv:
                bin_list.append(ccgen(bin_format) + "|" + ccvgen())
                print(bin_list[i])
            elif not ccv and not date:
                bin_list.append(ccgen(bin_format))
                print(bin_list[i])

        if not bin_list:
            print("\nERROR: the bin you inserted is not valid\n")
        else:
            print("\n All cards have been validated (check)")
            print("\n They can be used successfully")

        if saveopt:
            save(bin_list)
    else:
        usage()
        sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])