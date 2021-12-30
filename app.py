'''
Variables to change per deployment:
1) ABI      2) bytecode (for deploy)        3) ChecksumAddress (if Remix-deployed)
'''

import json
from web3 import Web3

from Crypto.Cipher import AES, DES3, Blowfish
from secrets import token_bytes
from Crypto.Random import get_random_bytes
import pickle as p
import random

''' =============================== WEB3 <-----------> GANACHE =============================== '''
# Setting up web3 connection with Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# ''' Temporary log-in for assigning a specified account for transaction (User session?) '''
# # temp default account for signing transactions?
# for a in range(0, len(web3.eth.accounts)):
#     print(str(a) + ": " + str(web3.eth.accounts[a]))
#
# accountIndex = int(input("Which account to use: "))
# web3.eth.defaultAccount = web3.eth.accounts[accountIndex]
web3.eth.defaultAccount = web3.eth.accounts[0]
''' ---------------------------------------------------------------------------------- '''

# Python representation of the smart contract; changes upon changing parameters, present variables(?), etc.;
abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"recordID","type":"uint256"}],"name":"createNotif","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"ownerWallet","type":"address"},{"internalType":"address","name":"recipientWallet","type":"address"},{"internalType":"uint256","name":"record_id","type":"uint256"},{"internalType":"string","name":"access_code","type":"string"}],"name":"createReq","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getAlgo","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"recordID","type":"uint256"}],"name":"getKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"get_current_acct","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"walletAddress","type":"address"},{"internalType":"string","name":"userRole","type":"string"}],"name":"insertUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"rDate","type":"string"},{"internalType":"string","name":"birthday","type":"string"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"_gender","type":"string"},{"internalType":"string","name":"hAddress","type":"string"},{"internalType":"string","name":"_city","type":"string"},{"internalType":"uint256","name":"code","type":"uint256"},{"internalType":"string","name":"description","type":"string"},{"internalType":"string","name":"bCost","type":"string"},{"internalType":"string","name":"_expense","type":"string"},{"internalType":"string","name":"_coverage","type":"string"}],"name":"insert_record","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessID","type":"uint256"}],"name":"invalidateKey","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessID","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"recordID","type":"uint256"}],"name":"invoke_Permission","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"record_id","type":"uint256"}],"name":"pullRecord","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"retrieve_owner","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"retrieve_permission","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"}],"name":"retrieve_user","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessID","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"recordID","type":"uint256"}],"name":"revoke_Permission","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"algo","type":"string"}],"name":"setAlgo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"accessID","type":"uint256"},{"internalType":"string","name":"generated_key","type":"string"}],"name":"storeKey","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"currentAcct","type":"address"},{"internalType":"uint256","name":"recordID","type":"uint256"}],"name":"verify_AP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')

# Address of deployed contract in Remix
address = web3.toChecksumAddress('0xA969484a2731607C3bc6c29a03cC177A5340B0F8') # changes per deployment

