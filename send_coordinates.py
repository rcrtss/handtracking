# import os
# import time

# # Define the named pipe
# PIPE_NAME = 'coordinates_pipe'

# # Create the named pipe if it doesn't exist
# if not os.path.exists(PIPE_NAME):
#     os.mkfifo(PIPE_NAME)

# # Open the named pipe for writing
# pipeout = os.open(PIPE_NAME, os.O_WRONLY)

# # Loop to send coordinates every 0.1 seconds
# while True:
#     # Send the coordinates as a string
#     lock.acquire()
#     x = x_global
#     y = y_global
#     lock.release()
#     coordinates = f"{x},{y}"
#     os.write(pipeout, coordinates.encode())
#     time.sleep(0.1)
# # Close the named pipe
# os.close(pipeout)

def send_coordinates(x,y):
    print(x,",",y)