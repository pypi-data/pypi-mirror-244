import tkinter as tk
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
import re
import csv
from datetime import datetime

def highlight_changes(old_str, new_str) -> None:
    highlighted_str = ""

    for old_char, new_char in zip(old_str, new_str):
        if old_char != new_char:
            highlighted_str += f"\033[91m{new_char}\033[0m"  # Red color for additions
        else:
            highlighted_str += old_char

    # Handle remaining characters if one string is longer than the other
    if len(new_str) > len(old_str):
        highlighted_str += f"\033[91m{new_str[len(old_str):].replace(' ', '␣')}\033[0m"

    print(f"-: {old_str.replace(' ', '␣')} -> {new_str.replace(' ', '␣')} +: {highlighted_str}")

def get_file_path() -> str:
    app = QApplication(sys.argv)

    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options
    )

    if file_path:
        return file_path
    else:
        return None


def get_output_file_path(input_file: str) -> str:
    # Pattern to match the 'output-N' format at the end of the file name
    pattern = r'output-(\d+)'

    # Check if the input file name contains 'output-N' format
    match = re.search(pattern, input_file)
    if match:
        # Extract the version number and increment it
        version = int(match.group(1)) + 1
        output_file = re.sub(pattern, f'output-{version}', input_file)
    else:
        # If 'output-N' format is not found, add it with version 1 before the file extension
        base, ext = input_file.rsplit('.', 1)
        output_file = f"{base}-output-1.{ext}"

    return output_file

def get_column_index(column_name: str) -> int:
    while True:
        try: 
            index = int(input(f"Enter the index of the {column_name} column: "))
            return index-1
        except ValueError:
            print("Invalid value. Please try again.")

def clean_spaces(input_file: str, output_file: str) -> None:
    with open(input_file, 'r') as input_csv:
        with open(output_file, 'w') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.writer(output_csv)
            for row in reader:
                new_row = []
                for cell in row:
                    original_cell = cell
                    new_cell = cell.strip()
                    new_cell = re.sub(' +', ' ', new_cell)
                    new_row.append(new_cell)
                    highlight_changes(original_cell, new_cell)
                writer.writerow(new_row)


def clean_pipes(input_file: str, output_file: str) -> None:
    with open(input_file, 'r') as input_csv:
        with open(output_file, 'w') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.writer(output_csv)
            for row in reader:
                new_row = []
                for cell in row:
                    original_cell = cell
                    new_cell = original_cell.replace(' |', '|').replace('| ', '|')
                    new_row.append(new_cell)
                    highlight_changes(original_cell, new_cell)
                writer.writerow(new_row)

def clean_dates(input_file: str, output_file: str) -> None:
    # date_column_index = get_column_index("date")
    # known_formats = {
    #     r'\d{4}-\d{2}-\d{2}': None,  # YYYY-MM-DD is a correct format
    #     r'\d{4}-\d{2}': None,  # YYYY-MM is a correct format 
    #     r'\d{4}-\d{4}': None,  # YYYY-YYYY is a correct format
    #     r'\d{4}': None,  # YYYY is a correct format

        
    # }

    # with open(input_file, 'r') as input_csv:
    #     with open(output_file, 'w') as output_csv:
    #         reader = csv.reader(input_csv)
    #         writer = csv.writer(output_csv)
    #         for row_index, row in enumerate(reader):
    #             new_row = []
    #             for cell_index, cell in enumerate(row):
    #                 if cell_index == date_column_index:
    #                     original_cell = cell
    #                     found_match = False
    #                     for pattern, conversion in known_formats.items():
    #                         if re.fullmatch(pattern, cell):
    #                             if conversion is not None:
    #                                 cell = datetime.strptime(cell, conversion).strftime(conversion)
    #                             found_match = True
    #                             break
    #                     if not found_match:
    #                         print(f"I've found a value that I don't know how to handle. The cell is " 
    #                             f"in positions {row_index+1}, {cell_index+1}. the cell is {cell}")
    #                         if input("Would you like to change this manually? (y/n): ").lower() == "y":
    #                             cell = input("Enter the new value: ").strip()
    #                         else:
    #                             print("I'll keep the original value.")
    #                             cell = original_cell
    #                     else:
    #                         highlight_changes(original_cell, cell)
    #                     new_row.append(cell)
    #             writer.writerow(new_row)
    # print("Those dates do be looking clean. Nice job!")
    pass

