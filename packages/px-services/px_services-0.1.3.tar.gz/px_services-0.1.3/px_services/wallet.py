import blockcypher
import json
from bitcoinlib.wallets import Wallet
from bitcoinlib.wallets import WalletError
from bitcoinlib.wallets import HDKey
from bitcoinlib.keys import BKeyError

class PxWallet:
    def __init__(self, _token: str, _wallet_name: str, _extended_key_to_import: str, _is_extended_key_private: bool = False, _printLog: bool = False ):
        self.token = _token
        self.wallet_name = _wallet_name
        self.extended_key_to_import = _extended_key_to_import
        self.is_extended_key_private = _is_extended_key_private
        self.printLog=_printLog

    def create_blockcypher_hd_wallet(self):
        """
        This method create a wallet on BlockCypher Service by sending an HTTP request to the hd wallet endpoint and as well create a internal wallet which can be use to manage/retrieve addresses, public & private keys info.  
        
        @author: Prince Foli (developer.prncfoli@gmail.com)

        @return ``dict[str, Any]``:  There are 3 main dictionary key of interest here. These are ``blockcyper_wallet_response``, ``internal_wallet_info``, ``imported_key_info``
        
        NB:

        required library: ``mnemonic`` , ``bitcoinlib`` 
        
        use the command below to install:

        ``pip3 install blockcypher bitcoinlib``

        """

            
        if  not (self.token and self.token.strip()):
            raise Exception("token is required")
        
        if not (self.wallet_name and self.wallet_name.strip())  :
            raise Exception("wallet name is required")
        
        if not (self.extended_key_to_import and self.extended_key_to_import.strip())  :
            raise Exception("extended_key_to_import is required")
        
        if not (self.extended_key_to_import.startswith("zpub") or  self.extended_key_to_import.startswith("zprv")):
            raise Exception("extended_key_to_import must either begin with zpub or zprv")
        
        try:
            
                # depth: 3, is_pivate = true (private), name="Account Extended Private Key"
                imported_key = HDKey.from_wif(self.extended_key_to_import,"bitcoin")
                wif = imported_key
                
                # internal version hd wallet
                wallet = Wallet.create( self.wallet_name, wif, witness_type='segwit', network='bitcoin' )
                blockcyper_wallet_response = blockcypher.create_hd_wallet( self.wallet_name, xpubkey=imported_key.wif_public(), api_key=self.token, subchain_indices = [0,1], coin_symbol= 'btc' )
            
                if( self.printLog ):
                    print(f"[Imported Key info]\n{ imported_key.as_json(include_private=self.is_extended_key_private) }\n" )
                    #print(f"\n[Imported Key (public key hex)]\n{imported_key}\n" )
                    print(f"[Internal Wallet created with Imported Key]\n{wallet.as_json()}\n\n" )
                    print(f'[Blockcypher create-wallet request\'s response]\n{blockcyper_wallet_response}\n\n' )
                return  { 
                    "blockcyper_wallet_response": blockcyper_wallet_response, 
                    "internal_wallet_info": wallet.as_json(),
                    "imported_key_info": imported_key.as_json(include_private=self.is_extended_key_private)
                    }

        except BKeyError as err:
            print(f"Error: {err.msg}")  

        except WalletError as err:
            if (err.msg):
                print(f"Error: {err.msg}")

        except Exception as err:
            if (err.args):
                print(f"Unexpected {err=}, {type(err)=}")
    def create_blockcypher_hd_wallet_with(self, subchain_indices=[0,1] ):
        """
        This method create a wallet on BlockCypher Service by sending an HTTP request to the hd wallet endpoint and as well create a internal wallet which can be use to manage/retrieve addresses, public & private keys info.  
        
        @author: Prince Foli (developer.prncfoli@gmail.com)

        @param ``subchain_indices``: these indices indicates the address chain type that you want to create, where 0 is normal address chain and 1 is change address chain.
        @return ``dict[str, Any]``:  There are 3 main dictionary key of interest here. These are ``blockcyper_wallet_response``, ``internal_wallet_info``, ``imported_key_info``
        
        NB:

        required library: ``mnemonic`` , ``bitcoinlib`` 
        
        use the command below to install:

        ``pip3 install blockcypher bitcoinlib``

        """

            
        if  not (self.token and self.token.strip()):
            raise Exception("token is required")
        
        if not (self.wallet_name and self.wallet_name.strip())  :
            raise Exception("wallet name is required")
        
        if not (self.extended_key_to_import and self.extended_key_to_import.strip())  :
            raise Exception("extended_key_to_import is required")
        
        if not (self.extended_key_to_import.startswith("zpub") or  self.extended_key_to_import.startswith("zprv")):
           raise Exception("extended_key_to_import must either begin with zpub or zprv")
        
        try:
            
            # depth: 3, is_pivate = true (private), name="Account Extended Private Key"
            imported_key = HDKey.from_wif(self.extended_key_to_import,"bitcoin")
            wif = imported_key
                
            # internal version hd wallet
            wallet = Wallet.create( self.wallet_name, wif, witness_type='segwit', network='bitcoin' )
            blockcyper_wallet_response = blockcypher.create_hd_wallet( self.wallet_name, xpubkey=imported_key.wif_public(), api_key=self.token, subchain_indices = subchain_indices, coin_symbol= 'btc' )
            
            if( self.printLog ):
                print(f"[Imported Key info]\n{ imported_key.as_json(include_private=self.is_extended_key_private) }\n" )
                #print(f"\n[Imported Key (public key hex)]\n{imported_key}\n" )
                print(f"[Internal Wallet created with Imported Key]\n{wallet.as_json()}\n\n" )
                print(f'[Blockcypher create-wallet request\'s response]\n{blockcyper_wallet_response}\n\n' )
            return  { 
                "blockcyper_wallet_response": blockcyper_wallet_response, 
                "internal_wallet_info": wallet.as_json(),
                "imported_key_info": imported_key.as_json(include_private=self.is_extended_key_private)
            }

        except BKeyError as err:
            print(f"Error: {err.msg}")  

        except WalletError as err:
            if (err.msg):
                print(f"Error: {err.msg}")

        except Exception as err:
            if (err.args):
                print(f"Unexpected {err=}, {type(err)=}")
    
