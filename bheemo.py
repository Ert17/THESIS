import json
from web3 import Web3
from Crypto.Cipher import AES, DES3, Blowfish
from secrets import token_bytes
from Crypto.Random import get_random_bytes
from struct import pack
import pickle as p
import random

contracts = None
web3 = None
chosenAlgorithm = 0     # Default to AES unless specified

'''
Needed Functionalities:
1. Data Pulling
2. Record retrieval
3. Encryption
4. Decryption
5. Access permission
6. Record Sharing
'''
# SAMPLE: getting a value
# print(contracts.functions.getAlgo().call())

# SAMPLE: setting a value
# tx_hash = contracts.functions.<function>(--inputs--).transact()
# web3.eth.waitForTransactionReceipt(tx_hash)

# # Call to get the instance of the smart contract for calling functions...?
# def getContract():
#     contracts = web3.eth.contract(address=address, abi=abi)
#     return contracts

# Initialize everything
def initialize():
    global contracts
    global web3
    # Setting up web3 connection with Ganache
    ganache_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]  # Assigning first account in Ganache for blockchain transactions
    ''' ---------------------------------------------------------------------------------- '''

    # Python representation of the smart contract; changes upon changing parameters, present variables(?), etc.;
    abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"}],"name":"checkUser","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessID","type":"uint256"}],"name":"createNotif","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"ownerWallet","type":"address"},{"internalType":"address","name":"recipientWallet","type":"address"},{"internalType":"uint256","name":"record_id","type":"uint256"},{"internalType":"string","name":"access_code","type":"string"}],"name":"createReq","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getAlgo","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"recordID","type":"uint256"}],"name":"getKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"get_current_acct","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"get_current_record_count","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"walletAddress","type":"address"},{"internalType":"string","name":"userRole","type":"string"}],"name":"insertUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"rDate","type":"string"},{"internalType":"string","name":"birthday","type":"string"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"_gender","type":"string"},{"internalType":"string","name":"hAddress","type":"string"},{"internalType":"string","name":"_city","type":"string"},{"internalType":"uint256","name":"code","type":"uint256"},{"internalType":"string","name":"description","type":"string"},{"internalType":"string","name":"bCost","type":"string"},{"internalType":"string","name":"_expense","type":"string"},{"internalType":"string","name":"_coverage","type":"string"}],"name":"insert_record","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessID","type":"uint256"}],"name":"invalidateKey","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessID","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"recordID","type":"uint256"}],"name":"invoke_Permission","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"record_id","type":"uint256"}],"name":"pullRecord","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"retrieve_owner","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"retrieve_permission","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"}],"name":"retrieve_user","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessID","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"recordID","type":"uint256"}],"name":"revoke_Permission","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"withAccess","type":"address"}],"name":"searchNotif","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"algo","type":"string"}],"name":"setAlgo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessID","type":"uint256"},{"internalType":"string","name":"generated_key","type":"string"}],"name":"storeKey","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"recordID","type":"uint256"}],"name":"verify_AP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')

    # Address of deployed contract in Remix
    address = web3.toChecksumAddress('0x31A70eCB69b13D8167Aa712dc64E82e4BF790460') # changes per deployment
    contracts = web3.eth.contract(address=address, abi=abi)
    chosenAlgorithm = getAlgoCode(contracts)

# Get current account
def getCurrentAcct():
    global contracts
    return contracts.functions.get_current_acct().call()

# Get chosen algorithm
def getAlgoCode(contracts):
    return contracts.functions.getAlgo().call()

# Load keys
def loadKeys():
    keys = {}
    # Loading existing key 'storage' to keys dictionary
    try:
        keys = p.load(open('app_keys/keys.rtf','rb'))
    except:
        pass

    return keys

# Save keys
def saveKeys(keys):
    p.dump(keys, open('app_keys/keys.rtf','wb'))

