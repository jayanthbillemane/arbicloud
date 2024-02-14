import requests
import json
import threading
import time

URL = "http://0.0.0.0:5000/tasks/1"
PAYLOAD = {
    "name": "jayanth",
    "image": "final"
}

def send_request():
    while True:
        try:
            response = requests.post(URL, json=PAYLOAD)
            print("Response:", response.text)
        except Exception as e:
            print("Exception occurred:", e)
        time.sleep(0.01)  # Adjust this value to achieve 100 requests per second

def main():
    threads = []
    for _ in range(100):
        thread = threading.Thread(target=send_request)
        thread.daemon = True
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()



# import multiprocessing
# import time

# # Define a function to be executed by each process
# def print_numbers(process_id):
#     for i in range(5):
#         print(f"Process {process_id}: {i}")
#         time.sleep(1)

# if __name__ == "__main__":
#     # Create multiple processes
#     processes = []
#     for i in range(3):
#         process = multiprocessing.Process(target=print_numbers, args=(i,))
#         process.start()
#         processes.append(process)

#     # Wait for all processes to finish
#     for process in processes:
#         process.join()

#     print("All processes have finished execution.")



# # Define a function to be executed by each thread
# def print_numbers():
#     for i in range(5):
#         print(f"Thread {threading.current_thread().name}: {i}")
#         time.sleep(1)

# # Create multiple threads
# threads = []
# for i in range(3):
#     thread = threading.Thread(target=print_numbers)
#     thread.start()
#     threads.append(thread)

# # Wait for all threads to finish
# for thread in threads:
#     print("thread",thread)
#     thread.join()

# print("All threads have finished execution.")
