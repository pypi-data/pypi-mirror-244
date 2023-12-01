import logging

def decimal_to_binary(n):
    return bin(n).replace("0b", "")

def binary_to_decimal(b):
    return int(b, 2)

def hex_to_decimal(h):
    return int(h, 16)
def extract_bits(binary, num_bits):
    return binary[:num_bits]

def getGnbId(h):

    decimal_num = hex_to_decimal(h)
    binary_num = decimal_to_binary(decimal_num)

    # Extract first 22 bits
    extracted_bits = extract_bits(binary_num, 19)
    # Convert extracted bits back to decimal
    decimal_again = binary_to_decimal(extracted_bits)
    logging.debug(f"The decimal representation of the first 22 bits is {decimal_again}")
    return decimal_again