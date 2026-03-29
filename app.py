import gradio as gr
def calculate_score(gpa, volunteer_hours, essay_score):
    score = gpa * 25 + volunteer_hours * 0.1 + essay_score * 0.5
    return score

def merge_sort(students):
    if len(students) <= 1:
        return students

    mid = len(students) // 2
    left_half = students[:mid]
    right_half = students[mid:]

    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    return merge(left_sorted, right_sorted)


def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i]["score"] > right[j]["score"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result

def process_students(students):
    for student in students:
        student["score"] = calculate_score(
            student["gpa"],
            student["volunteer_hours"],
            student["essay_score"]
        )

    sorted_students = merge_sort(students)

    output = "Scholarship Ranking:\n"
    output += "--------------------\n"

    rank = 1
    for student in sorted_students:
        output += str(rank) + ". " + student["name"] + " - " + str(student["score"]) + "\n"
        rank += 1

    output += "\nTop 3 Candidates:\n"
    output += "--------------------\n"

    for student in sorted_students[:3]:
        output += student["name"] + " - " + str(student["score"]) + "\n"

    return output

def parse_students_input(text):
    students = []

    if text.strip() == "":
        return "Error: input is empty."

    lines = text.strip().split("\n")

    for line in lines:
        parts = line.split(",")

        if len(parts) != 4:
            return "Error: each line must have 4 values: name, GPA, volunteer hours, essay score."

        name = parts[0].strip()

        try:
            gpa = float(parts[1].strip())
            volunteer_hours = float(parts[2].strip())
            essay_score = float(parts[3].strip())
        except:
            return "Error: GPA, volunteer hours, and essay score must be numbers."

        student = {
            "name": name,
            "gpa": gpa,
            "volunteer_hours": volunteer_hours,
            "essay_score": essay_score
        }

        students.append(student)

    return students

def run_app(text):
    students = parse_students_input(text)

    if type(students) == str:
        return students

    return process_students(students)

sample_input = """Alice,3.9,40,85
Bob,3.7,60,90
Cathy,4.0,20,88
David,3.6,80,75"""

demo = gr.Interface(
    fn=run_app,
    inputs=gr.Textbox(
        lines=10,
        label="Enter student data (name, GPA, volunteer hours, essay score)",
        value=sample_input
    ),
    outputs=gr.Textbox(
        lines=15,
        label="Scholarship Ranking Results"
    ),
    title="Scholarship Shortlist Organizer",
    description="Enter one student per line in this format: Name,GPA,Volunteer Hours,Essay Score"
)

demo.launch()
