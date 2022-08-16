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

def userfunc(keys):
    logged = True

    currentAcct = bheemo.getCurrentAcct()
    while (logged):
        print('[1] Create a Record\n[2] Modify Record Permission\n[3] Retrieve a Record\n[4] View Current Permissions\n[5] Logout\n\n')
        #try:
        choice = int(input('Input Action: '))

        if choice == 1:
            recordDate = input ('Enter record date (MM/DD/YYYY): ')
            birthDay = input ('Enter birthday (MM/DD/YYYY): ')
            name = input ('Enter name: ')
            gender = input ('Enter gender: ')
            address = input ('Enter home address: ')
            city = input ('Enter city: ')
            code = int (input ('Enter vaccine code: '))
            description = input ('Enter vaccine description: ')
            baseCost = input ('Enter vaccine base cost: ')
            expense = input ('Enter total expense: ')
            coverage = input ('Enter insurance coverage: ')


            try:
                inserted = bheemo.insertRecord(recordDate, birthDay, name, gender, address, city, code, description, baseCost, expense, coverage)
                print("\nRecord Successfully Added!\nRecord ID: " + str(inserted) + "\n")
            except:
                print("\nAddition of Record Unsuccesful :(\n")
            #if hash is sent, successful
            #how to get recordID?

        elif choice == 2:
            ownerWallet = currentAcct
            recipientWallet = input ('Enter recipient address: ')
            recordID = int (input ('Enter record ID: '))

            valid = False
            accessCode = 0
            permission = ''

            while valid == False:
                try:
                    accessCode = int (input ('[1] Invoke Access Permission\n[2] Revoke Access Permission\nInput: '))
                    if accessCode == 1:
                        permission = 'R'
                        valid = True
                    elif accessCode == 2:
                        permission = 'N'
                        valid = True
                except:
                    print('Invalid Input sa accessCode')

            reqResult = bheemo.modifyRecordPermission(ownerWallet, recipientWallet, recordID, permission, keys)
            #reqResult is an array
            # if invoke, 6 laman ni reqResult
            # if revoke, 4 laman ni reqResult

            print ('Modification successful.\n')

            if permission == 'R':
                print ('Key ID: ' + str(reqResult[4]))

            bheemo.loadKeys()


        elif choice == 3:
            ownerWallet = currentAcct #user
            recordID = int (input ('Enter record ID: '))

            isOwner = bheemo.checkOwner(recordID)

            if isOwner == 1: #owner
                record = bheemo.retrieveRecord(ownerWallet, recordID)
            else:
                privKey = (input ('Enter private key: '))
                record = bheemo.recipientRetrieve(ownerWallet, keys, privKey, recordID)

            print(record)


        elif choice == 4:
            notifList = bheemo.listCurrentPermissions(currentAcct)
            print("\nNOTIFS TO")
            #print(notifList)

            for notif in notifList:
            	print('Access ID: {}\nRecord ID: {}\nKey ID: {}\n'.format(notif[0], notif[1], notif[2]))

        elif choice == 5:
            logged = False

        #except:
        #    print('\nInvalid Input sa outerest\n')

def main ():
    bheemo.initialize()
    keys = bheemo.loadKeys()
    print(keys)

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
                userfunc(keys)


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
