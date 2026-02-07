import random
import string

def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    """
    Generate a secure password with specified criteria.
    
    Args:
        length (int): Length of the password (default 12)
        use_upper (bool): Include uppercase letters
        use_lower (bool): Include lowercase letters
        use_digits (bool): Include digits
        use_symbols (bool): Include symbols
    
    Returns:
        str: Generated password
    """
    if length < 1:
        raise ValueError("Password length must be at least 1")
    
    char_pool = ''
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation
    
    if not char_pool:
        raise ValueError("At least one character type must be selected")
    
    # Ensure at least one character from each selected type
    password = []
    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password.append(random.choice(string.ascii_lowercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_symbols:
        password.append(random.choice(string.punctuation))
    
    # Fill the rest of the password
    while len(password) < length:
        password.append(random.choice(char_pool))
    
    random.shuffle(password)
    return ''.join(password)

# Example usage
if __name__ == "__main__":
    print("Generated password:", generate_password(16))
