import string
import socket
import threading
import random

# Define the host and port where your server will run
# define the number of questions and the time limit per question
NUM_QUESTIONS = 100
TIME_LIMIT = 25
HOST = '0.0.0.0'
PORT = 6969
FLAG = 'flag{I_4m_c4t_0f_1nt3rn3t}'

# Bash ASCII color codes
RED = '\033[91m'
PINK = '\033[95m'
ENDC = '\033[0m'
BLUE = '\033[1;34m'

# ASCII art of a red-pink cat with color codes
WELCOME_MESSAGE = f"""
{RED}
 /\_/\\                                                          /\_/\\
( o.o )                                                        ( o.o )
 > ^ <                                                          > ^ <

                      /^--^\     /^--^\     /^--^\\
                      \____/     \____/     \____/
                     /      \   /      \   /      \ 
                    |        | |        | |        |
                     \__  __/   \__  __/   \__  __/
|^|^|^|^|^|^|^|^|^|^|^|^\ \^|^|^|^/ /^|^|^|^|^\ \^|^|^|^|^|^|^|^|^|^|^|^|
| | | | | | | | | | | | |\ \| | |/ /| | | | | | \ \ | | | | | | | | | | |
| | | | | | | | | | | | / / | | |\ \| | | | | |/ /| | | | | | | | | | | |
| | | | | | | | | | | | \/| | | | \/| | | | | |\/ | | | | | | | | | | | |
#########################################################################
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |


{PINK}Welcome to the math quiz game! You will be asked 100 mathematical expressions.
Solve them correctly within 25 seconds to go to the next question. Good luck!
{ENDC}
"""

# Initialize a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(400)  # You can adjust the number of connections you want to allow

# List to keep track of connected clients
connected_clients = []

# Function to handle a client's connection
def handle_client(client_socket, client_IP, client_PORT):
    try:
        # Set a timeout for client connection
        client_socket.settimeout(TIME_LIMIT)

        # Add the client to the list of connected clients
        connected_clients.append(client_socket)

        # Send a welcome message to the client
        client_socket.send(WELCOME_MESSAGE.encode())
        # initialize the score and the question number
        score = 0
        question_num = 1



        while question_num <= NUM_QUESTIONS:
            # generate a random mathematical expression
            operators = ['+', '-', '*', '/']
            rand_expr = ''.join(random.choices(string.digits[1:], k=4))
            for _ in range(2):
                rand_expr += ' ' + random.choice(operators) + ' '
                rand_expr += ''.join(random.choices(string.digits[1:], k=4))
            rand_expr += ' ='

            # replace '+' with 'x' and add '=' at the end
            expr_with_operators = rand_expr.replace('*', 'x')

            # send the question to the client
            client_socket.send(f"Question {question_num}: What is the result of {expr_with_operators}\n".encode())
            # receive the answer from the client
            answer = client_socket.recv(1024).decode().strip()  # Adjust the buffer size as needed

            # evaluate the expression and check if the answer is correct
            try:
                correct_result = eval(rand_expr.replace('x', '*').replace('=', '').strip())
                if float(answer) == correct_result:
                    # increment the score and send a positive feedback
                    score += 1
                    # increment the question number
                    question_num += 1
                    client_socket.send(b"Correct!\n")
                    continue
                else:
                    # send a negative feedback then end the challenge
                    client_socket.send(f"Wrong! The correct answer is {correct_result}.\n".encode())
                    break
            except Exception as e:
                client_socket.send(f"Invalid expression. Please provide a valid mathematical expression.\n".encode())











        if score == NUM_QUESTIONS:
            client_socket.send(f"{BLUE}Congratulations! Here is your flag: {FLAG}{ENDC}\n".encode())

    except socket.timeout:
        client_socket.send(b"Time's up! You didn't answer within the time limit.\n")
        print(f"Client timed out at {client_IP}:{client_PORT}")
    except Exception as e:
        print(f"Error handling client: {str(e)}")
    finally:
        client_socket.close()
        print(f"Closed connection from {client_IP}:{client_PORT}")
        connected_clients.remove(client_socket)

# Main server loop
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address[0], client_address[1],))
    client_thread.start()
