import sys
import blockcypher
from bitcoinlib.wallets import Wallet
from bitcoinlib.wallets import WalletError
from bitcoinlib.wallets import HDKey
from bitcoinlib.keys import BKeyError


def create_blockcypher_hd_wallet(token: str, wallet_name: str, extended_key_to_import: str, is_extended_key_private: bool = False):
        
    if  not (token and token.strip()):
        raise Exception("token is required")
    
    if not (wallet_name and wallet_name.strip())  :
        raise Exception("wallet name is required")
    
    if not (extended_key_to_import and extended_key_to_import.strip())  :
        raise Exception("extended_key_to_import is required")
    
    try:
           
            # depth: 3, is_pivate = true (private), name="Account Extended Private Key"
            imported_key = HDKey.from_wif(extended_key_to_import,"bitcoin")
            wif = imported_key
            
            # internal version hd wallet
            wallet = Wallet.create( wallet_name, wif, witness_type='segwit', network='bitcoin' )
            blockcyper_wallet_response = blockcypher.create_hd_wallet( wallet_name, xpubkey=imported_key.wif_public(), api_key=token, subchain_indices = [0,1], coin_symbol= 'btc' )
        
            print(f"[Imported Key info]\n{ imported_key.as_json(include_private=is_extended_key_private) }\n" )
            print(f"\n[Imported Key (public key)]\n{imported_key}\n" )
            print(f"[Internal Wallet created with Imported Key]\n{wallet.as_json()}\n\n" )
            print(f'[Blockcypher create-wallet request\'s response]\n{blockcyper_wallet_response}\n\n' )

    except BKeyError as err:
        print(f"Error: {err.msg}")  

    except WalletError as err:
        if (err.msg):
            print(f"Error: {err.msg}")

    except Exception as err:
        if (err.args):
            print(f"Unexpected {err=}, {type(err)=}")


        