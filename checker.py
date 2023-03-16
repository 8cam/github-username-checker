import requests
import colorama
from colorama import Fore, Back, Style, init
import time
import threading
from multiprocessing.pool import ThreadPool

def check_username(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return False  # Username is taken
    elif response.status_code == 404:
        return True   # Username is available
    else:
        raise Exception(f"Unexpected status code: {response.status_code}")

def check_usernames(usernames_to_check):
    results = {}
    for username in usernames_to_check:
        try:
            is_available = check_username(username)
            if is_available:
                results[username] = True
            else:
                results[username] = False
        except Exception as e:
            results[username] = None
            print(Fore.MAGENTA + "[/] " + Fore.WHITE +  f"Error checking username {username}: {e}")
    return results

def check_usernames_threaded(usernames_to_check):
    pool = ThreadPool(10)
    chunks = [usernames_to_check[i:i+10] for i in range(0, len(usernames_to_check), 10)]
    results = {}
    for chunk in chunks:
        thread_results = pool.map(check_username, chunk)
        for i, username in enumerate(chunk):
            is_available = thread_results[i]
            if is_available:
                results[username] = True
            else:
                results[username] = False
    return results

def check_usernames_multiprocess(usernames_to_check):
    pool = multiprocessing.Pool(processes=4)
    chunks = [usernames_to_check[i:i+10] for i in range(0, len(usernames_to_check), 10)]
    results = {}
    for chunk in chunks:
        process_results = pool.map(check_username, chunk)
        for i, username in enumerate(chunk):
            is_available = process_results[i]
            if is_available:
                results[username] = True
            else:
                results[username] = False
    return results

def main():
    with open("usernames.txt", "r") as f:
        usernames_to_check = f.read().splitlines()

    init()  # Initialize Colorama for colored output

    print("Checking GitHub usernames...")
    
    start_time = time.monotonic()
    results = check_usernames(usernames_to_check)
    end_time = time.monotonic()

    print(f"Checked {len(usernames_to_check)} usernames in {end_time - start_time:.2f} seconds")

    for username, is_available in results.items():
        if is_available:
            print(Fore.GREEN + "[+] " + Fore.WHITE + f"{username} is available!")
        else:
            print(Fore.RED + "[-] " + Fore.WHITE + f"{username} is already taken.")

    print("Threaded version:")

    start_time = time.monotonic()
    results_threaded = check_usernames_threaded(usernames_to_check)
    end_time = time.monotonic()

    print(f"Checked {len(usernames_to_check)} usernames in {end_time - start_time:.2f} seconds")

    for username, is_available in results_threaded.items():
        if is_available:
            print(Fore.GREEN + f"{username} is available!")
        else:
            print(Fore.RED + f"{username} is already taken.")

if __name__ == "__main__":
    main()