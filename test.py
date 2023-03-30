import whois # pip install python-whoisdef is_registered(domain_name):
def is_registered(domain_name):
    """
    A function that returns a boolean indicating 
    whether a `domain_name` is registered
    """
    try:
        w = whois.query(domain_name)
        # print(w.registrant)
    except Exception:
        return False
    else:
        return bool(w.name)
if __name__ == "__main__":
    test =  'kmoz.dev'
    result = is_registered(test)
    print(f"results: {result}")