# bytecode changes for every deployment
# bytecode='608060405234801561001057600080fd5b50600436106101005760003560e01c8063969a2b3911610097578063bb5b27e111610066578063bb5b27e1146102a6578063d2fdcec4146102d6578063e0a2042d146102f4578063f88289d11461031057610100565b8063969a2b391461021d5780639ad44dac14610239578063b0b07f1f1461026c578063b113afc21461028857610100565b80638129fc1c116100d35780638129fc1c1461018d57806389aaeeaf146101975780638d3ba5ae146101b35780639333cb5e146101e957610100565b80630764da1d1461010557806326fdbb6f14610121578063708121b01461013d5780637262bfe214610159575b600080fd5b61011f600480360381019061011a9190611e32565b610341565b005b61013b60048036038101906101369190612087565b61035b565b005b61015760048036038101906101529190611e7b565b6103a7565b005b610173600480360381019061016e9190612087565b61056f565b6040516101849594939291906122df565b60405180910390f35b610195610700565b005b6101b160048036038101906101ac91906120b4565b610946565b005b6101cd60048036038101906101c89190612087565b610aa6565b6040516101e09796959493929190612340565b60405180910390f35b61020360048036038101906101fe9190612087565b610d53565b6040516102149594939291906122df565b60405180910390f35b61023760048036038101906102329190611dd6565b610ee4565b005b610253600480360381019061024e9190611d53565b610f88565b60405161026394939291906123cb565b60405180910390f35b61028660048036038101906102819190612107565b611066565b005b6102906110a4565b60405161029d91906122bd565b60405180910390f35b6102c060048036038101906102bb9190612087565b611136565b6040516102cd91906122bd565b60405180910390f35b6102de6111ed565b6040516102eb9190612272565b60405180910390f35b61030e600480360381019061030991906120b4565b6111f5565b005b61032a60048036038101906103259190611d26565b61133d565b60405161033892919061228d565b60405180910390f35b8060049080519060200190610357929190611be9565b5050565b604051806020016040528060008152506007828154811061037f5761037e612680565b5b906000526020600020906005020160040190805190602001906103a3929190611be9565b5050565b60006103b233611443565b90506001151581151514156105615760016000808282546103d3919061248d565b9250508190555060006005600080548152602001908152602001600020905060005481600001819055508c816001019080519060200190610415929190611be9565b50338160020160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508b816003019080519060200190610471929190611be9565b508a81600401908051906020019061048a929190611be9565b50898160050190805190602001906104a3929190611be9565b50888160060190805190602001906104bc929190611be9565b50878160070190805190602001906104d5929190611be9565b50868160080181905550858160090190805190602001906104f7929190611be9565b508481600a019080519060200190610510929190611be9565b508381600b019080519060200190610529929190611be9565b508281600c019080519060200190610542929190611be9565b5061055f33600054604051806020016040528060008152506114ee565b505b505050505050505050505050565b600080600060608060006007878154811061058d5761058c612680565b5b9060005260206000209060050201905080600001548160010160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16826002015483600301846004018180546105e0906125bf565b80601f016020809104026020016040519081016040528092919081815260200182805461060c906125bf565b80156106595780601f1061062e57610100808354040283529160200191610659565b820191906000526020600020905b81548152906001019060200180831161063c57829003601f168201915b5050505050915080805461066c906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054610698906125bf565b80156106e55780601f106106ba576101008083540402835291602001916106e5565b820191906000526020600020905b8154815290600101906020018083116106c857829003601f168201915b50505050509050955095509550955095505091939590929450565b60066040518060a001604052806001548152602001600073ffffffffffffffffffffffffffffffffffffffff16815260200160005481526020016040518060200160405280600081525081526020016040518060200160405280600081525081525090806001815401808255809150506001900390600052602060002090600502016000909190919091506000820151816000015560208201518160010160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550604082015181600201556060820151816003019080519060200190610802929190611be9565b50608082015181600401908051906020019061081f929190611be9565b50505060076040518060a001604052806001548152602001600073ffffffffffffffffffffffffffffffffffffffff16815260200160005481526020016040518060200160405280600081525081526020016040518060200160405280600081525081525090806001815401808255809150506001900390600052602060002090600502016000909190919091506000820151816000015560208201518160010160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550604082015181600201556060820151816003019080519060200190610924929190611be9565b506080820151816004019080519060200190610941929190611be9565b505050565b60006109528383611643565b905061095d8161035b565b60076040518060a001604052808681526020018573ffffffffffffffffffffffffffffffffffffffff1681526020018481526020016040518060400160405280600181526020017f4e0000000000000000000000000000000000000000000000000000000000000081525081526020016040518060200160405280600081525081525090806001815401808255809150506001900390600052602060002090600502016000909190919091506000820151816000015560208201518160010160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550604082015181600201556060820151816003019080519060200190610a80929190611be9565b506080820151816004019080519060200190610a9d929190611be9565b50505050505050565b600060606000606080600060606000600560008a815260200190815260200160002090508060000154816001018260020160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff168360040184600501856008015486600901858054610b15906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054610b41906125bf565b8015610b8e5780601f10610b6357610100808354040283529160200191610b8e565b820191906000526020600020905b815481529060010190602001808311610b7157829003601f168201915b50505050509550838054610ba1906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054610bcd906125bf565b8015610c1a5780601f10610bef57610100808354040283529160200191610c1a565b820191906000526020600020905b815481529060010190602001808311610bfd57829003601f168201915b50505050509350828054610c2d906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054610c59906125bf565b8015610ca65780601f10610c7b57610100808354040283529160200191610ca6565b820191906000526020600020905b815481529060010190602001808311610c8957829003601f168201915b50505050509250808054610cb9906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054610ce5906125bf565b8015610d325780601f10610d0757610100808354040283529160200191610d32565b820191906000526020600020905b815481529060010190602001808311610d1557829003601f168201915b50505050509050975097509750975097509750975050919395979092949650565b6000806000606080600060068781548110610d7157610d70612680565b5b9060005260206000209060050201905080600001548160010160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1682600201548360030184600401818054610dc4906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054610df0906125bf565b8015610e3d5780601f10610e1257610100808354040283529160200191610e3d565b820191906000526020600020905b815481529060010190602001808311610e2057829003601f168201915b50505050509150808054610e50906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054610e7c906125bf565b8015610ec95780601f10610e9e57610100808354040283529160200191610ec9565b820191906000526020600020905b815481529060010190602001808311610eac57829003601f168201915b50505050509050955095509550955095505091939590929450565b6000600860008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000209050828160000160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555081816001019080519060200190610f82929190611be9565b50505050565b6000806000806000610f9988611443565b9050610fa5898861175e565b1561104b5760011515811515141561104a576001806000828254610fc9919061248d565b9250508190555060006040518060a0016040528060015481526020018a73ffffffffffffffffffffffffffffffffffffffff168152602001898152602001888152602001604051806020016040528060008152508152509050600061102e8a8a611643565b905061103a8183611851565b965096509650965050505061105b565b5b6000806000809450945094509450505b945094509450949050565b806007838154811061107b5761107a612680565b5b9060005260206000209060050201600401908051906020019061109f929190611be9565b505050565b6060600480546110b3906125bf565b80601f01602080910402602001604051908101604052809291908181526020018280546110df906125bf565b801561112c5780601f106111015761010080835404028352916020019161112c565b820191906000526020600020905b81548152906001019060200180831161110f57829003601f168201915b5050505050905090565b60606007828154811061114c5761114b612680565b5b90600052602060002090600502016004018054611168906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054611194906125bf565b80156111e15780601f106111b6576101008083540402835291602001916111e1565b820191906000526020600020905b8154815290600101906020018083116111c457829003601f168201915b50505050509050919050565b600033905090565b60076040518060a001604052808581526020018473ffffffffffffffffffffffffffffffffffffffff1681526020018381526020016040518060400160405280600181526020017f520000000000000000000000000000000000000000000000000000000000000081525081526020016040518060200160405280600081525081525090806001815401808255809150506001900390600052602060002090600502016000909190919091506000820151816000015560208201518160010160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550604082015181600201556060820151816003019080519060200190611318929190611be9565b506080820151816004019080519060200190611335929190611be9565b505050505050565b600060606000600860008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002090508060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16816001018080546113b9906125bf565b80601f01602080910402602001604051908101604052809291908181526020018280546113e5906125bf565b80156114325780601f1061140757610100808354040283529160200191611432565b820191906000526020600020905b81548152906001019060200180831161141557829003601f168201915b505050505090509250925050915091565b60008073ffffffffffffffffffffffffffffffffffffffff16600860008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614156114e457600090506114e9565b600190505b919050565b600160026000828254611501919061248d565b9250508190555060066040518060a0016040528060025481526020018573ffffffffffffffffffffffffffffffffffffffff1681526020018481526020016040518060400160405280600181526020017f4f0000000000000000000000000000000000000000000000000000000000000081525081526020018381525090806001815401808255809150506001900390600052602060002090600502016000909190919091506000820151816000015560208201518160010160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060408201518160020155606082015181600301908051906020019061161e929190611be9565b50608082015181600401908051906020019061163b929190611be9565b505050505050565b6000807fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff90506000600160078054905061167d91906124e3565b90505b6000811115611752578473ffffffffffffffffffffffffffffffffffffffff16600782815481106116b4576116b3612680565b5b906000526020600020906005020160010160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614801561172d5750836007828154811061171957611718612680565b5b906000526020600020906005020160020154145b1561173f578091508192505050611758565b808061174a90612595565b915050611680565b50809150505b92915050565b600080600090506000600160068054905061177991906124e3565b90505b6000811115611846578473ffffffffffffffffffffffffffffffffffffffff16600682815481106117b0576117af612680565b5b906000526020600020906005020160010160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff161480156118295750836006828154811061181557611814612680565b5b906000526020600020906005020160020154145b1561183357600191505b808061183e90612595565b91505061177c565b508091505092915050565b6000806000807fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff86141561189d5760018560000151866020015187604001519350935093509350611be0565b6000600787815481106118b3576118b2612680565b5b90600052602060002090600502016040518060a0016040529081600082015481526020016001820160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200160028201548152602001600382018054611946906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054611972906125bf565b80156119bf5780601f10611994576101008083540402835291602001916119bf565b820191906000526020600020905b8154815290600101906020018083116119a257829003601f168201915b505050505081526020016004820180546119d8906125bf565b80601f0160208091040260200160405190810160405280929190818152602001828054611a04906125bf565b8015611a515780601f10611a2657610100808354040283529160200191611a51565b820191906000526020600020905b815481529060010190602001808311611a3457829003601f168201915b50505050508152505090508560600151604051602001611a719190612231565b604051602081830303815290604052805190602001208160600151604051602001611a9c9190612231565b604051602081830303815290604052805190602001201415611ae5576001806000828254611aca91906124e3565b92505081905550600080600080945094509450945050611be0565b604051602001611af49061225d565b604051602081830303815290604052805190602001208660600151604051602001611b1f9190612231565b604051602081830303815290604052805190602001201415611b5a576001866000015187602001518860400151945094509450945050611be0565b604051602001611b6990612248565b604051602081830303815290604052805190602001208660600151604051602001611b949190612231565b604051602081830303815290604052805190602001201415611bcf576002866000015187602001518860400151945094509450945050611be0565b600360008060009450945094509450505b92959194509250565b828054611bf5906125bf565b90600052602060002090601f016020900481019282611c175760008555611c5e565b82601f10611c3057805160ff1916838001178555611c5e565b82800160010185558215611c5e579182015b82811115611c5d578251825591602001919060010190611c42565b5b509050611c6b9190611c6f565b5090565b5b80821115611c88576000816000905550600101611c70565b5090565b6000611c9f611c9a84612435565b612410565b905082815260208101848484011115611cbb57611cba6126e3565b5b611cc6848285612553565b509392505050565b600081359050611cdd81612755565b92915050565b600082601f830112611cf857611cf76126de565b5b8135611d08848260208601611c8c565b91505092915050565b600081359050611d208161276c565b92915050565b600060208284031215611d3c57611d3b6126ed565b5b6000611d4a84828501611cce565b91505092915050565b60008060008060808587031215611d6d57611d6c6126ed565b5b6000611d7b87828801611cce565b9450506020611d8c87828801611cce565b9350506040611d9d87828801611d11565b925050606085013567ffffffffffffffff811115611dbe57611dbd6126e8565b5b611dca87828801611ce3565b91505092959194509250565b60008060408385031215611ded57611dec6126ed565b5b6000611dfb85828601611cce565b925050602083013567ffffffffffffffff811115611e1c57611e1b6126e8565b5b611e2885828601611ce3565b9150509250929050565b600060208284031215611e4857611e476126ed565b5b600082013567ffffffffffffffff811115611e6657611e656126e8565b5b611e7284828501611ce3565b91505092915050565b60008060008060008060008060008060006101608c8e031215611ea157611ea06126ed565b5b60008c013567ffffffffffffffff811115611ebf57611ebe6126e8565b5b611ecb8e828f01611ce3565b9b505060208c013567ffffffffffffffff811115611eec57611eeb6126e8565b5b611ef88e828f01611ce3565b9a505060408c013567ffffffffffffffff811115611f1957611f186126e8565b5b611f258e828f01611ce3565b99505060608c013567ffffffffffffffff811115611f4657611f456126e8565b5b611f528e828f01611ce3565b98505060808c013567ffffffffffffffff811115611f7357611f726126e8565b5b611f7f8e828f01611ce3565b97505060a08c013567ffffffffffffffff811115611fa057611f9f6126e8565b5b611fac8e828f01611ce3565b96505060c0611fbd8e828f01611d11565b95505060e08c013567ffffffffffffffff811115611fde57611fdd6126e8565b5b611fea8e828f01611ce3565b9450506101008c013567ffffffffffffffff81111561200c5761200b6126e8565b5b6120188e828f01611ce3565b9350506101208c013567ffffffffffffffff81111561203a576120396126e8565b5b6120468e828f01611ce3565b9250506101408c013567ffffffffffffffff811115612068576120676126e8565b5b6120748e828f01611ce3565b9150509295989b509295989b9093969950565b60006020828403121561209d5761209c6126ed565b5b60006120ab84828501611d11565b91505092915050565b6000806000606084860312156120cd576120cc6126ed565b5b60006120db86828701611d11565b93505060206120ec86828701611cce565b92505060406120fd86828701611d11565b9150509250925092565b6000806040838503121561211e5761211d6126ed565b5b600061212c85828601611d11565b925050602083013567ffffffffffffffff81111561214d5761214c6126e8565b5b61215985828601611ce3565b9150509250929050565b61216c81612517565b82525050565b600061217d82612466565b6121878185612471565b9350612197818560208601612562565b6121a0816126f2565b840191505092915050565b60006121b682612466565b6121c08185612482565b93506121d0818560208601612562565b80840191505092915050565b60006121e9600183612482565b91506121f482612703565b600182019050919050565b600061220c600183612482565b91506122178261272c565b600182019050919050565b61222b81612549565b82525050565b600061223d82846121ab565b915081905092915050565b6000612253826121dc565b9150819050919050565b6000612268826121ff565b9150819050919050565b60006020820190506122876000830184612163565b92915050565b60006040820190506122a26000830185612163565b81810360208301526122b48184612172565b90509392505050565b600060208201905081810360008301526122d78184612172565b905092915050565b600060a0820190506122f46000830188612222565b6123016020830187612163565b61230e6040830186612222565b81810360608301526123208185612172565b905081810360808301526123348184612172565b90509695505050505050565b600060e082019050612355600083018a612222565b81810360208301526123678189612172565b90506123766040830188612163565b81810360608301526123888187612172565b9050818103608083015261239c8186612172565b90506123ab60a0830185612222565b81810360c08301526123bd8184612172565b905098975050505050505050565b60006080820190506123e06000830187612222565b6123ed6020830186612222565b6123fa6040830185612163565b6124076060830184612222565b95945050505050565b600061241a61242b565b905061242682826125f1565b919050565b6000604051905090565b600067ffffffffffffffff8211156124505761244f6126af565b5b612459826126f2565b9050602081019050919050565b600081519050919050565b600082825260208201905092915050565b600081905092915050565b600061249882612549565b91506124a383612549565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff038211156124d8576124d7612622565b5b828201905092915050565b60006124ee82612549565b91506124f983612549565b92508282101561250c5761250b612622565b5b828203905092915050565b600061252282612529565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b82818337600083830152505050565b60005b83811015612580578082015181840152602081019050612565565b8381111561258f576000848401525b50505050565b60006125a082612549565b915060008214156125b4576125b3612622565b5b600182039050919050565b600060028204905060018216806125d757607f821691505b602082108114156125eb576125ea612651565b5b50919050565b6125fa826126f2565b810181811067ffffffffffffffff82111715612619576126186126af565b5b80604052505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b600080fd5b600080fd5b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e00000000000000000000000000000000000000000000000000000000000000600082015250565b7f5200000000000000000000000000000000000000000000000000000000000000600082015250565b61275e81612517565b811461276957600080fd5b50565b61277581612549565b811461278057600080fd5b5056fea2646970667358221220dd8410284b14746f728b13c08aa84b67835e5eb5cfc25ccabe1cb8319eedfe8d64736f6c63430008070033'

