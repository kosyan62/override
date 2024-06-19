# Stack variables:
data = ["756e505234376848",
        "45414a3561733951",
        "377a7143574e6758",
        "354a35686e475873",
        "48336750664b394d"]

result = []
for dword in data:
    reversed_result = []
    for i in range(8):
        num = dword[i * 2: (i + 1) * 2]  # Get 2 chars from string
        reversed_result.append(chr(int(num, 16)))  # Convert hex to int and then to char
    # We should remember about big/little endian int, so adding letters in reversed order from uniq integer
    result += reversed_result[::-1]
print("".join(result))
