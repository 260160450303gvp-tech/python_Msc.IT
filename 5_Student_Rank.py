students = {}

subjects = ["Python", "linux", "Data structure", "java", "Computer Network"]

n = int(input("Enter number of students: "))

for i in range(n):
    roll = input("Roll No: ")
    name = input("Name: ")

    marks = []
    for sub in subjects:
        marks.append(int(input("Enter " + sub + " mark: ")))

    total = sum(marks)
    per = total / 5

    if per >= 90:
        grade = "A"
    elif per >= 75:
        grade = "B"
    elif per >= 50:
        grade = "C"
    elif per >= 35:
        grade = "D"
    else:
        grade = "F"

    students[roll] = [name, total, per, grade]

data = sorted(students.items(), key=lambda x: x[1][1], reverse=True)

rank = 0
last = -1

print("\nRank\t Roll\t Name\t Total\t Percentage\t Grade\t")

for i, (roll, s) in enumerate(data):
    if s[1] != last:
        rank = i + 1

    print(rank,"\t", roll,"\t", s[0],"\t", s[1],"\t", s[2],"\t","\t", s[3])
    last = s[1]