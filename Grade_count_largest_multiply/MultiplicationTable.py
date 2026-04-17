def MultiplicationTable(num):
    try:
        for i in range(1, 11):
           multiplication = num * i
           multiplication_table = f"{num} x {i} = {multiplication}"
           print(multiplication_table)     
    except Exception as e:
        return f"An error occurred: {e}"
    
if __name__ == "__main__":
    number = int(input("Enter a number to make multiplication table: "))
    table = MultiplicationTable(number)
    print(table)