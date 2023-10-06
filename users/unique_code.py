from datetime import datetime

def generate_unique_code():
    now = datetime.now()
    unique_code = now.strftime("%Y%m%d%H%M%S")
    return unique_code