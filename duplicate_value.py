number = (input("enter a numbers:"))

duplicate = []

for i in range(len(number) - 1):
    if number[i] == number[i + 1] and number[i] not in duplicate:
        duplicate.append(number[i])

print("Repeated consecutive numbers:", duplicate)