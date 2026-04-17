def calculate_grade(marks):
    try:
        if marks < 0 or marks > 100:
            return "Marks should be between 0 and 100."
        elif marks >= 90:
            return "A"
        elif marks >= 80:
            return "B"
        elif marks >= 70:
            return "C"
        elif marks >= 60:
            return "D"
        else:
            return "F"
    except ValueError:
        return "Invalid input. Please enter a number."
    

if __name__ == "__main__":
    marks = float(input("Enter the marks: "))
    grade = calculate_grade(marks)
    print(f"The grade is: {grade}")

