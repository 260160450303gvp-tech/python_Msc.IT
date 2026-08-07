p= input("Enter paragraph: ")

w = p.split()

print("Total words:", len(w))
print("Unique words:", len(set(w)))
print("Longest word:", max(w, key=len))
print("Shortest word:", min(w, key=len))

print("Repeated words:")
for i in set(w):
    if w.count(i) > 1:
        print(i)