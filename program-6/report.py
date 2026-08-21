import csv

def display_students(students):

    print("\nIndex | Roll No | Name | Total | Percentage | Grade")
    print("-" * 60)

    index = 1

    for student in students:

        print(
            index, "|",
            student[0], "|",
            student[1], "|",
            student[2], "|",
            round(student[3], 2), "|",
            student[4]
        )

        index = index + 1


def save_ranked_csv(students):

    file = open("ranked_students.csv", "w", newline="")

    writer = csv.writer(file)

    writer.writerow([
        "Index", "Roll No", "Name",
        "Total", "Percentage", "Grade"
    ])

    index = 1

    for student in students:

        writer.writerow([
            index,
            student[0],
            student[1],
            student[2],
            round(student[3], 2),
            student[4]
        ])

        index = index + 1

    file.close()
