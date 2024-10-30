import os
import sys
import io

#This file function reads files from a specified folder path based on the given file type (A, B, or C) to then process each file 
#differently according to its type and stores the results in separate output files. 
def read_files(folder_path, file_type):
    #Ensure the folder path ends with a separator
    if not folder_path.endswith(os.path.sep):
        folder_path += os.path.sep

    #Get a list of all files in the folder
    files = os.listdir(folder_path)
    matching_files = [file for file in files if file[0].upper() == file_type.upper()]

    #Execute the content of each matching file
    for file_name in matching_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            file_content = file.read()
            print(type(file_content))
            

            if (file_type == 'A'):

                try:
                    #execute the operation and save the result
                    result = eval(file_content) 
                    print(f"File {file_name} operation [{file_content}] =  {result}")
                    
                    #Store the result of each file  
                    output_file_name = f"Codes/Files/LocalOutputs/Files_{file_type}/result_{file_name}"
                    with open(output_file_name, 'w') as file:
                        file.write(f'{result}')

                except Exception as e:
                    print(f"Error executing file {file_name}: {e}")

            elif (file_type == 'B'):
                try:
                    #execute the operation and save the result
                    result =  file_content[::-1]
                    print(f"File {file_name} \n word: {file_content} = {result}")
                    
                    #Store the result of each file  
                    output_file_name = f"Codes/Files/LocalOutputs/Files_{file_type}/result_{file_name}"
                    with open(output_file_name, 'w') as file:
                        file.write(f'{result}')

                except Exception as e:
                    print(f"Error executing file {file_name}: {e}")
            else:
                try:
                    #execute the operation and save the result
                    chunks = [file_content[i:i+8] for i in range(0, len(file_content), 8)]
                    # Convert each chunk to its decimal equivalent and then to ASCII
                    ascii_characters = [chr(int(chunk, 2)) for chunk in chunks]
                    result = ''.join(ascii_characters)
                    
                    print(f"File {file_name} \n Binary: {file_content} ASCII = {result}")
                    
                    #Store the result of each file  
                    output_file_name = f"Codes/Files/LocalOutputs/Files_{file_type}/result_{file_name}"
                    with open(output_file_name, 'w') as file:
                        file.write(f'{result}')

                except Exception as e:
                    print(f"Error executing file {file_name}: {e}")

#This is the user input block that prompts the user to choos the type of files to process
if __name__ == "__main__":

    #user input 
    f_type = ''
    while True:
        try:
            f_type = input('Choose the type of the folder you would like to see the results. \nOptions: \n 1. Type A (A) \n 2. Type B (B) \n 3. Type C (C) \n Please select the letter of your type: ').upper()
            if f_type not in ['A', 'B', 'C']:
                raise ValueError("Invalid input. Please enter 'A', 'B', or 'C'.")
            else:
                break
        except ValueError as e:
            print(f"Error: {e}")

    #Generate files
    folder_path = f'Codes/Files/Files_{f_type}'
    file_type = f_type
    read_files(folder_path, file_type)