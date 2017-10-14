#!/usr/bin/env python


def clean(input):
    if input == 'X':
        return None
    x = int(input)
    assert 1 <= x <= 9
    return x


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


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({x},{y})".format(x=self.x,
                                  y=self.y)


class Cell:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.possible_set = set(range(1,10))

    def __str__(self):
        return "CELL{coordinates}: P{length}".format(coordinates=self.coordinates,
                                                 length=len(self.possible_set))

    def remove_possibility(self, value):
        if value in self.possible_set:
            self.possible_set.remove(value)

        assert len(self.possible_set) > 0, "{value} could not be removed Cell{coordinates}'s possiblity set because it was the only element".format(
            value=value,
            coordinates=self.coordinates)

    def set(self, value):
        assert value in self.possible_set, "{value}({value_type}) is not in Cell{coordinates}'s possiblity set: {possible_set}".format(
            value=value,
            value_type=type(value),
            coordinates=self.coordinates,
            possible_set=self.possible_set)
        self.possible_set = {value}

    @property
    def num_possibilities(self):
        return len(self.possible_set)


class Board:
    def __init__(self):
        self.rows = []
        self.possibility_partition = []
        for i in range(10):
            self.possibility_partition.append(set())
        for i in range(9):
            new_row = []
            for j in range(9):
                coordinates = Coordinates(x=j, y=i)
                new_cell = Cell(coordinates=coordinates)
                new_row.append(new_cell)
                self.possibility_partition[new_cell.num_possibilities].add(new_cell)
            self.rows.append(new_row)

    @staticmethod
    def coordinate_sort(a, b):
        return cmp("{x}{y}".format(x=a.coordinates.x, y=a.coordinates.y),"{x}{y}".format(x=b.coordinates.x, y=b.coordinates.y))

    def __str__(self):
        ret_val = 'BOARD:\n'
        for y in range(len(self.rows)):
            for x in range(len(self.rows[y])):
                ret_val = '{old_retval}{spacer}{new_portion}'.format(old_retval=ret_val,
                                                                     spacer='' if x == 0 else ' ',
                                                                     new_portion=str(self._get_cell(Coordinates(x=x, y=y))))
            ret_val = '{old_retval}\n'.format(old_retval=ret_val)
        ret_val = '{old_retval}\nPARTITION:'.format(old_retval=ret_val)
        for i in range(len(self.possibility_partition)):
            partition_row = list(self.possibility_partition[i])
            partition_row.sort(self.coordinate_sort)
            ret_val = '{old_retval}\t\tpartition[{i}] ({length})={row}\n'.format(old_retval=ret_val,
                                                                      i=i,
                                                                      length=len(partition_row),
                                                                      row=map(str, partition_row))
        return ret_val

    def set(self, coordinates, value):
        self.rows[coordinates.x][coordinates.y].set(value=value)

    def set_starting_state(self, file_name):
        values_from_file = self._read_puzzle(file_name=file_name)
        for y in range(len(values_from_file)):
            cur_row = values_from_file[y]
            x = -1
            for curr_cell in cur_row:
                x += 1
                if curr_cell is not None:
                    self._set_cell_and_update_adjacents(coordinates=Coordinates(x=x, y=y),
                                                        value=curr_cell)

    def _get_cell(self, coordinates):
        return self.rows[coordinates.x][coordinates.y]

    def _update_cell_and_partition(self, coordinates, value):
        print "_update_cell_and_partition({coordinates}, {value})".format(coordinates=coordinates,
                                                                          value=value)
        cell = self._get_cell(coordinates=coordinates)
        old_num_possibilities = cell.num_possibilities
        print "\told_num_possibilities={old_num_possibilities}".format(old_num_possibilities=old_num_possibilities)
        print "self.possibility_partition[{old_num_possibilities}] = {result}".format(
            old_num_possibilities=old_num_possibilities,
            result="\n".join(map(str, self.possibility_partition[old_num_possibilities])))
        cell.set(value=value)
        new_num_possibilities = cell.num_possibilities
        print "\tnew_num_possibilities={new_num_possibilities}".format(new_num_possibilities=new_num_possibilities)
        if new_num_possibilities <= old_num_possibilities:
            self.possibility_partition[old_num_possibilities].remove(cell)
            if new_num_possibilities > 1:
                assert cell not in self.possibility_partition[new_num_possibilities]
                self.possibility_partition[new_num_possibilities].add(cell)
        else:
            assert new_num_possibilities == old_num_possibilities

    def _remove_possibility_and_update_partition(self, coordinates, value):
        print "Starting_remove_possibility_and_update_partition({coordinates}, {value})".format(
            coordinates=coordinates,
            value=value)
        cell = self._get_cell(coordinates=coordinates)
        old_num_possibilities = cell.num_possibilities
        cell.remove_possibility(value=value)
        new_num_possibilities = cell.num_possibilities
        if new_num_possibilities <= old_num_possibilities:
            self.possibility_partition[old_num_possibilities].remove(cell)
            if new_num_possibilities > 1:
                assert cell not in self.possibility_partition[new_num_possibilities]
                self.possibility_partition[new_num_possibilities].add(cell)
        else:
            assert new_num_possibilities == old_num_possibilities
        print "Ending remove_possibility_and_update_partition() {old_num_possibilities} => {new_num_possibilities}".format(
            old_num_possibilities=old_num_possibilities,
            new_num_possibilities=new_num_possibilities)
        if (new_num_possibilities < old_num_possibilities) and (new_num_possibilities > 1):
            assert cell in self.possibility_partition[new_num_possibilities]
            print "self.possibility_partition[{new_num_possibilities}] = {result}".format(
                new_num_possibilities=new_num_possibilities,
                result="\n".join(map(str, self.possibility_partition[new_num_possibilities])))
        print ""

    def _set_cell_and_update_adjacents(self, coordinates, value):
        # Set the value for the cell in question
        self._update_cell_and_partition(coordinates=coordinates,
                                        value=value)

        # Remove that value from the possibility set for the rest of the row
        for curr_x in range(9):
            if curr_x != coordinates.x:
                self._remove_possibility_and_update_partition(coordinates=Coordinates(x=curr_x, y=coordinates.y),
                                                              value=value)

        # Remove that value from the possibility set for the rest of the column
        for curr_y in range(9):
            if curr_y != coordinates.y:
                self._remove_possibility_and_update_partition(coordinates=Coordinates(x=coordinates.x, y=curr_y),
                                                              value=value)

        # Remove that value from the possibility set for the rest of the neighborhood
        start_x = (coordinates.x / 3) * 3
        stop_x = start_x + 2
        start_y = (coordinates.y / 3) * 3
        stop_y = start_y + 2
        for curr_x in range(start_x, stop_x+1):
            for curr_y in range(start_y, stop_y+1):
                if not(curr_y == coordinates.y or curr_x == coordinates.x):
                    self._remove_possibility_and_update_partition(coordinates=Coordinates(x=curr_x, y=curr_y),
                                                                  value=value)

    @classmethod
    def _read_puzzle(cls, file_name):
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
    # puzzle = read_puzzle('sample_medium.txt')
    # solution = read_puzzle('sample_medium_solution.txt')
    #
    # print "\n\nPuzzle:"
    # print puzzle
    #
    # print "\n\nSolution:"
    # print solution

    B = Board()
    print B

    B._set_cell_and_update_adjacents(coordinates=Coordinates(x=3, y=0),
                                     value=5)

    print B

    #
    # B.set_starting_state('sample_medium.txt')
    # print B
