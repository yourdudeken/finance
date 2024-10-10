from bitcoin import *

# Replace these with your actual private keys and redeem script
private_keys = ['<private_key1>', '<private_key2>']
redeem_script = '<redeem_script>'
multisig_address = '<multisig_address>'
recipient_address = '<recipient_address>'
amount_to_send = 0.001  # Amount in BTC
transaction_fee = 0.0001  # Transaction fee in BTC

# Fetch unspent outputs for the multisig address
unspent_outputs = unspent(multisig_address)

# Create raw transaction
inputs = [{'txid': utxo['output'], 'vout': utxo['output_index']} for utxo in unspent_outputs]
outputs = {recipient_address: amount_to_send, multisig_address: sum([utxo['value'] for utxo in unspent_outputs]) - amount_to_send - transaction_fee}
raw_tx = mktx(inputs, outputs)

# Sign the transaction with each private key
signed_tx = raw_tx
for key in private_keys:
    signed_tx = sign(signed_tx, 0, key, redeem_script)

# Broadcast the transaction
broadcast_tx(signed_tx)