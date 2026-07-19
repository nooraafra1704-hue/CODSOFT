import sys
import io
# Force UTF-8 encoding for standard output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from chatbot import get_chatbot_response

def run_tests():
    # Test cases: (input, expected_intent_response_keyword, should_be_exit)
    tests = [
        ("hi", "hello", False),
        ("hello there", "hello", False),
        ("how are you", "doing", False),
        ("what is your name", "aegis", False),
        ("who created you", "internship", False),
        ("what is artificial intelligence", "computer science", False),
        ("tell me about python", "popular", False),
        ("what is codsoft", "internship", False),
        ("what is the time", "today is", False),
        ("help", "try asking", False),
        ("bye", "goodbye", True),
        ("unknown query 123", "sorry", False)
    ]
    
    success = True
    for idx, (inp, kw, expected_exit) in enumerate(tests):
        resp, is_exit = get_chatbot_response(inp)
        resp_lower = resp.lower()
        
        if kw == "sorry":
            match = any(x in resp_lower for x in ["sorry", "outside", "oops", "not sure", "couldn't match"])
        elif kw == "popular":
            match = any(x in resp_lower for x in ["high-level", "popular", "written in python"])
        elif kw == "goodbye":
            match = any(x in resp_lower for x in ["goodbye", "bye", "farewell"])
        elif kw == "hello":
            match = any(x in resp_lower for x in ["hello", "hi", "hey"])
        elif kw == "doing":
            match = any(x in resp_lower for x in ["doing", "efficiency", "great"])
        elif kw == "aegis":
            match = "aegis" in resp_lower
        elif kw == "internship":
            # Match if response contains any of the keywords related to internship or codsoft response
            match = any(x in resp_lower for x in ["internship", "developer", "built", "created", "codsoft"])
        elif kw == "computer science":
            match = any(x in resp_lower for x in ["computer science", "artificial intelligence", "transforming", "fascinating"])
        else:
            match = kw in resp_lower
            
        exit_match = (is_exit == expected_exit)
        
        if not match or not exit_match:
            print(f"[FAIL] Test {idx+1} failed for input '{inp}':")
            print(f"   Expected keyword: '{kw}' (Match: {match})")
            print(f"   Response: '{resp}'")
            print(f"   Expected Exit: {expected_exit}, Got: {is_exit}")
            success = False
        else:
            print(f"[OK] Test {idx+1} passed for input '{inp}'")
            
    if success:
        print("\nAll local chatbot verification tests passed successfully!")
        exit(0)
    else:
        print("\nSome tests failed. Please review chatbot.py.")
        exit(1)

if __name__ == "__main__":
    run_tests()
