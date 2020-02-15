import csv # for reading and writing CSV files
import codecs # for reading the Â£ sign
from operator import itemgetter # for selecting column to sort

def globalVars():
    global totalBags # to keep running total
    global totalValue # to keep running total
    global coinFileName
    global volunteers # used throughout the program
    totalBags = 0
    totalValue = 0
    coinFileName = "CoinCount.txt"
    volunteers = []


def menu():
    
        coinFile=open(coinFileName)
    
        
        menuChoice = "0"
    
        menuChoice=""

        global volunteers
       
        with codecs.open(coinFileName,"r","utf-8") as coinFile:
            # codecs and utf-8 is needed for the £ symbol
            coinReader = csv.reader(coinFile) #CSV-comma separated values
            for row in coinReader:
                volunteers.append(row)

    # repeat until 0 is chosen to exit the program
    
        print("""
        Coin Count Menu

        1) Input bag details
        2) Show running totals
        3) Volunteer accuracy report

        0) Exit

        """)
    

        # initialise so rest of program runs at least once
        menuChoiceOK = False

        while not menuChoiceOK:
        # repeat while an invalid menu option has been chosen
            menuChoice=input("Enter number of your choice: ")
            if menuChoice=="1": # input bag details chosen
                countCoins()
                menuChoiceOK = True
            elif menuChoice=="2": # running totals chosen
                displayTotals()
                menuChoiceOK = True
            elif menuChoice=="3": # report chosen
                volunteerReport()
                menuChoiceOK = True
            elif menuChoice=="0": # quit chosen
                saveExit()
                menuChoiceOK = True
            else: # invalid option chosen
                print("Please input only 1, 2, 3 or 0: ")
            

def countCoins():
    volunteerName = input("Please enter your name: ")
    coinType = validateCoinType() # check the coinType exists
    bagWeight = validateBagWeight()

    coin = findCoin(coinType) # find the current coin type details

    # assign array values to variable names
    coinValue = coin[1] # value of coin in pence
    coinsInBag = coin[2] # number of coins expected in bag
    coinWeight = coin[3] # weight of individual coin
    expectedBagWeight = coin[4] # expected weight of coin bag

    # CHECK BAG WEIGHT
    
    if bagWeight == expectedBagWeight:
    
        print("Correct bag weight, thank you")
        correct = "Y" 
    else:
        print("You entered a bag weight of", bagWeight, "grams")
        print("The bag weight should be", expectedBagWeight, "grams")
        
        weightDifference = expectedBagWeight - bagWeight
       
        coinsDifference = weightDifference / coinWeight
        correct ="N" # to be saved to file

        print("The difference in weight is",
              "{:.2f}".format(weightDifference), "grams")
        if weightDifference > 0:
        
            print("You need to add", coinsDifference, "coins")
        else: 
            print("You need to remove", coinsDifference*-1,
                  "coins")

    # CALCULATE TOTALS
    global totalBags
    totalBags = totalBags + 1 # one more bag for this session added to total

    newValue = coinValue * coinsInBag # calculate value of coins in bag

    global totalValue # changing global variable
    totalValue = totalValue + newValue # running total value

    # create single row for new volunteer data
    newVolunteer = [volunteerName,coinType,bagWeight,correct]

    global volunteers # changing global variable
    volunteers.append(newVolunteer) # add new volunteer to volunteers list

    input("Press any key to continue")

# end countCoins

def validateCoinType():
# validate input of coin type against list of valid coins
    
    
    validCoins=["£2","£1","50p","20p","10p","5p","2p","1p"]
    # initialise so input runs at least once
    validCoin = False
    while not validCoin: # repeat until the coin is valid
        coinInput = input("Please enter the coin type: ")
        if coinInput in validCoins: # input coin exists
            validCoin = True
        else: # input coin does not exist
            validCoin = False
            print("Your must input a valid coin from the list below:")
            print(validCoins)
    return coinInput

# end validate coin type
def validateBagWeight():

    
        bagInput = input("Please enter the bag weight: ")
        
        bagReal=float(bagInput) # attempt to convert input to real
        
        return bagReal # return the value input by user
# end validate bag weight


def findCoin(coinType):

    # set values and weights of coins
    coins = [["£2",200,10,12.00,120.00],
         ["£1",100,20,8.75,175.00],
         ["50p",50,20,8.00,160.00],
         ["20p",20,50,5.00,250.00],
         ["10p",10,50,6.50,325.00],
         ["5p",5,100,3.25,325.00],
         ["2p",2,50,7.12,356.00],
         ["1p",1,100,3.56,356.00]]

   
    for coinLine in coins: # for each type of coin
        if coinLine[0] == coinType:
        # if first column matches the inputted coinType
            break
    return coinLine


def displayTotals():
    print("Running totals for this session\n")
    print("Total bags checked = ", totalBags)
    # format to 2 decimal places
   # valueInPounds = "{:.2f}".format(totalValue / 100)
    print("Total value = £", valueInPounds)
    input("Press any key to continue")
# end displayTotals

def volunteerReport():
    print("Volunteer Accuracy Report\n")

    volunteerNames = []

    for volunteer in volunteers:
    # for each volunteer in the list of volunteers and bags counted
        if volunteer[0] not in volunteerNames:
        # if the volunteer is unique (doesn't exist in volunteerNames)
            # append the volunteer name to a list of volunteerNames
            volunteerNames.append(volunteer[0])

    sortedSummary = calculateSummary(volunteerNames)

    displaySummary(sortedSummary)

def calculateSummary(volunteerNames): # calculate summary values
    summary = [] # initialise new list
    for volunteerName in volunteerNames:
    
        totalBags = 0
        accuracy = 0
        for volunteer in volunteers:
            # for each volunteer's count of coins in the list
            if volunteer[0] == volunteerName:
           
                totalBags += 1 # increment totalBags
                if volunteer[3] == "Y": # if input weight was accurate
                    accuracy += 1 # increment accuracy

        # calculate percentage accuracy
        accuracyPercent = accuracy / totalBags * 100
        # append name, percentage accuracy and total bags to a summary list
        summary.append([volunteerName,accuracyPercent,totalBags])

    # sort the summary list by accuracy percent (column 2 in list)
    # itemgetter selects the second column
    summary.sort(key=itemgetter(1))

    return summary
# end calculate summary

def displaySummary(summary):
    print("    Name         Accuracy  Total Bags")
    for item in summary: # for each volunteer's summary
        vName = item[0]
        vAccuracy = "{:.0f}%".format(item[1]) # format accuracy to 0 decimals
        vTotalBags = item[2]
        print("   ",vName, "\t", vAccuracy, "\t  ", vTotalBags)
    input("Press any key to continue")
# end display summary

def saveExit():
    print("You have chosen to end the session.  Bye bye.")
    with codecs.open(coinFileName, 'w',"utf-8") as coinWFile:
        # using codecs and utf-8 there is no need to specify new line character
        # codecs and utf-8 is needed for the £ symbol
        coinWriter = csv.writer(coinWFile)
        coinWriter.writerows(volunteers)
# end volunteer report

# #### MAIN PROGRAM STARTS HERE ######

globalVars()
menu()

# #### MAIN PROGRAM ENDS HERE ######
