#!/usr/bin/env python


def clean(input):
    if input == 'X':
        return None
    assert 1 <= int(input) <= 9
    return input


def read_puzzle(file_name):
    values = []
    for line in open(file_name, "r").xreadlines():
        line_without_comment = line.split("#")[0].strip()
        if not(line_without_comment == '' or line_without_comment.isspace()):
            line_values = map(clean, line_without_comment.split())
            assert len(line_values) == 9
            values.append(line_values)
            assert len(values) <= 9
    return values

if  __name__ =='__main__':
    puzzle = read_puzzle('sample_medium.txt')
    solution = read_puzzle('sample_medium_solution.txt')

    print "Puzzle:"
    print puzzle

    print "Solution:"
    print solution