class PxWalletKeyGenerator:
    @staticmethod
    def generate_seed_phrase(print_log=True):
        
        """
        This generate 12 word phrase that can serve as a recovery phrase (word list). This word list is supposed to be kept secret. Please do not share this with anyone because doing so will mean you are giving away your private key info. Only use it to recover funds on any trusted wallet or wallet provider service or application. Please note that not keeping your ``seed``  or ``secret_recovery_words``safe may result you losing your funds. 
        
        @author: Prince Foli (developer.prncfoli@gmail.com)

        @return ``tuple[str, dict[str, Any]]``:  The first index of tuple is ``recovery phrase`` which is also known as ``seed phrase`` or ``backup phrase``. The second index of the tuple is dictionary of ``seed`` values. There are two main dictionary keys that might be of interest. These are ``bytes`` and ``hex`` and they represent the format of the seed
        
        NB:

        required library: ``mnemonic`` 
        
        use the command below to install:

        ``pip3 install mnemonic``
        """

        from mnemonic import Mnemonic

        mnemo = Mnemonic("english")
        
        # word count: [ 12,  15,  18,  21,  24]
        # bit size:   [128, 160, 192, 224, 256]
        secret_recovery_words = mnemo.generate(strength=128)
        if (print_log):
            print('\n[Secret Recovery Phrase | Backup Phrase | Seed Phrase]\n\n%s\n\n' %secret_recovery_words)

        master_seed = mnemo.to_seed(secret_recovery_words, passphrase="")
        if (print_log):
            print('[ Seed (in hex) ]\n\n%s\n' %master_seed.hex())
        seed = { "hex":  (master_seed.hex()), "btyes": master_seed }
        return ( secret_recovery_words, seed )
    @staticmethod
    def seedToMasterKey(seed, print_log=True):
    
        """
        Import/Retrieve segwit extended master key from ``seed`` (in hex)

        @author: Prince Foli (developer.prncfoli@gmail.com)

        @type ``seed``: hex
        @param ``seed``: The seed (in hex) to import.

        @return ``(tuple[dict[str, dict[str, Any]], HDKey] | None)``: The first index of tuple is dictionary that contains master key information and the second index is the HDKey object of the master key. There are two main dictionary key that is of interest and these are ``extended_key`` and ``account_keys``. Note that these are all extended keys but serve different roles. ``Account Keys`` (``account_keys`` because their ``depth`` equals ``3``) are normally derived from ``Root Extended Keys`` ( ``extend_keys`` a.k.a ``root keys`` because their ``depth`` equals ``0`` ).
        
        # usage: 

        >>> recovery_words, seed = PxWalletKeyGenerator.generate_seed_phrase()

        >>> info, key = PxWalletKeyGenerator.seedToMasterKey(seed['hex'])


        # NB: 
        
        ``Extended private key (xprv, zprv)`` = ``Parent private key``   ``+``   ``Parent chain code`` 
        
        ``Extended public key (xpub, zpub)`` = ``Parent public key``   ``+``   ``Parent chain code`` 

        The first level extended private key generated is also known as ``BIP32 Root key`` or ``Master (private) key`` 
        
        The first level extended public key generated is also known as  ``BIP32 Root key`` or ``Master (public) key``
        
        required library: ``bitcoinlib`` 
        
        use the command below to install:
        
        ``pip3 install bitcoinlib``
        """
        from bitcoinlib.wallets import HDKey
        
        if (seed is None):
            raise ValueError('seed parameter is required')
        else:
            master_key_info = HDKey.from_seed(seed, encoding='bech32', witness_type='segwit', network='bitcoin')
            if(master_key_info):
                point_x, point_y = master_key_info.public_point()
                if (master_key_info.secret):
                    key_info = {
                        "master_key_info": { 
                            "network": master_key_info.network.name,
                            "bip32_root_key": master_key_info.wif(is_private=True),
                            "extended_keys": [
                                {
                                    "name": "extended_private_key",
                                    "value": master_key_info.wif(is_private=True),
                                    "depth": 0,
                                    "format": "wif",
                                    "note": "This is the BIP32 root private key. It is also known the root key. This is same as ``bip32_root_key`` "
                                },
                                {
                                    "name": "extended_public_key",
                                    "value": master_key_info.wif_public(),
                                    "depth": 0,
                                    "format": "wif",
                                    "note": "This is the BIP32 root public key "
                                }
                            ],
                            "account_keys": {
                                "zpub":  master_key_info.subkey_for_path("m/84'/0'/0'").wif_public(),
                                "zprv":  master_key_info.subkey_for_path("m/84'/0'/0'").wif_private(),
                                "format": "wif",
                                "path": "m/84'/0'/0'",
                                "depth": 3,
                                "note": "These keys are known as account level keys because they are derived on the path ``m/84'/0'/0'``. The path representation is ``m/purpose/coin_type/account``. Keys derived on path is also known as ``Segwit as root key``."
                            },
                            "parent": {
                                "private":[
                                    { 
                                        "name": "parent_private_key_wif",
                                        "key": master_key_info.wif_key(),
                                        "format": "wif"
                                    },
                                    { 
                                        "name": "parent_private_key_hex",
                                        "key": master_key_info.private_hex,
                                        "format": 'hex',
                                        "compressed": True,
                                    },
                                    { 
                                        "name": "parent_secret",
                                        "key": master_key_info.secret,
                                        "format": "long", 
                                    },
                                ],
                                "public":[
                                    { 
                                        "name": "public_key_hex",
                                        "key": master_key_info.public_hex,
                                        "format": "hex",
                                        "compressed": True,
                                    },
                                    { 
                                        "name": "public_key_uncompressed_hex",
                                        "key": master_key_info._public_uncompressed_hex,
                                        "format'": "hex",
                                        "compressed": False,
                                    },
                                    { 
                                        "name": "hash160_hex",
                                        "key":  master_key_info.hash160.hex(),
                                        "format": "hex" 
                                    },
                                    { 
                                        "name": "hash160_btyes",
                                        "key": master_key_info.hash160,
                                        "format": "btyes",
                                    }
                                ],
                                "public_key_points": {
                                    "x": "%s" %point_x,
                                    "y" : "%s" %point_y ,
                                },
                                "address" : {
                                    "value" : master_key_info.address(),
                                    "type": "segwit",
                                    "format": "bech",
                                    "note": 'bc1 address'
                                },
                                "chain": {
                                    "name":"parent_chain_code",
                                    "code": master_key_info.chain.hex(),
                                    "format": "hex"
                                }
                            }
                        } 
                    }
                    
                    if(print_log):
                        # master_key_info.info()
                        print('\n[key_info]\n\n%s\n' % json.dumps(key_info), sep='')
                    return (key_info, master_key_info)
     

