import bheemo

keyID = None

#TO-DO: function for validating blockchain address?

# Register -> insertUser
# Login Check -> check user
'''
Login -> receive address -> validate address format -> checkUser(address) -> return value
    if return value false print not registered
    else
    var = get address logged in
    setUser(var)
    continue>

Register -> receive address -> validate address format -> checkUser(address) ->
    if value false; address is registered OR invalid
    else:
    addUser(address) -> return value
    regis succesful(notif)

print('[1] Create a Record [2] Modify Record Permission\n [3] Retrieve a Record\n  [4] View Notifications
[5] Logout  [6] Logout and Exit')

CreateRecord -> ask all inputs
inputs:                                 return:
rDate -> function now()                     true/false? - success/fail
birthday                                    recordID
Name
gender
Address
city
Code
Description
bcost
expense
coverage

ModifyRecordPermission -> ask all inputs
inputs:                                 return:
ownerAddress (not inputted by user)        success/fail
recipientAddress                           privateKey
recordID
accessCode(permission)
keyID? (not inputted by user)

Retrieve a Record -> ask record ID -> retrieveRecord()
inputs:                                 return:
ownerAddress                                decrypted record; print with format
record ID
privateKey

Logout -> break Main menu loop(?)
Logout and Exit -> exit()(?)
'''

def userfunc():
    logged = True

    currentAcct = bheemo.getCurrentAcct()
    while (logged):
        print('[1] Create a Record\n[2] Modify Record Permission\n[3] Retrieve a Record\n[4] View Notifications\n[5] Logout\n\n')
        try:
            choice = int(input('Input Action: '))

            if choice == 1:
                recordDate = input ('Enter record date: ')
                birthDay = input ('Enter birthday: ')
                name = input ('Enter name: ')
                gender = input ('Enter gender: ')
                address = input ('Enter home address: ')
                city = input ('Enter city: ')
                code = input ('Enter vaccine code: ')
                description = input ('Enter vaccine description: ')
                baseCost = input ('Enter vaccine base cost: ')
                expense = input ('Enter total expense: ')
                coverage = input ('Enter insurance coverage: ')

                tx_hash = bheemo.insertRecord(recordDate, birthDay, name, gender, address, city, code, description, baseCost, expense, coverage)
                #if hash is sent, successful
                #how to get recordID?

            elif choice == 2:
                ownerWallet = currentAcct
                recipientWallet = input ('Enter recipient address: ')
                recordID = int (input ('Enter record ID: '))

                valid = False
                accessCode = 0

                while valid == False:
                    try:
                        accessCode = int (input ('[1] Invoke Access Permission\n[2] Revoke Access Permission'))
                    except:
                        print('Invalid Input')

                    if accessCode == 1 or accessCode == 2:
                        valid = True

                accessID, recipientWallet, accessPermissions, keyID, privKey = bheemo.modifyRecordPermission(ownerWallet, recipientWallet, recordID, accessCode)
                #if hash is sent, successful
                print ('Modification successful.\n')
                print ('Record share\'s private key: ' + privKey)

            elif choice == 3:
                ownerWallet = currentAcct
                recordID = int (input ('Enter record ID: '))
                privKey = (input ('Enter private key (if owner, leave blank): '))


            elif choice == 4:
                notifList = bheemo.listNotification(currentAcct)

                valid = False
                view = 0

                while valid == False:
                    try:
                        view = int(input('[1] Yes\n[2] No\n Proceed to view a notification? '))
                    except:
                        print('Invalid Input')

                    if view == 1 or view == 2:
                        valid = True

                if view == 1:
                    accessID = -1
                    included = False

                    while included == False:
                        try:
                            accessID = int(input('Input access ID of notification to view: '))
                        except:
                            print('Invalid Input')

                        if accessID in notiflist:
                            included = True
                        else:
                            print('No existing notification with access ID: ' + str(accessID))

                    content = bheemo.viewNotification(accessID)
                    print("\n")
                    print('A record has been shared and access permission is granted.\n')
                    print('Access ID: {}\nRecipient: {}\nAccess Permission: {}\nKey ID: {}'.format(content[0], content[1], content[2], content[3]))

                elif view == 2:
                    print('Loop here')
                else:
                    print('Invalid input')

            elif choice == 5:
                logged = False

        except:
            print('\nInvalid Input\n')

def main ():
    bheemo.initialize()

    opt = 0
    while (opt is not 3):
        opt = int (input ('[1] Login\n[2] Register\n[3] Exit\n>> '))

        if opt is 1:
            activeUser = input ('Enter your blockchain address: ')
            #TO-DO: validation that entry is a blockchain address
            #if not validUser(activeUser): print ('Invalid address.')
            if not bheemo.checkUser(activeUser):   #if checkUser doesn't identify address in list
                print ("Log-in failed. Address not found.")
            else:
                print ('Logged successfully.\n')
                bheemo.setUser(activeUser)
                userfunc()


        elif opt is 2:
            activeUser = input ('Enter blockchain address to register: ')
            #TO-DO: validation that entry is a blockchain address
            #if not validUser(activeUser): print ('Invalid address.')
            if bheemo.checkUser(activeUser) == False:   #if checkUser sees the address in the list
                valid = False
                role = 0
                desc = ""

                while valid == False:
                    try:
                        role = int(input('[1] Doctor\n[2] Patient\n[3] Provider\nInput Role: '))
                    except:
                        print('Invalid Input')

                    if role == 1:
                        desc = 'Doctor'
                        valid = True
                    elif role == 2:
                        desc = 'Patient'
                        valid = True
                    elif role == 3:
                        desc = 'Provider'
                        valid = True

                print ('Registered successfully.\n')
                bheemo.addUser(activeUser, desc)
            else:
                print ("Log-in failed. Address is taken.")



if __name__ == '__main__':
    main()
