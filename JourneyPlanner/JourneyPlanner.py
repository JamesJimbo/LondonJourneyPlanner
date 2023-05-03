#James McKenna
#Made using IDLE IDE

import requests
import json
import datetime
import urllib.parse

api_id = ''
api_key = ''

#Input your own api ID and api key.

print("Welcome to the Transport for London checker\n")

#New function for checking the tube
def tubeCheck():

    getRequest = requests.get("https://api.tfl.gov.uk/Line/Mode/Tube/Status")
    #GET request to retrive data from the TfL server.
    
    #print(f"\nStatus code from GET Request is {getRequest.status_code}\n")
    #Lines like this have been commented out as it was used for testing purposes.

    print("\nWelcome to the Transport for London Underground checker\n")
    print("Please enter a number for the line you want to check:\n")

    lineNames = []

    data = getRequest.json()
    #Converts the data into json format.

    for i, line in enumerate(data):
        lineNames.append(f"{i} - {line['name']}")

    for line in lineNames:
        print(line)

    #Prints every line name in the shell.

    try:
        number = int(input("\n> "))
        if number < 0 or number > 10:
            print("\nPlease enter a valid number")
            return tubeCheck()
        else:
            print(f"\nYou have selected {number}\n")
            rawData = getRequest.json()
            lineName = rawData[number]

        #If the user inputs a number less than 0 or greater than 10, it is invalid
        #and they are prompted to input again. If it is a string or another data type
        #then the exception handling will catch it and return the function again.

        print(f"Welcome to the {lineName['name']} line\n")
        #Accessing an element in a nested dictionary.
        
        print(f"The current status on the {lineName['name']} line is {lineName['lineStatuses'][0]['statusSeverityDescription']}")

        #lineName is a dictionary that contains information about tube lines, the 'name' key
        #is used to access the name of the tube line. The 'lineStatuses' key gives access to
        #a list of dictionaries that contain information about the statuses of the line.
        #index [0] is used to access the first dictionary in the list. The 'statusSeverityDescription'
        #key accesses the description of the current status.
        
        print(f"\nNow showing all available stops for the {lineName['name']} line:\n")
        getRequest = requests.get(f"https://api.tfl.gov.uk/line/{lineName['id']}/stoppoints")
        
        #Changed the request from name to ID as 4 and 10 returned a key error.
        
        stopPoints = getRequest.json()
        stopCount = 0
        for stop in stopPoints:
            print(stopPoints[stopCount]['commonName'])
            stopCount += 1
        enter = input("\nPress enter to return to the menu\n")

        #Prints out all the stations on that line.
        

    except (ValueError, UnboundLocalError, IndexError) as error:
        print(f"\n{type(error).__name__}. Please enter a valid number")
        return tubeCheck()

    #Handling errors if user enters anything else other than a number or an invalid number


#New function for checking the roads
def roadCheck():
    try:
        getRequest = requests.get(f"https://api.tfl.gov.uk/road")
        #print(f"Status code from GET Request is {getRequest.status_code}\n")
        rawData = getRequest.json()

        print("Welcome to Transport for London Road Checker\n")

        data = requests.get("https://api.tfl.gov.uk/Road").json()
        roadNames = [f"{i} - {road['displayName']}" for i, road in enumerate(data)]
        print("\n".join(roadNames))

        #A list is used instead of a set as there are no repeating values.
        #Prints every line name in the shell, similar to the tubeCheck function.

        print("\nType in the number that you would like to check:\n")
        
        roadName = int(input("> "))
        if roadName < 0 or roadName > 22:
            print("\nPlease enter a valid number\n")
            return roadCheck()
        else: 
            roadData = rawData[roadName]
            print(f"Now viewing data for {roadData['displayName']}\n")
            print(f"The current status of {roadData['displayName']} is {roadData['statusSeverity']} with {roadData['statusSeverityDescription']}\n")
            enter = input("Press enter to return to the main menu")

        #If the user inputs a number less than 0 or greater than 22, it is invalid
        #and they are prompted to input again. If it is a string or another data type
        #then the exception handling will catch it and return the function again.
        
        
    except (ValueError, UnboundLocalError, IndexError) as error:
        print(f"\n{type(error).__name__}. Please enter a valid number\n")
        return roadCheck()

    #Handling errors if user enters anything else other than a number or an invalid number

