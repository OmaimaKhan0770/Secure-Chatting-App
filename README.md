# Secure Chatting Application

A Python based secure chatting application built for an **Information Security** course. The project combines **real-time client-server communication, password hashing, and cryptographic algorithms** with a performance dashboard used to compare DES, AES, and RSA.

## Project Overview

This project was designed to demonstrate how security concepts can be implemented in a practical messaging system.

The application uses **Python socket programming** for real-time communication between clients and the server. A login system is included for user authentication, where passwords are **hashed before being stored** rather than keeping the original plaintext passwords.

The project also includes a **cryptographic performance dashboard**. DES, AES, and RSA are tested and compared to understand their practical performance in terms of factors such as **execution time and computational overhead**. The goal is to observe which algorithm is more suitable under different circumstances rather than simply comparing them theoretically.

## Main Features

* Real time chatting using **Python socket programming**
* Client-server communication architecture
* User login/authentication system
* Password **hashing** before storage
* Implementation of **DES, AES, and RSA**
* Dashboard for cryptographic algorithm comparison
* Performance measurement and comparison
* Analysis of execution time and computational requirements

## Technologies Used

* **Python**
* **Socket Programming** for real time client-server communication
* **Cryptography** DES, AES, RSA
* **Password Hashing** for secure password storage
* **Dashboard / Data Visualization** for performance analysis

## Project Files

```text
Secure-Chatting-Application/
│
├── client.py          # Client-side chat application
├── server.py          # Server-side communication
├── crypto_utils.py    # Cryptographic operations
├── login_system.py    # User login and password handling
├── dashboard.py       # Algorithm performance comparison
├── users.txt          # Stored user information / password hashes
└── README.md
```

## How the System Works

### 1. User Authentication

The user first logs in through the authentication system. Passwords are **hashed before they are stored**, so the original password is not saved directly in the file.

### 2. Server Setup

The server is started using `server.py`. It creates the socket and waits for clients to connect.

### 3. Client Connection

The client is started using `client.py`. The client connects to the running server and can participate in the chat.

### 4. Real-Time Communication

Messages are exchanged between the client and server using **Python sockets**, allowing the application to demonstrate real-time network communication.

### 5. Cryptographic Performance Testing

The `dashboard.py` component is used to compare the implemented algorithms. DES, AES, and RSA are tested using the selected data/operations, and their performance is measured.

The comparison focuses on practical factors such as:

* Execution time
* Encryption/decryption performance
* Computational overhead
* Relative efficiency of the algorithms

## How to Run the Project

### Step 1 — Install Python

Make sure Python is installed on your system.

### Step 2 — Open the Project

Clone or download the repository and open a terminal in the project folder.

### Step 3 — Start the Server

Run:

```bash
python server.py
```

Keep this terminal running.

### Step 4 — Start the First Client

Open another terminal and run:

```bash
python client.py
```

Log in using a registered user and start chatting.

### Step 5 — Start Another Client

To simulate another user, open **another terminal** and run `client.py` again:

```bash
python client.py
```

Log in as the second user. This allows two separate client instances to communicate through the same server.

> **Important:** The server should remain running while the clients are being used.

### Step 6 — Run the Performance Dashboard

After starting or when you want to analyze the cryptographic algorithms, run:

```bash
python dashboard.py
```

Use the dashboard to compare **DES, AES, and RSA** based on the measured performance results.

## Cryptographic Algorithm Comparison

The project includes three encryption algorithms for practical comparison:

| Algorithm | Type       | Main Purpose in Project                       |
| --------- | ---------- | --------------------------------------------- |
| **DES**   | Symmetric  | Performance comparison and encryption testing |
| **AES**   | Symmetric  | Performance comparison and encryption testing |
| **RSA**   | Asymmetric | Public/private key encryption comparison      |

The dashboard helps visualize how these algorithms differ in computational performance.

The comparison is useful for understanding that cryptographic algorithms are not identical in practical cost. Factors such as the algorithm type and operation being performed can affect execution time and computational requirements.

## Project Objectives

* Build a working real-time chat system using socket programming.
* Apply security concepts to a practical messaging application.
* Protect stored passwords using hashing instead of plaintext storage.
* Implement and experiment with DES, AES, and RSA.
* Measure and compare cryptographic performance.
* Present experimental results through a dashboard.
* Understand the trade-off between **security mechanisms and computational performance**.

## What I Learned

This project provided practical experience with:

* Python network/socket programming
* Client-server architecture
* User authentication
* Password hashing and secure storage concepts
* Symmetric vs. asymmetric cryptography
* Performance benchmarking
* Data analysis and visualization
* Applying Information Security concepts in a working application

## Disclaimer

This project was developed for **educational purposes** as part of an Information Security course. It is a learning project and should not be treated as a production-ready secure messaging application without further security review, testing, and hardening.

## Author

**Omaima Khan** 

**Noor Ul Huda**

Information Security Project Python Secure Chatting Application

