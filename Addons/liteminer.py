import hashlib
import time

def Mine(hash_, a, diff):
    
    hashingStartTime = time.perf_counter()
    base_hash = hashlib.sha1(str(a).encode('ascii'))
    temp_hash = None
    device = "cpu"
    for result in range(100 * int(diff) + 1):
        temp_hash = base_hash.copy()
        temp_hash.update(str(result).encode('ascii'))
        ducos1 = temp_hash.hexdigest()
        
        if hash_ == ducos1:
            hashingStopTime = time.perf_counter()
            timeDifference = hashingStopTime - hashingStartTime
            if timeDifference == 0:
                hashrate = float('inf')
            else:
                hashrate = result / timeDifference
            return [result, hashrate, device]
    return [0, 0, device]
