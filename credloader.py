 #key management
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidSignature
import traceback


# === System Identifier Functions ===

def raiser(error, original_exception=None):
    if original_exception:
        #traceback.print_exception(original_exception)
        raise Exception(error) from original_exception
    raise Exception(error)

''' def get_machine_guid():
    """Get Windows Machine GUID from registry."""
    try:
        output = subprocess.check_output(
            r'reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography /v MachineGuid',
            shell=True
        ).decode()
        return output.strip().split()[-1].encode()
    except Exception as e:
        raiser(f"A fatal error occured",e)

 '''
 
#my custom encoding
import random

myrule = {
    # Lowercase
    'a': ['zif', 'nek', 'tod'], 'b': ['lop', 'miv', 'zan'], 'c': ['wer', 'syt', 'vex'],
    'd': ['qaz', 'xev', 'tuc'], 'e': ['rud', 'niv', 'pel'], 'f': ['gop', 'hav', 'jid'],
    'g': ['keb', 'lan', 'mur'], 'h': ['nop', 'bex', 'tur'], 'i': ['sey', 'fim', 'duv'],
    'j': ['cad', 'rex', 'lym'], 'k': ['vyt', 'hom', 'buz'], 'l': ['pon', 'mex', 'zut'],
    'm': ['wex', 'dyk', 'luv'], 'n': ['zer', 'fik', 'bon'], 'o': ['sun', 'peg', 'tok'],
    'p': ['dat', 'mil', 'vod'], 'q': ['rix', 'cug', 'jam'], 'r': ['xat', 'kim', 'pov'],
    's': ['mop', 'leg', 'zuk'], 't': ['kex', 'nir', 'hud'], 'u': ['pam', 'wyt', 'fek'],
    'v': ['tug', 'bak', 'lom'], 'w': ['xeb', 'suv', 'yit'], 'x': ['qom', 'fer', 'lap'],
    'y': ['rin', 'duk', 'gev'], 'z': ['job', 'kir', 'vek'],

    # Uppercase
    'A': ['KIH', 'QET', 'VUX'], 'B': ['LOL', 'WEM', 'ZEN'], 'C': ['XIT', 'FAZ', 'YOL'],
    'D': ['GUB', 'NAQ', 'MIX'], 'E': ['TEL', 'POV', 'RIK'], 'F': ['DUZ', 'LAX', 'JEY'],
    'G': ['VAG', 'MOH', 'QIK'], 'H': ['SEX', 'NIR', 'BAG'], 'I': ['LIZ', 'QUP', 'WAD'],
    'J': ['NAD', 'VUZ', 'PEX'], 'K': ['RIZ', 'KOB', 'SUL'], 'L': ['BEG', 'HIT', 'XUR'],
    'M': ['RAX', 'ZIM', 'WOC'], 'N': ['HUK', 'SIP', 'VET'], 'O': ['PAH', 'JOX', 'YEK'],
    'P': ['MAX', 'LOK', 'CUB'], 'Q': ['REK', 'HUX', 'YIN'], 'R': ['COZ', 'MIB', 'VIL'],
    'S': ['NAF', 'TIK', 'LOZ'], 'T': ['PUK', 'RIY', 'GEX'], 'U': ['DIZ', 'NEP', 'WOQ'],
    'V': ['LOX', 'KUN', 'ZOD'], 'W': ['TAD', 'FEX', 'GIB'], 'X': ['YOD', 'KIV', 'MOT'],
    'Y': ['WUV', 'GUR', 'BAQ'], 'Z': ['ZEQ', 'RUH', 'XID'],

    # Digits
    '0': ['pik', 'qad', 'nuz'], '1': ['wek', 'tud', 'bam'], '2': ['kaf', 'len', 'sor'],
    '3': ['riv', 'fok', 'jug'], '4': ['wab', 'yem', 'dig'], '5': ['qux', 'jor', 'liv'],
    '6': ['boh', 'nam', 'sig'], '7': ['hed', 'lug', 'xim'], '8': ['meh', 'sud', 'vok'],
    '9': ['zeh', 'wit', 'baj'],

    # Special characters
    '+': ['pls', 'adt', 'sgn'],
    '/': ['sls', 'dvt', 'brs'],
    '=': ['eql', 'pad', 'end']
}

def create_reverse_rule(rule):
    """Create a reverse mapping for decoding - maps all code variations back to original chars"""
    reverse_rule = {}
    for char, replacements in rule.items():
        for code in replacements:
            reverse_rule[code] = char
    return reverse_rule

