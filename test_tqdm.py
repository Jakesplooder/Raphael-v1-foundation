import sys
try:
    sys.stderr.write('\r\u2588')
    sys.stderr.flush()
    print("Success")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")