# Determine index of given valid address from Ganache list
def setUser(address):
    global web3
    #TO-DO: find index of given address in Ganache
    for a in range(0, len(web3.eth.accounts)):
        if web3.eth.accounts[a] == address:
            accountIndex = a

    web3.eth.defaultAccount = web3.eth.accounts[accountIndex]

# Check if address is a registered user in the program/smart contract(?)
def checkUser(address):
    global contracts
    isUser = contracts.functions.checkUser(address).call()
    return isUser

# Add a user to the program
def addUser(address, userRole):
    global contracts
    tx_hash = contracts.functions.insertUser(address, userRole).transact()

# Create and add a record to the system
def insertRecord(date, birthday, name, gender, homeAddress, city, code, desc, bCost, expense, coverage):
    global contracts
    tx_hash = contracts.functions.insert_record(date, birthday, name, gender, homeAddress, city, code, desc, bCost, expense, coverage).transact()
    recordID = contracts.functions.get_current_record_count().call()

    return recordID

# Modify record permissions and create/delete keys
def modifyRecordPermission(ownerAddress, recipientAddress, recordID, accessCode, keys):
    global contracts
    getKeyIndex = None
    if accessCode == 'N':
        getKeyIndex = contracts.functions.getKey(recipientAddress, recordID).call()

    print('\nKeys: ' + str(keys))
    print('\nOwner: ' + ownerAddress)
    print('\nRecipient: ' + recipientAddress)
    print('\nRecord ID: ' + str(recordID))
    print('\nAccess Code: ' + str(accessCode))
    reqResult = contracts.functions.createReq(str(ownerAddress), str(recipientAddress), recordID, str(accessCode)).call()
    # print(reqResult) # sample result (tuple) : [1, 1, '0x0D619E52fa0ff4EEB8e1cC9F3597c9dEb7c6B74e', 1]
    #                          Access Permission, Access ID, Recipient, Record ID

    if reqResult[0] == 0:
        print("\nAccess Permission Request Dropped.")
    elif reqResult[0] == 1:
        print("\nAccess Permission Invoked Successfully.")
        print("Access Permission created:\n")
        print("Access ID: " + str(reqResult[1]))
        print("Recipient: " + str(reqResult[2]))
        print("Record ID: " + str(reqResult[3]))
        print("Updated Access Permission: R")
    elif reqResult[0] == 2:
        print("\nAccess Permission Revoked Successfully.")
        print("Access Permission created:\n")
        print("Access ID: " + str(reqResult[1]))
        print("Recipient: " + str(reqResult[2]))
        print("Record ID: " + str(reqResult[3]))
        print("Updated Access Permission: N")
    elif reqResult[0] == 3:
        print("\nInvalid Request for Access Permission.")

    tx_hash = contracts.functions.createReq(str(ownerAddress), str(recipientAddress), recordID, str(accessCode)).transact()
    #reqResult2 = contracts.functions.createReq(str(ownerAddress), str(recipientAddress), recordID, str(accessCode)).call()
    #print('Req Result 2: ' + str(reqResult2))

    if reqResult[0] == 1: #reqResult(0) == 1
        invokeResult = contracts.functions.invoke_Permission(reqResult[1], str(reqResult[2]), reqResult[3]).transact()
        implemented = False

        if(chosenAlgorithm == 0): #AES
            # AES key generation
            AES_key = token_bytes(32)
            print ("AES Key: " + str(web3.toHex(AES_key)))
            print("Transaction Hash: " + str(web3.toHex(tx_hash)))

            while not implemented:
                keyID = random.randint(10000, 99999)
                exist = keys.get(keyID)

                if exist == None:
                    keys[str(keyID)] = AES_key
                    print("\nKey ID inserted is: " + str(keyID))
                    implemented = True
        elif(chosenAlgorithm == 1): #3DES
            # 3DES key generation
            while True:
                try:
                    TripleDES_key = DES3.adjust_key_parity(get_random_bytes(24))
                    break
                except ValueError:
                    pass

            print ("3DES Key: " + str(web3.toHex(TripleDES_key)))
            print("Transaction Hash: " + str(web3.toHex(tx_hash)))

            while not implemented:
                keyID = random.randint(10000, 99999)
                exist = keys.get(keyID)

                if exist == None:
                    keys[str(keyID)] = TripleDES_key
                    print("\nKey ID inserted is: " + str(keyID))
                    implemented = True
        elif(chosenAlgorithm == 2):
            # Blowfish key generation
            Blowfish_key = token_bytes(24)
            print("Blowfish Key: " + str(web3.toHex(Blowfish_key)))
            print("Transaction Hash: " + str(web3.toHex(tx_hash)))

            while not implemented:
                keyID = random.randint(10000, 99999)
                exist = keys.get(keyID)

                if exist == None:
                    keys[str(keyID)] = Blowfish_key
                    print("\nKey ID inserted is: " + str(keyID))
                    implemented = True

        print(reqResult)
        accessID = reqResult[1]

        print ('\nnew accessID: ' + str(accessID))
        print("new Key ID: " + str(keyID) + '\n')

        contracts.functions.storeKey(int(accessID), str(keyID)).transact()

        notif = contracts.functions.createNotif(accessID).call()
        reply = []
        reply.append(notif[0])
        reply.append(notif[1])
        reply.append(notif[2])
        reply.append(notif[3])
        reply.append(keyID)
        reply.append(keys[str(keyID)])

        saveKeys(keys)

        return reply

        #print("Transaction Hash: " + str(web3.toHex(keyStoreResult)))        # Debugging
        #print("(Checking purpose only): \nAll current keys: " + str(keys))   # Debugging

    elif reqResult[0] == 2:
        # remove from key storage
        #print("Key index to be popped: " + str(getKeyIndex))               # Debugging
        #print("Key to delete: " + str(keys[getKeyIndex]))                  # Debugging
        del keys[str(getKeyIndex)];

        # remove key validity from latest invoked smart contract
        revokeResult = contracts.functions.revoke_Permission(reqResult[1], str(reqResult[2]), reqResult[3]).transact()
        print(web3.toHex(revokeResult))
        # Debugging: print
        print("(Checking purpose only): \nRemaining keys after removing and invalidating specified key: " + str(keys))
        
        accessID = reqResult[1]

        notif = contracts.functions.createNotif(accessID).call()
        reply = []
        reply.append(notif[0])
        reply.append(notif[1])
        reply.append(notif[2])
        reply.append(notif[3])

        saveKeys(keys)

        return reply

