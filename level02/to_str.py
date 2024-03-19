data = ["756e505234376848", 
        "45414a3561733951",
        "377a7143574e6758",
        "354a35686e475873",
        "48336750664b394d"]

result = []
for e in data:
    rev = []
    for i in range(8):
        num = e[i * 2: (i + 1) *2]
        rev.append(chr(int(num, 16)))
    # We should remember about big/little endian int, so adding letters in reversed order from uniq integer
    result += rev[::-1]
print("".join(result))

