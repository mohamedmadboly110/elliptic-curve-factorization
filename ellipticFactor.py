import random
import math

def is_prime(n):
    """
    Pre-computation Check 1: 
    Verifies if the number is prime using trial division up to sqrt(n).
    ECM will not run if this returns True.
    """
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def is_perfect_power(n):
    """
    Pre-computation Check 2:
    ECM mathematically fails if the integer is a perfect power (like x^2, x^3).
    This function detects if 'n' can be written as a^b.
    """
    for b in range(2, int(math.log2(n)) + 1):
        a = round(n ** (1.0 / b))
        if a ** b == n:
            return True, a
    return False, n

def gcd(a, b):
    """Standard Greatest Common Divisor."""
    while b:
        a, b = b, a % b
    return a

def modular_inverse(a, m):
    """
    The core trap of Lenstra's ECM:
    Computes modular inverse. If gcd(a, m) != 1, the inverse fails,
    and the GCD found IS the non-trivial prime factor of our number!
    """
    if a == 0: return None
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None  # Signal that a factor is trapped inside 'g'
    return x % m

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def elliptic_add_and_double(P, Q, a, n):
    """
    Standard Elliptic Curve Arithmetic (Standard Affine Coordinates).
    y^2 = x^3 + ax + b (mod n)
    
    If addition or doubling fails due to a missing modular inverse, 
    the trapped factor is returned immediately as an integer.
    """
    if P is None: return Q
    if Q is None: return P
    
    x1, y1 = P
    x2, y2 = Q
    
    # Checking for point at infinity
    if x1 == x2 and (y1 + y2) % n == 0:
        return None  
    
    # Slope (lambda) calculation
    if x1 != x2:
        # Point Addition Formula
        num = (y2 - y1) % n
        denom = (x2 - x1) % n
        inv = modular_inverse(denom, n)
        if inv is None:
            return gcd(denom, n)  # Breakthrough: Factor found!
        lam = (num * inv) % n
    else:
        # Point Doubling Formula (P == Q)
        num = (3 * x1 * x1 + a) % n
        denom = (2 * y1) % n
        inv = modular_inverse(denom, n)
        if inv is None:
            return gcd(denom, n)  # Breakthrough: Factor found!
        lam = (num * inv) % n
        
    # Resulting point coordinates
    x3 = (lam * lam - x1 - x2) % n
    y3 = (lam * (x1 - x3) - y1) % n
    return (x3, y3)

def elliptic_scalar_multiply(k, P, a, n):
    """Coordinates the scalar multiplication k*P using standard Double-and-Add."""
    Q = None
    R = P
    while k > 0:
        if k % 2 == 1:
            Q = elliptic_add_and_double(Q, R, a, n)
            if isinstance(Q, int): return Q  # Bubble up the factor
        R = elliptic_add_and_double(R, R, a, n)
        if isinstance(R, int): return R      # Bubble up the factor
        k //= 2
    return Q

def lenstra_ecm_algorithm(n, max_curves=1000, B=2000):
    """
    Main ECM Engine following the same architecture as the GitHub repository
    but using simplified affine coordinates.
    """
    # 1. Quick initial trial division for small primes (2 and 3)
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    
    # 2. Iterate over random elliptic curves
    for curve_count in range(max_curves):
        x1 = random.randint(1, n-1)
        y1 = random.randint(1, n-1)
        a = random.randint(1, n-1)
        
        # y^2 = x^3 + ax + b  =>  b = y^2 - x^3 - ax
        b = (y1*y1 - x1*x1*x1 - a*x1) % n
        
        # Non-singularity condition: 4a^3 + 27b^2 != 0
        discriminant = (4 * a*a*a + 27 * b*b) % n
        g = gcd(discriminant, n)
        if g == n:
            continue
        elif g > 1:
            return g  # Lucky factor from discriminant
            
        P = (x1, y1)
        
        # Stage 1: Compute scalar multiplication up to bound B
        for i in range(2, B):
            P = elliptic_scalar_multiply(i, P, a, n)
            if isinstance(P, int):  
                if P != 1 and P != n:
                    return P  # Successful non-trivial factor extraction
                break 
                
    return None

# --- Main Execution Interface ---
if __name__ == "__main__":
    print("=" * 60)
    print("   Lenstra's ECM Factoring Engine (Standard Affine Mode)   ")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nEnter a composite number to factorize: ")
            number = int(user_input)
            
            if number <= 1:
                print("❌ Error: Number must be greater than 1.")
                continue
                
            # GitHub Feature 1: Primality testing validation
            if is_prime(number):
                print(f"⚠️  {number} is a PRIME number. ECM cannot decompose primes.")
                continue
                
            # GitHub Feature 2: Perfect Power Pre-check
            is_power, base = is_perfect_power(number)
            if is_power:
                print(f"🎉 Factorization Successful (via Perfect Power Check)!")
                print(f"👉 Perfect Power Detected: {base} to some power equals {number}")
                break
                
            print(f"[+] Spawning normal affine curves to analyze {number}...")
            factor = lenstra_ecm_algorithm(number)
            
            if factor:
                other_factor = number // factor
                print("-" * 60)
                print(f"🎉 Factorization Successful (via Elliptic Curve breakdown)!")
                print(f"👉 First Factor : {factor}")
                print(f"👉 Second Factor: {other_factor}")
                print(f"✅ Verification : {factor} * {other_factor} = {number}")
                print("-" * 60)
                break
            else:
                print("\n❌ Bounds exhausted. No factors found. Try increasing B.")
                break
                
        except ValueError:
            print("❌ Error: Please enter numerical digits only.")