# Retrieve a record for a recipient
def recipientRetrieve(address, keys, privateKey, recordID):
    global contracts
    #try:
    #    recordID = int(input("\nInput recordID to retrieve: "))
    #except:
    #    print("Invalid input.\n")
        # continue

    verified = contracts.functions.verify_AP(recordID).call()
    print("\nAccess Permission Value: " + str(verified))
    #0 1 2

    if verified == 0: # if user has no permission to access record
        return "Invalid Request"
    elif verified == 2:
        record = contracts.functions.pullRecord(recordID).call()
        record_values = str(record[0]) + "\n" + str(record[0]) + "\n" + str(record[1]) + "\n" + str(record[2]) + "\n" + str(record[3]) + "\n" + str(record[4]) + "\n" + str(record[5]) + "\n" + str(record[6])
        encoded_record = record_values.encode("windows-1252").strip()
        record_byte = bytes(encoded_record)
        #print(record_byte)                                     # Debugging
        keyID = contracts.functions.getKey(address, recordID).call()
        key = keys.get(keyID)

        # Encrypt Record
        if(chosenAlgorithm == 0): #AES
            cipher1 = AES.new(key, AES.MODE_EAX)
            nonce = cipher1.nonce
            #print("Record before encryption: " + str(Record))    # Debugging
            encrypt_record = cipher1.encrypt(record_byte)
            print("\nEncrypted record: " + str(encrypt_record) + '\n')

        elif(chosenAlgorithm == 1): #3DES
            cipher1 = DES3.new(key, DES3.MODE_CFB)
            #nonce = cipher1.nonce
            #print("Record before encryption: " + str(Record))    # Debugging
            encrypt_record = cipher1.iv + cipher1.encrypt(record_byte)
            print("\nEncrypted record: " + str(encrypt_record) + '\n')

        elif(chosenAlgorithm == 2): #Blowfish
            cipher1 = Blowfish.new(key, Blowfish.MODE_CBC)
            #nonce = cipher1.nonce

            block_size = 24
            plen = block_size - len(record_byte) % block_size
            padding = [plen]*plen
            padding = pack('b'*plen, *padding)

            #print("Record before encryption: " + str(Record))    # debugging
            encrypt_record = cipher1.iv + cipher1.encrypt(record_byte + padding)
            print("\nEncrypted record: " + str(encrypt_record) + '\n')

        keyIndex = contracts.functions.getKey(address, recordID).call()
        decrypt_key_checker = keys.get(keyIndex)

        try:
            decrypt_key = privateKey
            #decrypt_bytes = str("b\'") + decrypt_key + str("\'")

            # Check if user provided key is same sa one in key storage
            if str(decrypt_key_checker) == str(decrypt_key):
                if(chosenAlgorithm == 0): #AES
                    cipher2 = AES.new(decrypt_key_checker, AES.MODE_EAX, nonce=nonce)
                    decrypted_data = cipher2.decrypt(encrypt_record)
                    # print ("/nDecrypted data: " + str(decrypted_data))
                elif(chosenAlgorithm == 1): #3DES
                    cipher2 = DES3.new(decrypt_key_checker, DES3.MODE_CFB)
                    decrypted_data = cipher2.decrypt(encrypt_record)
                    # print ("/nDecrypted data: " + str(decrypted_data))
                elif(chosenAlgorithm == 2): #Blowfish
                    cipher2 = Blowfish.new(decrypt_key_checker, Blowfish.MODE_CBC)
                    decrypted_data = cipher2.decrypt(encrypt_record)
                    # print ("/nDecrypted data: " + str(decrypted_data))

                dec_data = decrypted_data.decode("windows-1252")
                #print(dec_data)
                finalRecord = dec_data.split('\n')

                return finalRecord
            else:
                print("Invalid key: The record you requested cannot be decrypted.") #return na din ba ito?
        except:
            print("Oops something went wrong. Possible decryption failure.\n") #return na din ba ito?

