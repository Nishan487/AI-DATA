def find_largest(numbers_list)->list:
    if not numbers_list:
        return None
    largest = numbers_list[0]
    for num in numbers_list:
        if num > largest:
            largest = num
    return largest
if __name__ == "__main__":
    numbers = input("Enter a list of numbers separated by spaces: ")
    numbers_list = [float(num) for num in numbers.split()]
    largest_number = find_largest(numbers_list)
    print(f"The largest number is: {largest_number}")