students = {}

subjects = ["Python", "linux", "Data structure", "java", "Computer Network"]

n = int(input("Enter number of students (minimum 5): "))

while n < 5:
    print("Please enter at least 5 students.")
    n = int(input("Enter number of students (minimum 5): "))

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
    elif per >= 80:
        grade = "B"
    elif per >= 70:
        grade = "C"
    elif per >= 50:
        grade = "D"
    else:
        grade = "F"

    students[roll] = [name, total, per, grade]

data = sorted(students.items(), key=lambda x: x[1][1], reverse=True)

rank = 0
last = -1

print("\nRoll\tName\tTotal\tPercentage\tGrade\trank")

for i, (roll, s) in enumerate(data):

    if s[1] != last:
        rank = i + 1

    print(roll, "\t", s[0], "\t", s[1], "\t", s[2], "\t\t", s[3],"\t",rank)

    last = s[1]
    
