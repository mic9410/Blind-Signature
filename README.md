# Blind-Signature
To run this project you have to generate private and public keys (.pem format), and type in the console:

python Server.py -p 12345 -S 'private_key.pem'

to run Serer.py, where -p is port ans S is private key, and:

python Client.py -o 'localhost' -p 12345 -K 'public_key.pem' -M 123

to run Client.py, where -o is host, -p is port and -M is your message. 