''' ========================================================================================== '''

# SAMPLE: getting a value
#print(contracts.functions.getAlgo().call())

# SAMPLE: setting a value
#tx_hash = contracts.functions.<function>(--inputs--).transact()
#web3.eth.waitForTransactionReceipt(tx_hash)

def get_currentAcct(contracts):
    return contracts.functions.get_current_acct().call()

def get_algoCode(contracts):
    return contracts.functions.getAlgo().call()


if __name__ == "__main__":


    ''' vvvvvvvvvvvvvvvvvvvvvvvvv If Deployment in Web3 vvvvvvvvvvvvvvvvvvvvvvvvv '''
    # Instantiate the smart contract to be deployed(?)
    # EHR = web3.eth.contract(abi=abi, bytecode=bytecode)
    #
    # # Deploying the compiled smart contract (in Remix) to the Blockchain (ata)
    # tx_hash = EHR.constructor().transact()
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #
    #
    # #Instantiate the smart contract deployed via Address from the receipt and the ABI
    # contracts = web3.eth.contract(
    #  	address = tx_receipt.contractAddress,
    #  	abi=abi
    # )
    ''' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ '''

    # Instantiate the smart contract deployed (in Remix)
    contracts = web3.eth.contract(address=address, abi=abi)

    algo = input("Chosen Algorithm (AES/3DES/Blowfish): ")
    if algo:
        contracts.functions.setAlgo(algo).transact()
    else:
        pass # algorithm is default to AES

    # Debugging: confirming Algo Change
    chosenAlgorithm = get_algoCode(contracts)
    print(chosenAlgorithm)

    # Verify web3 to smart contract connection
    print('Web3 connection state: ' + str(web3.isConnected()))

    keyID = None
    keys = {}

    # Loading existing key 'storage' to keys dictionary
    try:
        keys = p.load(open('/Users/earth/Downloads/THESIS/app_keys/keys.rtf','rb'))
        print(keys)
    except:
        pass

    # # key generations - 192-bit and 24 bytes
    # # AES key generation
    # AES_key = token_bytes(32)
    # print("AES Key Generated: " + str(AES_key))
    # print("Key converted to hex: " + str(web3.toHex(AES_key)))
    # cipher = AES.new(AES_key, AES.MODE_EAX) # not totally sure ano ginagawa
    # print("Cipher: " + str(cipher))
    # temp = "Plain Text"
    # encrypt_data, tag = cipher.encrypt_and_digest(temp)
    # print("Plain: " + temp)
    # print("Encrypted: " + str(encrypt_data))
    # decrypt_data = cipher.decrypt(encrypt_data)
    # print(decrypt_data)

    # AES_key = token_bytes(32)
    # print("AES Key Generated: " + str(AES_key))
    # #                   v - computed
    #
    # cipher1 = AES.new(token_bytes(24), AES.MODE_EAX)
    # nonce = cipher1.nonce
    # file = b'Earth Lopez'
    # print("File before encryption: " + str(web3.toHex(file)))
    # encrypted_data = cipher1.encrypt(file)
    # print ("Encrypted data: " + str(web3.toHex(encrypted_data)))
    #
    # cipher2 = AES.new(b'}.\x86\x12F\xbf\xd4Dfc~\xe3U\xe9\xbf(\xe2\x1b\xaf\xef)a\xa36\xd5n1\xd1\x9f\xfd\xf8\x10', AES.MODE_EAX, nonce=nonce)
    # decrypted_data = cipher2.decrypt(encrypted_data)
    # print ("Decrypted data: " + str(web3.toHex(decrypted_data)))

    valid = True
    logged = True

    while (valid):
        ''' Temporary log-in for assigning a specified account for transaction (User session?) '''
        # temp default account for signing transactions?
        for a in range(0, len(web3.eth.accounts)):
            print(str(a) + ": " + str(web3.eth.accounts[a]))

        accountIndex = int(input("Which account to use: "))
        try:
            web3.eth.defaultAccount = web3.eth.accounts[accountIndex]
            logged = True
        except:
            pass

        while(logged):
            choice = int(input("Choices: (1. Create Request   2. Invoke/Revoke Permission)  3. Retrieve a Record   4. View Notification   5. Logout    6. Logout and Exit> "))

            if choice == 1:
                # get inputs : recipientWallet, recordID, accesscode
                currentAcct = get_currentAcct(contracts)
                print(currentAcct)
                recipient_wallet = input("Input recipient wallet: ")
                recordID = int(input("Input recordID to be shared: "))
                accesscode = input("Input access code (R or N): ")

                reqResult = contracts.functions.createReq(str(currentAcct), str(recipient_wallet), recordID, str(accesscode)).call()
                print(reqResult) # sample result (tuple) : [1, 1, '0x0D619E52fa0ff4EEB8e1cC9F3597c9dEb7c6B74e', 1]

                tx_hash = contracts.functions.createReq(str(currentAcct), str(recipient_wallet), recordID, str(accesscode)).transact()
                print(web3.toHex(tx_hash))

            elif choice == 2:
                print('Req result 0: ' + str(reqResult[0])) # result
                print('Req result 1: ' + str(reqResult[1])) # accessID
                print('Req result 2: ' + str(reqResult[2])) # address
                print('Req result 3: ' + str(reqResult[3])) # recordID

                if reqResult[0] == 1: #reqResult(0) == 1
                    # get inputs: accessID, recipientAddress, record ID
                    invokeResult = contracts.functions.invoke_Permission(reqResult[1], str(reqResult[2]), reqResult[3]).transact()
                    key_flag = web3.eth.waitForTransactionReceipt(invokeResult)

                    print(web3.toHex(invokeResult))
                    implemented = False

                    if(chosenAlgorithm == "AES"): #AES
                        # AES key generation
                        AES_key = token_bytes(32)
                        print ("AES Key: " + str(web3.toHex(AES_key)))

                        while not implemented:
                            keyID = random.randint(10000, 99999)
                            exist = keys.get(keyID)

                            if exist == None:
                                keys[str(keyID)] = AES_key
                                print("Key ID inserted is: " + str(keyID))
                                implemented = True


                    elif(chosenAlgorithm == "3DES"): #3DES
                        # 3DES key generation
                        while True:
                            try:
                                TripleDES_key = DES3.adjust_key_parity(get_random_bytes(24))
                                break
                            except ValueError:
                                pass
                        print ("3DES Key: " + str(web3.toHex(TripleDES_key)))

                        while not implemented:
                            keyID = random.randint(10000, 99999)
                            exist = keys.get(keyID)

                            if exist == None:
                                keys[str(keyID)] = TripleDES_key
                                print("Key ID inserted is: " + str(keyID))
                                implemented = True


                    elif(chosenAlgorithm == "Blowfish"):
                        # Blowfish key generation
                        Blowfish_key = token_bytes(24)
                        print ("Blowfish Key: " + str(web3.toHex(Blowfish_key)))

                        while not implemented:
                            keyID = random.randint(10000, 99999)
                            exist = keys.get(keyID)

                            if exist == None:
                                keys[str(keyID)] = Blowfish_key
                                print("Key ID inserted is: " + str(keyID))
                                implemented = True


                    keyStoreResult = contracts.functions.storeKey(reqResult[1], str(keyID)).transact()
                    print(web3.toHex(keyStoreResult))
                    print("All current keys: " + str(keys))


                elif reqResult[0] == 2:
                    # remove from key storage
                    getKeyIndex = contracts.functions.getKey(str(reqResult[2]), reqResult[3]).call()

                    print("Key index to be popped: " + str(getKeyIndex))
                    print("Key to delete: " + str(keys[getKeyIndex]))
                    del keys[str(getKeyIndex)];

                    # remove key validity from latest invoked smart contract
                    revokeResult = contracts.functions.revoke_Permission(reqResult[1], str(reqResult[2]), reqResult[3]).transact()
                    print(web3.toHex(revokeResult))

                    # Debugging: print
                    print("Remaining keys after removing and invalidating specified key: " + str(keys))

            elif choice == 3: # Retrieve a record
                '''
                    Inputs:
                        - Record ID (ID of record to retrieve)
                        - ***** Requesting ID? (Owner or Recipient) // initial: refer first via msg.sender (Assign in Remix which
                            account will "retrieve")
                '''
                # MAKE SURE ACCOUNT RETRIEVING IS CHOSEN IN REMIX FIRST BEFORE CALLING THIS CHOICE;; #recheck if msg.sender changes
                # otherwise, find a way to use the chosen account to be saved in the smart contracts
                recordID = int(input("Input recordID to retrieve: "))
                currentAcct = get_currentAcct(contracts)
                print("Current Account: " + str(currentAcct))

                verified = contracts.functions.verify_AP(currentAcct, recordID).call()
                print("Value ni verified: " + str(verified))

                if verified == 0: # if user has no permission to access record
                    print ("Request rejected: User is not permitted to access said record.")

                elif verified == 1: # if OWNER of record
                    Record = contracts.functions.pullRecord(recordID).call()

                    print('Record ID: {}   Date: {}'.format(Record[0], Record[1]))
                    print('Patient ID: {}   Patient Name: {}   Gender: {}'.format(Record[2], Record[3], Record[4]))
                    print('Vaccine Code: {}    Description: {}'.format(Record[5], Record[6]))

                # elif verified == 2: # if RECIPIENT with access to record
                #     recordID, date, patientID, patientName, gender, vacc_code, description = contracts.functions.pullRecord(recordID).transact()
                #
                #     # key = contracts.functions.getKey(reqResult[2], reqResult[3]).transact()
                #     # call to encrypt (function)
                #     # display encrypted record
                #     # getDecryptkey; key = contracts.functions.getKey(reqResult[2], reqResult[3]).transact()?
                #     # call to decrypt (function)
                #     print ('Record ID: {}   Date: {}\n
                #         Patient ID: {}   Patient Name: {}   Gender: {}\n
                #         Vaccine Code: {}    Description: {}').format(recordID, date, patientID, patientName, gender, vacc_code, description)

            elif choice == 4: # View Notification for a record
                # should be executed when user(recipient) is 'logged in'
                # need to get their access ID without relying on the reqResult made by the owner

                recordID = int(input("Input recordID to check notification(?): "))
                currentAcct = get_currentAcct(contracts)
                print("Current Account: " + str(currentAcct))

                notif = contracts.functions.createNotif(currentAcct, recordID).call()


                if notif[2] == 'Read Access':
                    print('A record has been shared and access permission is granted.\n')
                    print('Access ID: {}\nRecipient: {}\nAccess Permission: {}\nKey ID: {}'.format(notif[0], notif[1], notif[2], notif[3]))
                else:
                    print('No record has been shared. :\'(')

            elif choice == 5: # Logout
                p.dump(keys, open('/Users/earth/Downloads/THESIS/app_keys/keys.rtf','wb'))
                logged = False

            elif choice == 6: # Logout and Exit
                p.dump(keys, open('/Users/earth/Downloads/THESIS/app_keys/keys.rtf','wb'))
                logged = False
                valid = False
