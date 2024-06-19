mnemonics = []

def add_mnemonic(mnemonic):
    mnemonics.append(mnemonic)

def remove_mnemonic(mnemonic):
    if mnemonic in mnemonics:
        mnemonics.remove(mnemonic)

def list_mnemonics():
    return mnemonics
