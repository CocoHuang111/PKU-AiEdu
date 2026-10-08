> 检索摘要：MAS.S62 Cryptocurrency Engineering and Design（Spring 2018，Graduate）的「Problem Set 2: Mine Your Name」。页内标题：Problem Set 2: Mine Your Name；Mine Your Name Into the Blockchain；Block Specifications；Client / Server Connections；What To Do。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/mas-s62-cryptocurrency-engineering-and-design-spring-2018/pages/assignments/pset2-mine-your-name/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Problem Set 2: Mine Your Name

### Mine Your Name Into the Blockchain

This problem set will use a mock blockchain which you can mine blocks into.

### Block Specifications

Blocks are ASCII strings, with a maximum length of 100 characters. The block format is:

> `prevhash name nonce`

“prevhash” is the ascii hexadecimal representation of the previous block hash. It must be lowercase and in hex; do not use raw bytes. Example:

> `00000000c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b`

“name” is the name you want to credit nameChain points to. It’s case sensitive. Example:

> `miner2049`

“nonce” is a random nonce to satisfy the work requirement. Example:

> `TWFuI3GlzIGR`

Note that names and nonces must be in the base64 character set:

> `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`

which is just caps, lowercase, numbers and + and /. Can’t have spaces; spaces separate the 3 different elements of the block. This is to make everything easy to run through terminals, let people use shell scripts, and so on.

### Client / Server Connections

This problem set has a server. It’s not a real decentralized system, as that’s too much work to deal with for this early assignment. There is a NameChain server which listens on a TCP port, and when a TCP connection is made to it, it sends the current blockchain tip. Connected clients can send a new block to it, which, if valid, will be appended to the end of the blockchain.

The required work is 2^33, which is twice as difficult as the initial target for the Bitcoin network. (But nowhere near as difficult as the current Bitcoin target.)

### What To Do

A bunch are already written for you. The network functions are `GetTipFromServer()` and `SendBlockToServer()` and already implemented, so you don’t have to deal with TCP.

You need to write the `Mine()` function and then `SendBlockToServer()` once you have mined a block.

You may need to poll the server for new blocks occasionally so that you don’t submit “stale” blocks, where someone else submitted a block before you did with the same parent. To not DDoS our server, please keep requests to 1 per second maximum.

Using Go concurrency features is recommended for this problem set. The amount of work required to find a block is fairly high, and if you’re mining using only 1 CPU core you will be at a disadvantage compared to multi-threaded, multi-core miners.

Here is a simple tutorial on Go channels; they’re not too hard to use, even if you haven’t done multi-threaded programming before. They allow you to pass messages between functions which are running at the same time. There are also other possible methods like `sync.WaitGroup`, or, in fact, it’s quite possible to mine without any synchronization between threads at all.

There will be a “high score” ranking with the number of blocks in the chain made by each user. This is the same as getting more coins by mining more blocks. To get a high score, mine a bunch of blocks with the same name. We’re using names instead of public keys which is not as decentralized, but we know who you are already.

The entire current blockchain can be downloaded from the server at port 6299. Example code:

`$ nc hubris.media.mit.edu 6299`

`00000000722a3b3cabaac078bd4e15ce361312895cfef0494c9ffc75bedb82db adiabat 19579781213`

This is if you want to check how the blockchain is progressing.
