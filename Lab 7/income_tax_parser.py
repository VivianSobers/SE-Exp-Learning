import re


def clean_pan(pan):
    """
    Return a cleaned PAN string or None.
    Accepts only strings, removes all whitespace, upper-cases, and validates
    exactly 5 ASCII letters + 4 ASCII digits + 1 ASCII letter.
    """
    if not isinstance(pan, str):
        return None
    cleaned = re.sub(r"\s+", "", pan)
    if not cleaned.isascii():
        return None
    cleaned = cleaned.upper()
    if re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", cleaned):
        return cleaned
    return None

def parse_amount(text):
    """
    Return an integer amount or None.
    Accepts only strings, strips an optional leading Rs/Rs./₹ prefix, removes
    commas and whitespace, and parses only 1..15 ASCII digits.
    """
    if not isinstance(text, str):
        return None
    cleaned = text.strip()
    cleaned = re.sub(r"^(?:rs\.?|₹)\s*", "", cleaned, count=1, flags=re.IGNORECASE)
    cleaned = re.sub(r"[\s,]+", "", cleaned)
    if not re.fullmatch(r"[0-9]{1,15}", cleaned):
        return None
    return int(cleaned)

def parse_tax_slab(line):
    """
    Return (low, high, rate) as integers or None.
    Accepts only strings matching LOW-HIGH:RATE with optional surrounding
    spaces; each number uses ASCII digits. Returns None if low > high or
    rate is outside 0..100.
    """
    if not isinstance(line, str):
        return None
    match = re.fullmatch(r"\s*([0-9]{1,15})\s*-\s*([0-9]{1,15})\s*:\s*([0-9]{1,3})\s*", line)
    if not match:
        return None
    low = int(match.group(1))
    high = int(match.group(2))
    rate = int(match.group(3))
    if low > high or not (0 <= rate <= 100):
        return None
    return (low, high, rate)

def main():
    def safe_input(prompt):
        try:
            return input(prompt)
        except EOFError:
            return ""

    print("==== Running clean_pan ====")
    value = safe_input("Enter a PAN (e.g. abcde 1234f): ")
    result = clean_pan(value)
    if result is None:
        print("Invalid PAN")
    else:
        print("Cleaned PAN:", result)

    print("\n==== Running parse_amount ====")
    value = safe_input("Enter an amount (e.g. Rs 12,50,000): ")
    result = parse_amount(value)
    if result is None:
        print("Invalid amount")
    else:
        print("Amount in rupees:", result)

    print("\n==== Running parse_tax_slab ====")
    value = safe_input("Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): ")
    result = parse_tax_slab(value)
    if result is None:
        print("Invalid tax slab")
    else:
        print("Tax slab (low, high, rate):", result)

if __name__ == "__main__":
    main()