# Retrieve a record for owner
def retrieveRecord(address, recordID): #added address
    global contracts
    #try:
    #    recordID = int(input("\nInput recordID to retrieve: "))
    #except:
    #    print("Invalid input.\n")


    verified = contracts.functions.verify_AP(recordID).call()
    print("\nAccess Permission Value: " + str(verified))    #Debugging

    if verified == 0: # if user has no permission to access record
        return "Invalid Request"
    elif verified == 1: # if OWNER of record
        record = contracts.functions.pullRecord(recordID).call()
        return record #i-format pa ba muna dapat like record[0], record[1]?

# Get all notifications
def listCurrentPermissions(address):
    global contracts
    notifList = contracts.functions.searchNotif(address).call()

    print("\nAccess IDs for this user:\n")

    approved = []
    latest = []

    for notif in notifList: #[accessIDs]
        access = contracts.functions.retrieve_permission(notif).call()
        #[permission.accessID, permission.recipient, permission.recordID, permission.access, permission.key]

        if access[2] not in latest:
            latest.append(access[2])
            
            if access[3] == 'R':
            	approved.append([access[0],access[2],access[4]])
                             	#accessID, recordID, key
    return approved

# # View all notifications
# def viewNotification(accessID):
#     global contracts
#     notif = contracts.functions.createNotif(accessID).call()
#
#     notifList = []
#     notifList.append(notif[0])
#     notifList.append(notif[1])
#     notifList.append(notif[2])
#     notifList.append(notif[3])
#
#     return notifList