#New function for planning a route
def travelRoute():
    try:           
        session = requests.Session()

        response = session.get("https://api.tfl.gov.uk/line/mode/tube/status")
        lines = response.json()

        stationNames = set()
        stationIDs = {}

        #A set is more efficient as it removes duplicates, stations can be on multiple lines,
        #so this gets rid of repeats and only shows the station names once. Sets also use
        #hash tables so it has an average time complexity of O(1).

        for line in lines:
            response = session.get(f"https://api.tfl.gov.uk/line/{line['id']}/stoppoints")
            stopPoints = response.json()

            for stopPoint in stopPoints:
                name = stopPoint['commonName'].replace(' Underground Station', '')
                naptanID = stopPoint['naptanId']
                stationNames.add(name)
                stationIDs[name] = naptanID

        #This nested for loop checks each tube and its stop points, using the ID to convert it into text format.
        #It then adds removes underground station for simplicity of showing the user all stations. It uses
        #the common name instead of the ID as the ID is a set of numbers that the user would not understand.

        #The NaPTAN ID is not used for this project due to complications, however, the code has been left in
        #in case someone wants to use it.

        print("\nList of available stations:\n")

        for i, name in enumerate(sorted(stationNames)):
            print(f"{i+1} - {name}")

        #prints every station, whereas the tubeCheck prints every line.

        startNum = input("\nEnter start number: ")
        if not startNum.isdigit():
            print("Invalid input, please enter a number.")
        else:
            startNum = int(startNum)
            if startNum < 1 or startNum > len(stationNames):
                print("Invalid station number.")
            else:
                startName = sorted(stationNames)[startNum-1]
                startID = stationIDs[startName]
                print(f"\nYou have selected {startName} as your starting station.")

        endNum = input("\nEnter end number: ")
        if not endNum.isdigit():
            print("Invalid input, please enter a number.")
        else:
            endNum = int(endNum)
            if endNum < 1 or endNum > len(stationNames):
                print("Invalid station number.")
            else:
                endName = sorted(stationNames)[endNum-1]
                endID = stationIDs[endName]
                print(f"\nYou have selected {endName} as your destination station.\n")

        #The user is prompted to input the start and end destination by inputting the corresponding
        #number. If the input is invalid then the program will return an error and run the function
        #again until the correct inputs are inputted. Number inputs were simpler as there can be no
        #spelling mistakes or extra spaces, it's also simpler for the user to input.
            
        print("Now fetching route, please wait...\n")

        getRequest = requests.get(f"https://api.tfl.gov.uk/journey/journeyresults/{startName}/to/{endName}?app_id={api_id}&app_key={api_key}")
        #print(f"Status code from GET is {getRequest.status_code}")
        rawData = getRequest.json()
        
        startPoint = rawData['fromLocationDisambiguation']['disambiguationOptions'][0]['parameterValue']
        print(f"The ICS Code for the start point is {startPoint}")
        #Finding the ICS Code for start point
        
        endPoint = rawData['toLocationDisambiguation']['disambiguationOptions'][0]['parameterValue']
        print(f"The ICS Code for the end point is {endPoint}\n")
        #Finding the ICS Code for end point

        #Find the ICS Code for the start and end destination - used to build another GET request.
        #The ICS Code is a unique identifier for each station. It's simpler for the system to
        #identify each station with a number than the full name.
        
        rawJourneyData = requests.get(f"https://api.tfl.gov.uk/journey/journeyresults/{startPoint}/to/{endPoint}?app_id={api_id}&app_key={api_key}")
        #print(f"Status code from GET is {rawJourneyData.status_code}")
        fullRouteResponse = rawJourneyData.json()
        journeyTime = fullRouteResponse['journeys'][0]['duration']
        print(f"The overall journey time will be {journeyTime} minutes")
        print("The journey steps are:\n")
        selectedRoute = fullRouteResponse['journeys'][0]['legs']

        #The journeyTime is set to the duration of the journey data, with
        #the journey time being displayed and the steps used to get there.
        #The ['legs'] is the list of all the legs in the journey, which
        #represents each mode of transportation or walking, so it can be
        #displayed to the user step by step.

        prevDesc = ''
        #Previous Description

        for i, detail in enumerate(selectedRoute):
            print(f"Step {i+1}:")
            print("From {}".format(detail['departurePoint']['commonName']))
            print(detail['instruction']['detailed'])
            print("Arrive at {}".format(detail['arrivalPoint']['commonName']))

            isDisrupted = detail['isDisrupted']
            if isDisrupted == True:
                for disruption in detail['disruptions']:
                    disDesc = disruption['description']
                    #Disruption Description
                    if disDesc != prevDesc:
                        print("\n------Disruption:------\n")
                        print(disDesc)
                        prevDesc = disDesc
            else:
                print("\nNo disruptions reported.")
            print()

        #For each leg, the code prints out the departure point and the
        #instructions for the journey. The code prints out if there is
        #a delay or disruption, otherwise it prints out that there are
        #no disruptions. 


    except (requests.exceptions.RequestException, KeyError, TypeError, IndexError, Exception) as error:
        print(f"{type(error).__name__}. Please enter a valid input\n")
        print("Showing Underground Stations again, please wait...")
        return travelRoute()

    #Handling errors
        
    print("Press enter to return to the main menu.")
    enter = input()


valid = True
while valid == True:
    print("=====================================================\n")
    print("""Please specify which service you would like to check:\n
1 - Underground
2 - Roads
3 - Route Checker for Underground\n
Type 'q' to quit""")
    
    check = input("\n> ")
    if check == '1':
        tubeCheck()
    elif check == '2':
        roadCheck()
    elif check == '3':
        travelRoute()
    elif check == 'q':
        print("\nGoodbye")
        valid = False
    else:
        print("Error. Please try again.\n")

#Main code, calls up functions depending on the user input.

