def count_word(file_name):
    try:
        with open(file_name, 'r') as f:
            text=f.read()
            word = text.split()
            word_count=len(word)
            return word_count
    except FileNotFoundError:
        return "File not found. Please check the file path and try again."
    
if __name__ == "__main__":
    file_Name = input("Enter the file Name: ")
    count = count_word(file_Name)
    print(f"The number of words in the file is: {count}")