def clean_titles(input_file: str, output_file: str) -> None:
    title_column_index = get_column_index("title")
    articles = [
        "a",
        "abaft",
        "aboard",
        "about",
        "above",
        "absent",
        "across",
        "afore",
        "after",
        "against",
        "along",
        "alongside",
        "amid",
        "amidst",
        "among",
        "amongst",
        "an",
        "anenst",
        "apropos",
        "apud",
        "around",
        "as",
        "aside",
        "astride",
        "at",
        "athwart",
        "atop",
        "barring",
        "before",
        "behind",
        "below",
        "beneath",
        "beside",
        "besides",
        "between",
        "beyond",
        "but",
        "by",
        "circa",
        "concerning",
        "despite",
        "down",
        "during",
        "except",
        "excluding",
        "failing",
        "following",
        "for",
        "forenenst",
        "from",
        "given",
        "in",
        "including",
        "inside",
        "into",
        "lest",
        "like",
        "mid",
        "midst",
        "minus",
        "modulo",
        "near",
        "next",
        "notwithstanding",
        "of",
        "off",
        "on",
        "onto",
        "opposite",
        "out",
        "outside",
        "over",
        "pace",
        "past",
        "per",
        "plus",
        "pro",
        "qua",
        "regarding",
        "round",
        "sans",
        "save",
        "since",
        "than",
        "the",
        "through",
        "throughout",
        "till",
        "times",
        "to",
        "toward",
        "towards",
        "under",
        "underneath",
        "unlike",
        "until",
        "unto",
        "up",
        "upon",
        "versus",
        "via",
        "vice",
        "with",
        "within",
        "without",
        "worth"
    ]
    with open(input_file, 'r') as input_csv:
        with open(output_file, 'w') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.writer(output_csv)
            for row_index, row in enumerate(reader):
                new_row = []
                for cell_index, cell in enumerate(row):
                    if cell_index == title_column_index:
                        original_cell = cell
                        new_cell = cell.strip()
                        for word_index, word in enumerate(new_cell.split()):
                            if word_index == 0 or word not in articles:
                                new_cell = new_cell.replace(word, word.capitalize())
                            else :
                                new_cell = new_cell.replace(word, word.lower())
                        if new_cell != original_cell:
                            highlight_changes(original_cell, new_cell)
                        new_row.append(new_cell)
        print("Titles are now capitalized.")

def clean_pages(input_file: str, output_file: str) -> None: 
    page_column_index = get_column_index("page")
    with open(input_file, 'r') as input_csv:
        with open(output_file, 'w') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.reader(output_csv)
            for row_index, row in enumerate(reader):
                new_row = []
                for cell_index, cell in enumerate(row):
                    if cell_index == page_column_index:
                        original_cell = cell
                        new_cell = cell.strip()
                        # Use a regular expression to extract the page number format
                        page_number_pattern_match = re.search(r'(\d+)(?:\s*-\s*(\d+))?', new_cell)
                       
                        if page_number_pattern_match:
                           # Reconstruct the cell with cleaned page number format
                            start_page, end_page = page_number_pattern_match.groups()
                            if end_page:
                                cell = f"{start_page}-{end_page}"
                            else:
                                cell = start_page
                    if cell != original_cell:
                        highlight_changes(original_cell, cell)
                    new_row.append(new_cell)
                writer.writerow(new_row)
    print("Pages are now clean.")


    


                                        
                                    
                                    




