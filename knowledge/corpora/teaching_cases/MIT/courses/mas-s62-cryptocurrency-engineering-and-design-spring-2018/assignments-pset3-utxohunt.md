> 检索摘要：MAS.S62 Cryptocurrency Engineering and Design（Spring 2018，Graduate）的「Assignments Problem Set 3: UTXOhunt」。页内标题：Assignments Problem Set 3: UTXOhunt；Setup；main.go；addrfrompriv.go；eztxbuilder.go；opreturn.go；Task 1: Create a Bitcoin Address；Task 2: Find the First Treasure Hunt Transaction；Task 3: Make a Transaction；Further Steps / Bonus Money。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/mas-s62-cryptocurrency-engineering-and-design-spring-2018/pages/assignments/pset3-utxohunt/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments Problem Set 3: UTXOhunt

In this assignment, we’re going to make some transactions on the Bitcoin test network using btcd for libraries, which is a bitcoin implementation written in golang. The goal is to understand how transactions are constructed and signed, and to become more familiar with the utxo model Bitcoin uses.

Testnet3 is a network for testing out Bitcoin. It works almost exactly like the regular Bitcoin network (small changes to addresses, the difficulty of proof of work) but everyone agrees that the testnet coins are not worth anything. This isn’t enforced by anything on the network, it’s just something people decide. The fact that it’s testnet3 indicates that this rule failed for testnets 1 and 2, when people started trading the testnet coins for mainnet coins.

In this problem set you’ll perform many of the functions of wallet software, by identifying outputs to spend, creating transactions, signing them, and broadcasting them to the network. Most wallet software does this all automatically, but this assignment is more manual so you can see how it works.

### Setup

Get Bitcoin Core 0.16.0, available at [the download section of the Bitcoin Core website](https://bitcoincore.org/en/download/).

To get on to the test network, make a bitcoin.conf file in your bitcoin folder (which is `HOMEDIR/.bitcoin/bitcoin.conf` or in linux `~/.bitcoin/`) and have the following line in the conf file:

`testnet=1`

and then run

`$ bitcoind --daemon`

so that it runs in the background. Syncing up to the testnet will require download of around 12 GB and will take a few hours depending on your computer’s speed. Some MIT guest wifi will block outgoing connections to different ports, so try using wired ethernet or another SSID if it doesn’t seem to download.

Once bitcoind is running, you can see what it’s doing by looking at the `/.bitcoin/testnet3/debug.log` file and issue commands with `bitcoin-cli`.

In this repo there are 4 files:

`main.go`

`addrfrompriv.go`

`eztxbuilder.go`

`opreturn.go`

Here’s what they do:

#### main.go

This is the main function which is called when you run `./utxohunt`

Edit this file to call functions from other files when you run the program.

#### addrfrompriv.go

Creates a public key and bitcoin address from a private key. Addresses are copy&pastable encodings of public key hashes.

#### eztxbuilder.go

Puts a transaction together, signs it, and prints the tx hex to the screen. This can then be sent to the network with the `pushrawtransaction` command in `bitcoin-cli` or to your own bitcoin node with `./bitcoin-cli pushrawtransaction (tx hex)`.

#### opreturn.go

Similar to `eztxbuilder.go`, but creates a transaction with 1 input, and 2 outputs. 1 of the outputs is an “OP_RETURN” output which can contain arbitrary data. Use this to submit your results to the blockchain.

### Task 1: Create a Bitcoin Address

First, look in `utxohunt/main.go`, and make a keypair. The `AddressFromPrivateKey()` function will help you. Put your own random string in to generate a private key. If you call the `AddressFromPrivateKey()` function, it will return that address as a string, as well as give you the compressed public key and pay to witness pubkey hash script.

Save this address (it starts with an “m”). You’ll need this to send the money to yourself.

### Task 2: Find the First Treasure Hunt Transaction

A *block explorer* is a website which watches the blockchain and parses out information about blocks, addresses, and transactions. You can use this blockexplorer to see what’s happening on the Bitcoin testnet.

I’ve created a transaction with one 70 outputs. `1f497ac245eb25cd94157c290f62d042e3bdda1e57920b6d1d2c5cfa362c12da` is the txid, or unique identifier of this transaction. (The txid is the hash of the serialized transaction.)

The outputs of this transaction are all have the same address, which determines how they can be spent. The private key for this pubkey-hash address is the double-sha256 of the string “mas.s62”.

Claim an unspent output in this transaction. Please be nice and leave the rest of the outputs for other classmates! :)

### Task 3: Make a Transaction

Using `EZTxBuilder()`, make a transaction sending from the up-for-grabs transaction to your own address.

You will need to modify:

`hashStr`

`outPoint` (output index number)

`sendToAddressString`

`prevAddressString` (the address of the “BTC secret key” pubkey)

`wire.NewTxOut` (change the amount to less than the input amount. A few thousand less is enough of a fee)

When you modify the code, you need to re-compile the code. Run “`go build`” in that directory to compile.

You’ll get a long hex string which you can test by running the transaction though bitcoin-cli’s decoderawtransaction command `./bitcoin-cli decoderawtransaction (tx hex)`.

If you get an error, it might be for one of the following reasons:

1. Someone has already claimed the output you are trying to get. Go back and look at the transaction’s page and see if the output is still available. It will say “inputs spent” or equivalent.
2. 64: non-mandatory-script-verify-flag (Signature must be zero for failed `CHECK(MULTI)SIG` operation). This means your signature was invalid. Often this is because the hash being signed was invalid. This could be because the previous output you signed and the one you indicted don’t match, the wrong amount is being sent to the `WitnessScript` function, or some other invalid data is in the transaction prior to signing. An invalid signature can also be caused by using the wrong key. In that case, you will usually get this error:
3. 64: non-mandatory-script-verify-flag (Script failed an `OP_EQUALVERIFY` operation). This means you’re probably using the wrong key to sign with, as the public key used and public key hash in the previous output script don’t match.
4. TX decode failed. That means you’re missing some characters, or the transaction is otherwise unintelligible to the bitcoin-cli parser.

If everything worked, the `decoderawtransaction` output will show you a json representation of the transaction you’ve created. You can then send it to the network with the command sendrawtransaction. If that works, it will return a txid. If that works and the transaction is confirmed (check with `getrawtransaction`), you’ve got some testnet coins! You can use the same `EZTxBuilder()` to send that money somewhere else.

### Further Steps / Bonus Money

Try to get some more money. There are some coins stashed through the network, and we will add more over the week :)

The first output One has a private key which is the double-sha256 of the *address* from which you took the first coins.

To grab these coins, you will need to use `AddressFromPrivateKey()` to generate that address, search the blockchain for the txid, and try to send an output to yourself, the same way as with the first transaction you created.

Note that in many cases, someone else in the class may have grabbed the coins before you. That’s OK, just write down where you found the coins to be and the private key you would have used to take them.
