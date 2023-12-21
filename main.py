import string
import requests
import json
import csv

#GLOBAL VARIABLES
USERNAME = "*****" #Input username to change
OLD_PASS = "*****" #Input current password
NEW_PASS = "*****" #Input desired password
API_VERSION = "v3"
SWITCH_CSV_PATH = "switches.csv"

#For operational reporting and debugging
RESPONSE_CODES = {
    200: "The command was successful.",
    201: "The resource has been created or changed successfully.",
    202: "The command URI has been accepted.",
    400: "Bad request - parameters are formatted incorrectly.",
    401: "You do not have the permissions to perform this action.",
    403: "This action is forbidden.",
    404: "This action is not found - the API call does not exist.",
    405: "This method is not allowed.",
    500: "The request has failed due to an error in the switch."
}


#~~~ARUBA REST API FUNCTIONS~~~
# DESC:     Uses switch administrator credentials to login to switch and acquire session cookies
# PARAMS:   authURL: a string with the URL needed for creating a privileged REST API session
#           username: a string containing the switch's administrator username
#           password: a string containing the switch's administrator password
# RETURNS:  The session cookie
def acquire_session_cookie(authURL, username, password):
    # Create data payload containing admin credentials to pass to network switch
    payload = json.dumps({
        'userName': username,
        'password': password
    })
    headers = {
        'Content-Type': 'application/json'
    }
    print("Acquiring session cookies...")
    response = requests.request("POST", authURL, headers=headers, data=payload)
    print("The response code is " + str(response.status_code) + ": " + RESPONSE_CODES[response.status_code])
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
        # Save cookie key and value to JSON data structure to pass in future API requests
        cookiestr = response.json().get("cookie").split("=")
        key = cookiestr[0]
        value = cookiestr[1]
        cookie = {
            key: value
        }
        print("Session cookie is: ")
        print(cookie)
        return cookie
    else:
        return null

# DESC:     Changes the switch's administrator password to what is defined in the global variable
# PARAMS:   userURL: a string with the URL needed for updating the existing manager user on the switch
#           username: Switch's administrator username
#           password: Desired new password of switch
#           cookie: The session cookie
def change_password(userURL, username, password, cookie):
    # Create data payload with updated password to pass to switch
    payload = json.dumps({
        "type": "UT_MANAGER",
        "name": username,
        "password": password,
        "password_type": "PET_PLAIN_TEXT"
    })
    headers = {
        'Content-Type': 'application/json',
    }
    print("Changing password of the switch...")
    response = requests.request("PUT", userURL, headers=headers, data=payload, cookies=cookie)
    print("The response code is " + str(response.status_code) + ": " + RESPONSE_CODES[response.status_code])


# DESC:     Writes the password change to the switch's memory by passing the cli command "wr me"
# PARAMS:   cliURL: a string with the URL needed for passing cli commands as json objects
#           cookie: The session cookie
def write_to_memory(cliURL, cookie):
    # Create data payload with the "wr me" command to pass to the switch's CLI
    payload = json.dumps({
        "cmd": "wr me"
    })
    headers = {
        'Content-Type': 'application/json',
    }
    print("Writing password change to memory...")
    response = requests.request("POST", cliURL, headers=headers, data=payload, cookies=cookie)
    print("The response code is " + str(response.status_code) + ": " + RESPONSE_CODES[response.status_code])


####~~~~~~~~~####SCRIPT BODY###~~~~~~~~###
def main():
    # First, open CSV of switch IP addresses with the password we want to update to
    with open(SWITCH_CSV_PATH) as switch_csv:
        switch_csv_reader = csv.reader(switch_csv, delimiter=',')
        for s_row in switch_csv_reader: #For each switch in the CSV
            print("Changing password of switch at IP address " + str(s_row[0]) + ".")
            # Configure API URLS based on the IP address of the switch
            baseURL = "http://" + s_row[0] + ":80/rest/" + API_VERSION
            authURL = baseURL+"/login-sessions"
            userURL = baseURL+"/management-user/UT_MANAGER"
            cliURL = baseURL+"/cli"
            # Authenticate to the switch to acquire a session cookie to then change the password
            cookie = acquire_session_cookie(authURL, USERNAME, OLD_PASS)
            change_password(userURL, USERNAME, NEW_PASS, cookie)
            # Acquire a new cookie now that credentialing has changed and save the change to the switch's memory
            cookie = acquire_session_cookie(authURL, USERNAME, NEW_PASS)
            write_to_memory(cliURL, cookie)



if __name__ == "__main__":
    main()