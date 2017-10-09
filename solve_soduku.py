#!/usr/bin/env python
import string

def read_input_file(infile_name):
    lines = open(infile_name, 'r').readlines()
    actual_line_count = 0
    for curr_line in lines:
        split_line = curr_line.split('#')
        if len(split_line) > 1:
            curr_line = split_line[0]
        if not (curr_line.isspace() or curr_line == ''):
            actual_line_count += 1
            numbers_list = map(lambda x: int(x) if x.isdigit() else None, map(string.strip, curr_line.split()))
            for curr_value in numbers_list:
                assert (curr_value is None) or (1 <= curr_value <= 9)
            assert len(numbers_list) == 9
            print numbers_list
    assert actual_line_count == 9

if __name__== "__main__":
    read_input_file(infile_name="sample_input_medium.txt")