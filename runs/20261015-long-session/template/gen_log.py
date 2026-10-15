"""Writes data/log.txt: 600 lines of a fake service log (fixed seed, so every run gets the same file)."""
import os, random
random.seed(7)
os.makedirs("data", exist_ok=True)
levels = ["INFO"] * 8 + ["WARN"] * 2 + ["ERROR"]
msgs = ["request served", "cache miss", "retrying upstream", "slow query", "user login", "token refreshed",
        "disk 81% full", "timeout talking to billing", "schema mismatch in event", "connection reset by peer"]
with open("data/log.txt", "w") as f:
    for i in range(600):
        f.write(f"2026-10-15T08:{i // 60:02d}:{i % 60:02d}Z {random.choice(levels):5} svc-{random.randint(1, 4)} "
                f"{random.choice(msgs)} id={random.randint(1000, 9999)}\n")
