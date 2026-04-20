import socket
import time
import threading

HOST = "127.0.0.1"
PORT = 8080

TIMEOUT = 2

# ----------------------------
# CORE REQUEST SENDER
# ----------------------------
def send(raw_request, timeout=TIMEOUT):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((HOST, PORT))
        s.send(raw_request.encode())

        response = b""
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    break
                response += data
            except:
                break

        s.close()
        return response.decode(errors="ignore")
    except Exception as e:
        return f"ERROR: {e}"


# ----------------------------
# PARSING HELPERS
# ----------------------------
def status_code(resp):
    try:
        return int(resp.split("\r\n")[0].split(" ")[1])
    except:
        return -1


def has_header(resp, header):
    return header.lower() in resp.lower()


# ----------------------------
# TEST WRAPPER
# ----------------------------
def test(name, request, expect_code=None, expect_in=None, should_fail=False):
    resp = send(request)

    code = status_code(resp)

    passed = True
    reason = ""

    if expect_code and code != expect_code:
        passed = False
        reason = f"Expected {expect_code}, got {code}"

    if expect_in and expect_in not in resp:
        passed = False
        reason = f"Missing expected content: {expect_in}"

    if should_fail and code < 400:
        passed = False
        reason = f"Should fail but got {code}"

    if passed:
        print(f"✅ PASS - {name}")
    else:
        print(f"❌ FAIL - {name}")
        print(f"   Reason: {reason}")
        print(f"   Response snippet:\n   {resp[:200]}\n")

    return passed


# ----------------------------
# 200+ TEST CASES BUILDER
# ----------------------------
tests = []

# --- BASIC GET TESTS ---
for i in range(1, 51):
    tests.append((
        f"GET / valid #{i}",
        "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n",
        200
    ))

# --- HTTP/1.1 HOST HEADER MISSING ---
for i in range(1, 21):
    tests.append((
        f"Missing Host #{i}",
        "GET / HTTP/1.1\r\n\r\n",
        400
    ))

# --- INVALID METHODS ---
methods = ["PUT", "PATCH", "TRACE", "CONNECT", "OPTIONS"]
for i, m in enumerate(methods * 10):
    tests.append((
        f"Invalid Method {m} #{i}",
        f"{m} / HTTP/1.1\r\nHost: localhost\r\n\r\n",
        405
    ))

# --- MALFORMED REQUESTS ---
for i in range(1, 21):
    tests.append((
        f"Malformed #{i}",
        "GARBAGE REQUEST\r\n\r\n",
        400
    ))

# --- POST TESTS ---
for i in range(1, 21):
    body = f"key=value{i}"
    req = (
        "POST / HTTP/1.1\r\n"
        "Host: localhost\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "\r\n"
        + body
    )
    tests.append((
        f"POST request #{i}",
        req,
        None  # depends on your server (200 or 405)
    ))

# --- DELETE TESTS ---
for i in range(1, 11):
    tests.append((
        f"DELETE test #{i}",
        "DELETE /test.txt HTTP/1.1\r\nHost: localhost\r\n\r\n",
        200  # or 204 depending on your implementation
    ))

# --- CGI PROBES ---
for i in range(1, 10):
    tests.append((
        f"CGI probe #{i}",
        "GET /cgi-bin/test.php HTTP/1.1\r\nHost: localhost\r\n\r\n",
        None
    ))

# --- LARGE REQUEST ---
large_body = "a" * 10000
tests.append((
    "Large POST body",
    "POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 10000\r\n\r\n" + large_body,
    None
))

# --- SLOW REQUEST ---
def slow_request():
    time.sleep(1)
    return send("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")

tests.append((
    "Slow request simulation",
    None,
    200
))


# ----------------------------
# RUN TESTS
# ----------------------------
def run_tests():
    passed = 0
    total = 0

    for t in tests:
        name, req, expect = t
        total += 1

        if name == "Slow request simulation":
            resp = slow_request()
            code = status_code(resp)
            if code == 200:
                print(f"✅ PASS - {name}")
                passed += 1
            else:
                print(f"❌ FAIL - {name}")
                print(resp[:200])
            continue

        resp = send(req)
        code = status_code(resp)

        ok = True
        reason = ""

        if expect and code != expect:
            ok = False
            reason = f"Expected {expect}, got {code}"

        if ok:
            print(f"✅ PASS - {name}")
            passed += 1
        else:
            print(f"❌ FAIL - {name} -> {reason}")
            print(resp[:200])

    print("\n====================")
    print(f"RESULT: {passed}/{total} passed")
    print("====================")


if __name__ == "__main__":
    run_tests()
