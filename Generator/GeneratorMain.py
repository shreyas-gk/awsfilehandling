#This file is in charge of housing the functions to generate random .txt files type A, B and C by importing the random 
#library and nltk for word generation
import random
import nltk #library of words 

#This function generates random simple mathematical equations. 
def generate_type_a_file():
    #Generate mathematical equations with whole numbers, plus, minus, and division operators
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = random.randint(1, 100)
    operations = ['+', '-', '/', '*' ]
    equation = f"{a}{random.choice(operations)}{b}{random.choice(operations)}{c}{random.choice(operations)}{random.randint(1, 100)}\n"
    return equation

#This function generates random simple inverted words.
def generate_type_b_file():
    nltk.download('words')
    #Get the list of English words
    word_list = nltk.corpus.words.words()
    random_word = random.choice(word_list)
    reversed_word = random_word[::-1] + '\n'
    return reversed_word

#This function generates random binary code. 
def generate_type_c_file():
    #Generate binary and convert it to ASCII
    while True:
        longitud = random.choice(range(64))

        if (longitud % 8 == 0):
            binary_string = ''.join([random.choice(['0', '1']) for _ in range(longitud)])
            return binary_string

#This function invokes the functions above to participate generating files
def generate_files(num_files, file_type):
    if file_type == 'A':
        generator_func = generate_type_a_file
    elif file_type == 'B':
        generator_func = generate_type_b_file
    elif file_type == 'C':
        generator_func = generate_type_c_file
    else:
        raise ValueError("Invalid file type")

    for i in range(1, num_files + 1):
        file_content = generator_func()
        file_name = f"Codes/Files/Files_{file_type}/{file_type}_file_{i}.txt"
        with open(file_name, 'w') as file:
            file.write(file_content)

#This is the function acts as a controller that manages all the previous functions to generate the files. 
def mainGenerator():
        
        n_files = 0
        f_type = ''
        while True:
            try:
                n_files = int(input('Enter the Number of Files to generate: '))
                f_type = input('Choose the type of the file you would like to generate. \nOptions: \n 1. Type A (A) \n 2. Type B (B) \n 3. Type C (C) \n Please select the letter of your type: ').upper()
                if n_files <= 0:
                    raise ValueError("Invalid input. Please enter a number greater than 0")
                elif f_type not in ['A', 'B', 'C']: 
                    raise ValueError("Invalid input. Please enter 'A', 'B', or 'C'.")
                else:
                    break
            except ValueError as e:
                print(f"Error: {e}")

        #Generate files
        generate_files(n_files, f_type)
        print(f"{n_files}, {f_type}")