reverse_rule = create_reverse_rule(myrule)

def custom_encode(data, encode: bool = True):
    """
    Apply custom encoding/decoding after Base64 with random code selection
    Args:
        data: Input string to process
        encode: True for encoding, False for decoding
    Returns:
        Processed string
    """
    if encode:
        # First convert to Base64 (check if its bytes)
        if isinstance(data,bytes):
           b64_data = base64.b64encode(data).decode()
        else:
           b64_data = base64.b64encode(data.encode()).decode()
           
        # Apply custom encoding with random choice
        result = []
        for char in b64_data:
            if char in myrule:
                # Randomly select one of the three encoding options
                result.append(random.choice(myrule[char]))
            else:
                # RETURN A NOT BASE64 TEXT
                raiser("Not a base64 file")
             
        return ''.join(result)
    else:
        decoded_chars = []
        i = 0
        if isinstance(data,bytes):
            mody = data.decode("utf-8")
        else:
            mody = data
        while i < len(mody):
           code = mody[i:i+3]
           if code in reverse_rule:
              decoded_chars.append(reverse_rule[code])
           else:
              raiser(f"Corrupt base 64 string")
           i += 3

        base64_string = ''.join(decoded_chars)
        return base64.b64decode(base64_string)


def find_middle_char(text):

    if not text:  # Handle empty string case
        return None
    
    length = len(text)
    middle_index = (length - 1) // 2  # Integer division favoring left 
    
    return (middle_index)  # Return the position opf the middle character


import winreg

def get_machine_guid():
    """Get Windows Machine GUID using winreg module."""
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Cryptography"
        ) as key:
            wguid = winreg.QueryValueEx(key, "MachineGuid")[0]
            
            #turning the string left to right for advanced security
            middlenum = find_middle_char(wguid) # return the position number of the middle char
            spiltfromniddle = wguid[0:int(middlenum)]
            reststring = wguid[int(middlenum):]
            
            switched = reststring+""+spiltfromniddle
        
            # More secure transformation using HMAC
            hmac = hashes.Hash(hashes.SHA256(), backend=default_backend())
            hmac.update(switched.encode())
            transformed = hmac.finalize()
            
            return base64.b64encode(transformed)
        
            
    except Exception as e:
        raiser(f"A fatal error occured",e)
    

# === Key Derivation ===

def derive_key(secret: bytes, salt: bytes = None):
    """Secure key derivation with optional salt."""
    # Generate random salt if none provided
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),  # Stronger than SHA256
        length=32,
        salt=salt,
        iterations=310000,  # NIST recommended minimum
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(secret))


def encrypt_file(input_path: str, output_path: str, text=False):
  try:
    """
    Encrypt a file using machine GUID derived key
    Stores salt with encrypted data
    """
    # Get machine GUID and derive key
    guid_derivative = get_machine_guid()
    salt = os.urandom(16)
    key = derive_key(guid_derivative, salt)
    
    # Read file content
    if text is True:
        file_data = input_path.encode()
      
    else:
        with open(input_path, 'rb') as f:
          file_data = f.read()
          
    # Encrypt
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(file_data)
    secondlayer = custom_encode(salt + encrypted_data,True) #enrypt the bytes
    # Store salt + encrypted data
    with open(output_path, 'wb') as f:
        f.write(secondlayer.encode())
 

  except Exception as e:
     raiser(f"A fatal error occured",e)
 
 
def decrypt_file(input_path: str, output_path=None,save=True):
  #Decrypt a file using machine GUID derived key
  #Reads salt from beginning of file

  try:
    
    # Get machine GUID
    guid_derivative = get_machine_guid()
    
    # Read salt and encrypted data
    with open(input_path, 'rb') as f:
        secondlayer = custom_encode(f.read(),False) #decoding
        #secondlayer = secondlayer.encode()
        salt = secondlayer[:16]
        encrypted_data = secondlayer[16:]
    
    # Derive same key
    key = derive_key(guid_derivative, salt)
    
    # Decrypt
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)
        
    # Write decrypted file
    if output_path is not None and save is True:
      with open(output_path, 'wb') as f:
       f.write(decrypted_data)
    else:
        return decrypted_data
    
  except InvalidToken:#IF KEYS DO NOT MATCH ASSUMES USING SURTR FOR THE FIRST TIME
    raise InvalidToken("First time use detected")
            
  except InvalidSignature: 
    raise InvalidSignature("Surtr has some currupt file and need instant repair")
    
            
  except Exception:
        raise InvalidSignature("Surtr has some currupt file and need instant repair")
 