// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.0 <0.9.0;

contract EHR{

    uint recordCtr = 0;
    uint accessCtr = 0;
    uint ownerCtr = 0;
    uint userCtr = 0;

    // algorithm set to AES as defualt
    string algorithm = "AES"; // 0 -> AES; 1 -> 3DES; 2 -> Twofish/Blowfish

    //patient record EHR
    struct Record {
        uint record_id;
        string record_date;
        address patient_id;
        string birth_date;
        string patient_name; // FIRST NAME|MAIDEN NAME|LAST NAME|SUFFIX
        //string last_name;
        //string suffix;
        //string maiden_name;
        //string marital_status;
        string gender;
        string home_address;
        string city;
        //string ssn;
        uint vaccine_code_num;
        string desc;
        string base_cost;
        string expense;
        string coverage;
    }

    struct Permission {
        uint accessID;
        address recipient;
        uint recordID;
        string access; // "O" - Owner; "R" - Read; "N" - No Access
        string key;
    }

    // user accounts
    struct User {
        address myAddress;
        string role;
    }

    // record id used as primary key
    mapping(uint => Record) records;

    // access permissions
    Permission[] owners;
    Permission[] permissions;

    // wallet address used as primary key
    mapping(address => User) users;

    constructor() public{
        initialize();
    }

    function initialize() internal {
        owners.push(Permission(accessCtr, 0x0000000000000000000000000000000000000000, recordCtr, "", ""));
        permissions.push(Permission(accessCtr, 0x0000000000000000000000000000000000000000, recordCtr, "", ""));
    }

    function setAlgo(string memory algo) public {
      algorithm = algo;
    }

    //function for pushing records
    function insert_record(string memory rDate, string memory birthday, string memory name, string memory _gender, string memory  hAddress, string memory _city,
    uint code, string memory description, string memory bCost, string memory _expense, string memory _coverage) public {

        bool isUser = checkUser(msg.sender);

        // if the provided address is an existing user
        if(isUser == true) {

            // Generate record ID for added EHRi
            recordCtr += 1;

            // Create instance of record with record id as identifier/primary key
            Record storage record = records[recordCtr];

            // Set values of the record instance
            record.record_id = recordCtr;
            record.record_date = rDate;
            record.patient_id = msg.sender;
            record.birth_date = birthday;
            record.patient_name = name;
            //record.last_name = lName;
            //record.suffix = sName;
            //record.maiden_name = mName;
            //record.marital_status = mStatus;
            record.gender = _gender;
            record.home_address = hAddress;
            record.city = _city;
            //record.ssn = ssNum;
            record.vaccine_code_num = code;
            record.desc = description;
            record.base_cost = bCost;
            record.expense = _expense;
            record.coverage = _coverage;

            // Initialize access permission for added record
            createOwner(msg.sender, recordCtr, "");
        }
    }

    // function for pushing owner access permissions for
    function createOwner(address walletAddress, uint record_id, string memory key) internal {

        // Initialize access id for added access permissions as owner
        ownerCtr += 1;

        // Create access permission for added records
        owners.push(Permission(ownerCtr, walletAddress, record_id, "O", key));
    }

    // function to check if users wallet exists as user
    function checkUser(address userAddress) internal view returns(bool) {

        if(users[userAddress].myAddress == 0x0000000000000000000000000000000000000000) {
            return false;
        }
        else {
            return true;
        }
    }

    // function to locate the latest access permission instance using the recipient address and record ID
    function get_OAP_index(address recipientAddress, uint record_id) internal view returns (int256){

        int256 latest = -1;

        // traverse from last element in permissions
        for(uint i = permissions.length-1; i > 0; i--) {

            //find the latest instance of an access permission given a recipient address and record id
            if(permissions[i].recipient == recipientAddress && permissions[i].recordID == record_id) {
                latest = int256(i);
                return latest;
            }
        }

        return latest;
    }

    // function to locate the latest owner access permission instance using the recipient address and record ID
    function verifyOwner(address recipientAddress, uint record_id) internal view returns (bool){

        bool verifiedOwner = false;

        // traverse from last element in permissions
        for(uint i = owners.length-1; i > 0; i--) {

            //find the latest instance of an access permission given a recipient address and record id
            if(owners[i].recipient == recipientAddress && owners[i].recordID == record_id) {
                verifiedOwner = true;
            }
        }

        // returns false if not an owner
        return verifiedOwner;
    }

    function storeKey(uint accessID, string memory generated_key) public {


        // retrieve record for key generation using record id provided
        // use provided algorithm to generate key for the specified record

        // store key
        permissions[accessID].key = generated_key;

        // return generated key here
        //return "key eto";
    }

    function invalidateKey(uint accessID) public {


        // retrieve record for key generation using record id provided
        // use provided algorithm to generate key for the specified record

        // store key
        permissions[accessID].key = "";

        // return generated key here
        //return "key eto";
    }

    function invoke_Permission(uint accessID, address recipient, uint recordID) public {

        // generate key here
        //string memory generated_key = generateKey(algorithm, request.recordID);

        // invoke by pushing request as updated/latest access permission ++ include generated key in this push
        permissions.push(Permission(accessID, recipient, recordID, "R", ""));
    }

    function revoke_Permission(uint accessID, address recipient, uint recordID) public {

        // invalidate key here
        uint invalidate_index = uint(get_OAP_index(recipient, recordID));
        invalidateKey(invalidate_index);
        // remove from key storage

        // revoke by pushing request as updated/latest access permission with "N"  ++ no key
        permissions.push(Permission(accessID, recipient, recordID, "N", ""));
    }

    // Function that accepts and evaluates the original access permission to whether to invoke, revoke, or drop the request
    function accept_OAP(int256 OAP_index, Permission memory request) internal returns (uint, uint, address, uint){

        if(OAP_index == -1) { // no existing access permission yet

            return (1, request.accessID, request.recipient, request.recordID); //invoke_Permission(request); // return 1

        }
        // with existing access permission

        Permission memory OAP = permissions[uint(OAP_index)];

        // if same access change to the original access permission, drop request and decrease accessCtr by 1
        if(keccak256(abi.encodePacked(OAP.access)) == keccak256(abi.encodePacked(request.access))) {
            // do nothing; drop the request
            accessCtr -= 1;
            return (0, 0, 0x0000000000000000000000000000000000000000, 0);
        }
        // if different access change to the latest access permission, push the request as a new permission

        if(keccak256(abi.encodePacked(request.access)) == keccak256(abi.encodePacked("R"))) {
            return (1, request.accessID, request.recipient, request.recordID);//invoke_Permission(request);
        }
        else if(keccak256(abi.encodePacked(request.access)) == keccak256(abi.encodePacked("N"))) {
            return (2, request.accessID, request.recipient, request.recordID);//revoke_Permission(request);
        }

        return (3, 0, 0x0000000000000000000000000000000000000000, 0);
    }

    // function that creates a change of access permission request once ownership is verified
    function createReq(address ownerWallet, address recipientWallet, uint record_id, string memory access_code) public returns (uint, uint, address, uint){

        bool isUser = checkUser(recipientWallet);

        // msg.sender pertaining to account currently calling the function
        if(verifyOwner(ownerWallet, record_id)) { // if requestor is owner

            if(isUser == true) { // if recipient is registered as user

                // Format request for change of access permission containing the access ID, recipient address, updated access permission, and key
                accessCtr += 1;
                Permission memory request = Permission(accessCtr, recipientWallet, record_id, access_code, "");

                // Locate the original access permission using the recipient address and record ID
                int256 OAP_index = get_OAP_index(recipientWallet, record_id);

                // Forward the original access permission to the Permission Modifier Submodule as well as the change of access permission request
                return accept_OAP(OAP_index, request);

            }
        }

        // If unsuccessful create request
        return (0, 0, 0x0000000000000000000000000000000000000000, 0);
    }

    //function for pushing users
    function insertUser(address walletAddress, string memory userRole) public {

        // Create instance of user with wallet address as identifier/perimary key
        User storage user = users[walletAddress];

        // Set values of the user instance
        user.myAddress = walletAddress;
        user.role = userRole;

    }

    function retrieve_record(uint record_id) public view returns
    (uint, string memory, address, string memory, string memory, uint, string memory) {
        Record storage record = records[record_id];
        /*
        string memory splitName = record.patient_name;
        string memory cut = "|";
        string[4] memory separatedName;

        separatedName.push(splitName.split(cut).toString());
        separatedName.push(splitName.split(cut).toString());
        separatedName.push(splitName.split(cut).toString());
        separatedName.push(splitName.split(cut).toString());
        */

        return (record.record_id, record.record_date, record.patient_id, record.patient_name, record.gender, record.vaccine_code_num, record.desc);
    }

    function retrieve_permission(uint index) public view returns (uint, address, uint, string memory, string memory) {
        Permission storage permission = permissions[index];

        return (permission.accessID, permission.recipient, permission.recordID, permission.access, permission.key);
    }

    function retrieve_owner(uint index) public view returns (uint, address, uint, string memory, string memory) {
        Permission storage owner = owners[index];

        return (owner.accessID, owner.recipient, owner.recordID, owner.access, owner.key);
    }

    function retrieve_user(address userAddress) public view returns (address, string memory) {
        User storage user = users[userAddress];

        return (user.myAddress, user.role);
    }

    function getAlgo() public view returns (string memory) {

        return algorithm;
    }

    function getKey(address recipient, uint recordID) public view returns (string memory) {

        uint index = uint(get_OAP_index(recipient, recordID));

        return permissions[index].key;
    }

    function get_current_acct() public view returns (address) {

        return msg.sender;
    }

}
