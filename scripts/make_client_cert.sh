#!/bin/bash

# accessing the puppetdb server requires a client certificate signed by the
# relevant CA for that server

# this script takes a CA cert as the first argument and the CA key as the second,
# which you can find either in the akvo-config repository or near the relevant
# environment declaration for vagrant boxes.

# the third argument is the base name for the certificates ($BASENAME.{crt,key}),
# it's a good idea to include information about the target puppetdb in this name
# (eg, butler-live)

# for testing butler using vagrant, the client certificate is already on the VM

# it will then create a client certificate and key, which you can move where you
# want ('butler.crt' and 'butler.key' in the repository root is the preferred
# default)

# to test, use
#    curl --cert [the crt created] --key [the key created] --cacert [path to puppetdb CA cert] [puppetdb url]

CACERT=$1
CAKEY=$2
BASENAME=$3

# make the key
openssl genrsa -out $BASENAME.key 2048

# make the signing request
SUBJ='/CN=`hostname -f`/O=akvo.org/C=NL'
openssl req -new -key $BASENAME.key -out $BASENAME.csr -subj "$SUBJ"

# make the client certificate
openssl x509 -req -days 3650 -in $BASENAME.csr -CA $CACERT -CAkey $CAKEY -set_serial 01 -out $BASENAME.crt

# clean up
rm $BASENAME.csr
