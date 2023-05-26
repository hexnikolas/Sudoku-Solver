import numpy as np
import traceback
import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

## TODO: sixth stage : x-wing, skyscraper techniques


class Sudoku(QMainWindow):
    def __init__(self) -> None:

        super().__init__()

        self.unsolved = 0
        self.sudoku = []
        self.labels = []
        self.third_flag = False
        self.fourth_flag = False
        self.fifth_flag = False

        width = 540
        height = 540

        # set the title
        self.setWindowTitle("Sudoku")
        # setting  the fixed width and height of window
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setUpdatesEnabled(True)
        self.move(2000,0)


    def load_sudoku_puzzle(self):
        with open("/home/nikos/projects/newsolver/puzzles", "r") as f:
            for line in f:
                line.rstrip()
                sudoku_array = []
                #self.sudoku=[]
                self.unsolved=0
                i=0
                for char in line:
                    if char=='\n':
                        pass
                    else:
                        if char==".":
                            self.unsolved+=1
                            char="0"
                        sudoku_array.append(int(char))

                        if char=="0":
                            self.label = QLabel("", self)
                        else:
                            self.label = QLabel(char, self)
                        self.label.setStyleSheet("border :1px solid black;")
                        self.label.resize(60, 60)
                        self.label.setFont(QFont('Arial', 20))
                        self.label.setAlignment(QtCore.Qt.AlignCenter)
                        self.label.move(60*i%540, 60*int(60*i/540))
                        self.labels.append(self.label)
                        i+=1

                for i in range (9):
                    self.label = QLabel('', self)
                    self.label.setStyleSheet("border :2px solid black;")
                    self.label.resize(180, 180)
                    self.label.move(180*i%540, 180*int(180*i/540))
                self.show()

                sudoku_array = np.array(sudoku_array)
                asd=np.array_split(sudoku_array,9)

                for i in asd:
                    print(i)
                    self.sudoku+=[i.tolist()]
                print(f'{self.unsolved} unsolved')
                return self.sudoku

    def first_stage(self):
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j]==0:
                    self.sudoku[i][j]=[1,2,3,4,5,6,7,8,9]

                    label = self.labels[9*i+j]
                    label.setFont(QFont('Arial', 10))
                    label.setAlignment(QtCore.Qt.AlignLeft)
                    label.setAlignment(QtCore.Qt.AlignVCenter)
                    label.setWordWrap(True);
                    label.setText('1    2    3    4    5    6    7    8    9')

                    #print(self.labels[label])
        return self.sudoku

    def second_stage(self):
        #print('second stage')
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], int):
                    self.sudoku = self.remove_from_box(i, j, self.sudoku[i][j])
                    self.sudoku = self.remove_from_line(i, self.sudoku[i][j])
                    self.sudoku = self.remove_from_column(j, self.sudoku[i][j])
        return self.sudoku

    def third_stage(self):
        #print('third stage')
        #print()
        self.third_flag=True
        while self.third_flag and self.unsolved!=0:
            #print("---------------start of third loop---------------")
            self.third_flag=False
            #Έλεγχος των γραμμών για μοναδικές τιμές
            for i in range(9):
                line = []
                possiblepairs = []
                for x in self.sudoku[i]:
                    if isinstance(x, list):
                        line+=x
                while len(line)>0:
                    y=line[0]
                    if line.count(y)==1:
                        for counter,item in enumerate(self.sudoku[i]):
                            if isinstance(item, list):
                                if y in item:
                                    self.sudoku[i][counter]=y
                                    self.unsolved-=1
                                    self.third_flag=True
                                    self.fourth_flag = True
                                    self.fifth_flag = True
                                    #print(f"only in row found [{i},{counter}]={self.sudoku[i][counter]}")
                                    labela=self.labels[9*i+counter]
                                    labela.setText(str(y))
                                    labela.setFont(QFont('Arial', 20))
                                    labela.setAlignment(QtCore.Qt.AlignCenter)
                                    self.remove_from_box(i, counter , self.sudoku[i][counter])
                                    self.remove_from_line( i, self.sudoku[i][counter])
                                    self.remove_from_column(counter, self.sudoku[i][counter])
                    elif line.count(y)<4:
                        possiblepairs.append(y)


                    line = list(filter((y).__ne__, line))
                #print(f' row {i} {possiblepairs}')
                if len(possiblepairs)>2:
                    index = 0
                    possiblepairspositions = [None] * len(possiblepairs)
                    for number in possiblepairs:
                        pos = []
                        for jj in range(9):
                            try:
                                if number in self.sudoku[i][jj]:
                                    pos.append(jj)
                            except TypeError:
                                pass
                            except AttributeError:
                                pass
                        possiblepairspositions[index]=pos
                        index += 1


                    while len(possiblepairspositions)>0:
                        numbers=[]
                        key_a = max(possiblepairspositions, key=len)
                        if len(key_a)>2:
                            #print(key)
                            #print(possiblepairs)
                            #print(possiblepairspositions)
                            for spot, abc in enumerate(possiblepairspositions):
                                if set(key_a)>=set(abc):
                                    numbers.append(possiblepairs[spot])
                            #print(numbers)
                            #print()
                            if len(numbers)==len(key_a):
                                same_box = [int(asd/3) for asd in key_a]
                                if not (self.all_equal(same_box)):
                                    #print(f'row {i} found pairs that match {numbers} in spots {key_a}')
                                    self.remove_pairs_from_row(i, key_a, numbers)
                        possiblepairspositions.pop(0)
                        possiblepairs.pop(0)



            #Έλεγχος των στηλών για μοναδικές τιμές
            for j in range(9):
                sudo = [row[j] for row in self.sudoku]
                column=[]
                possiblepairss=[]
                for z in sudo:
                    if isinstance(z,list):
                        column+=z
                while len(column)>0:
                    k=column[0]
                    if column.count(k)==1:
                        for counters,items in enumerate(sudo):
                            if isinstance(items, list):
                                if k in items:
                                    self.sudoku[counters][j]=k
                                    self.third_flag=True
                                    self.fourth_flag = True
                                    self.fifth_flag = True
                                    self.unsolved-=1
                                    print(f"only in column found [{counters},{j}]={self.sudoku[counters][j]}")
                                    labelb=self.labels[9*counters+j]
                                    labelb.setText(str(k))
                                    labelb.setFont(QFont('Arial', 20))
                                    labelb.setAlignment(QtCore.Qt.AlignCenter)
                                    self.remove_from_box(counters, j ,self.sudoku[counters][j])
                                    self.remove_from_line(counters, self.sudoku[counters][j])
                                    self.remove_from_column(j, self.sudoku[counters][j])
                    elif column.count(k)<4:
                        possiblepairss.append(k)

                    column = list(filter((k).__ne__, column))

                #print(f' column {j} {possiblepairss}')
                if len(possiblepairss)>2:
                    index = 0
                    possiblepairspositionss = [None] * len(possiblepairss)
                    for number in possiblepairss:
                        pos = []
                        for ii in range(9):
                            try:
                                if number in self.sudoku[ii][j]:
                                    pos.append(ii)
                            except TypeError:
                                pass
                            except AttributeError:
                                pass
                        possiblepairspositionss[index]=pos
                        index += 1

                    while len(possiblepairspositionss)>0:
                        numbers=[]
                        key_b = max(possiblepairspositionss, key=len)
                        if len(key_b)>2:
                            #print(key)
                            #print(possiblepairs)
                            #print(possiblepairspositions)
                            for spot, abc in enumerate(possiblepairspositionss):
                                if set(key_b)>=set(abc):
                                    numbers.append(possiblepairss[spot])
                            #print(numbers)
                            #print()
                            if len(numbers)==len(key_b):
                                same_box = [int(asd/3) for asd in key_b]
                                if not (self.all_equal(same_box)):
                                    #print(f'column {j} found pairs that match {numbers} in spots {key_b}')
                                    self.remove_pairs_from_column(j, key_b, numbers)
                        possiblepairspositionss.pop(0)
                        possiblepairss.pop(0)


            #Έλεγχος των κουτιών για μοναδικές τιμές
            for i in range(3):
                for j in range(3):
                    box=[]
                    for ii in range(3*i,3*i+3):
                        for jj in range(3*j,3*j+3):
                            if isinstance(self.sudoku[ii][jj], list):
                                box+=self.sudoku[ii][jj]
                    for l in box:
                        if box.count(l)==1:
                            for ii in range(3*i,3*i+3):
                                for jj in range(3*j,3*j+3):
                                    if isinstance(self.sudoku[ii][jj], list):
                                        if l in self.sudoku[ii][jj]:
                                            self.sudoku[ii][jj]=l
                                            self.third_flag=True
                                            self.fourth_flag = True
                                            self.fifth_flag = True
                                            self.unsolved-=1
                                            print(f"only in box found [{ii},{jj}]={self.sudoku[ii][jj]}")
                                            labelc=self.labels[9*ii+jj]
                                            labelc.setText(str(l))
                                            labelc.setFont(QFont('Arial', 20))
                                            labelc.setAlignment(QtCore.Qt.AlignCenter)
                                            self.remove_from_box(ii, jj , self.sudoku[ii][jj])
                                            self.remove_from_line(ii, self.sudoku[ii][jj])
                                            self.remove_from_column(jj, self.sudoku[ii][jj])
                        else:
                            box = list(filter((l).__ne__, box))

    def fourth_stage(self):
        self.fourth_flag=True
        while self.fourth_flag and self.unsolved!=0:
            #print("---------------start of fourth loop---------------")
            self.fourth_flag=False

            for i in range(3):
                for j in range(3):
                    pairsthatmatch=[]
                    tripsthatmatch=[]
                    box=[]
                    for ii in range(3*i,3*i+3):
                        for jj in range(3*j,3*j+3):
                            try:
                                box.extend(self.sudoku[ii][jj])
                            except TypeError:
                                pass

                    while len(box)>0:
                        l=box[0]
                        if box.count(l)==2:
                            pairs=[]
                            for ii in range(3*i,3*i+3):
                                for jj in range(3*j,3*j+3):
                                    try:
                                        if l in self.sudoku[ii][jj]:
                                            pairs.append([ii,jj])
                                    except TypeError:
                                        pass
                            pairsthatmatch.append([pairs,l])
                            try:
                                if pairs[0][0]==pairs[1][0]:
                                    self.remove_shadow_from_line(pairs[0][0], int(pairs[0][1]/3), l)
                                elif pairs[0][1]==pairs[1][1]:
                                    self.remove_shadow_from_column(pairs[0][1], int(pairs[1][0]/3), l)
                            except IndexError:
                                pass

                        elif box.count(l)==3:
                            pairs=[]
                            for ii in range(3*i,3*i+3):
                                for jj in range(3*j,3*j+3):
                                    try:
                                        if l in self.sudoku[ii][jj]:
                                            pairs.append([ii,jj])
                                    except TypeError:
                                        pass
                            tripsthatmatch.append([pairs,l])
                            #print(pairs)
                            try:
                                if pairs[0][0]==pairs[1][0]==pairs[2][0]:
                                    #Αν είναι και οι τρεις στην ίδια γραμμή, τον σβήνουμε από τα υπόλοιπα κουτιά της γραμμής
                                    #print(f'found a three possible {l} in line {pairs[0][0]}')
                                    self.remove_shadow_from_line(pairs[0][0], int(pairs[0][1]/3), l)
                                elif pairs[0][1]==pairs[1][1]==pairs[2][1]:
                                    #Αν είναι και οι τρεις στην ίδια στήλη, τον σβήνουμε από τα υπόλοιπα κουτιά της στήλης
                                    #print(f'found a three possible {l} in column {pairs[0][1]}')
                                    self.remove_shadow_from_column(pairs[0][1], int(pairs[1][0]/3), l)
                            except IndexError:
                                pass


                        box = list(filter((l).__ne__, box))

                    #Αν βρούμε δύο αριθμούς που πηγαίνουν μόνο σε δύο ίδια κουτιά, αφαιρούμε τους υπόλοιπους από εκείνα τα κουτιά
                    while len(pairsthatmatch)>1:
                        eye=pairsthatmatch[0]
                        for key in pairsthatmatch:
                            if eye[0]==key[0] and eye[1]!=key[1]:
                                #print(f'fffffffffffffffffffffound {eye[0]},  {eye[1]}+{key[1]}')
                                if not len(self.sudoku[eye[0][0][0]][eye[0][0][1]])==len(self.sudoku[eye[0][1][0]][eye[0][1][1]])==2:
                                    #print('found shadow in box')
                                    self.remove_shadow_from_box(eye[0][0], eye[0][1], eye[1], key[1])
                        pairsthatmatch.pop(0)


                    #Παρόμοια και για τρεις αριθμούς που πηγαίνουν μόνο σε τρία ίδια κουτιά.
                    pos=0
                    #print(tripsthatmatch)
                    while pos<len(tripsthatmatch):
                        matches=0
                        eye=tripsthatmatch[pos]
                        for key in tripsthatmatch:
                            if eye[0]==key[0] and eye[1]!=key[1]:
                                matches+=1
                        #print(matches)
                        if matches<2:
                            tripsthatmatch.pop(0)
                        else:
                            #print('found trips shadows in box')
                            self.remove_trips_shadows_from_box(tripsthatmatch[pos][0],[key[1] for key in tripsthatmatch if key[0]==tripsthatmatch[pos][0]])
                            tripsthatmatch.pop(pos)

            self.third_stage()
        return self.sudoku

    def fifth_stage(self):
        #print('fifth stage')
        self.fifth_flag = True
        x_wing= {}
        while self.fifth_flag and self.unsolved!=0:
            #print("---------------start of fifth loop---------------")
            self.fifth_flag = False
            for i in range(9):
                line = []
                line_two = []
                line_x_wing = []
                for x in self.sudoku[i]:
                    if isinstance(x, list):
                        line.append(x)
                        line_two.extend(x)
                        line_x_wing.extend(x)
                #print(line_x_wing)
                while len(line)>0:#for item in line:
                    item = line[0]
                    if line.count(item)>1:
                        #print(f'found match {item}')
                        positions=[]
                        for pos,x in enumerate(self.sudoku[i]):
                            if item == x:
                                positions.append(pos)
                                #print(x,pos)
                        #print(positions)
                        if len(positions)==2:
                            if int(positions[0]/3)!=int(positions[1]/3):
                                print(f'match found in row {i} positions {positions} and numbers {item}')
                                self.remove_pair_from_line(i, positions, item)
                        elif len(positions)==3:
                            print(f'three match found {item}')
                    line = list(filter((item).__ne__, line))

                #print(line_two)
                while len(line_two)>0:
                    number = line_two[0]
                    position=[]
                    if line_two.count(number)==2 or line_two.count(number)==3:
                        #print(f'possible ghost found line {i} number {number}')
                        for j in range(9):
                            try:
                                if number in self.sudoku[i][j]:
                                    position.append(j)
                            except TypeError:
                                pass
                        #print(position)
                        boxes = [int(k/3) for k in position]
                        if all(x==boxes[0] for x in boxes) and boxes:
                            #print(f'fffffffffffound ghost in line {i} number {number}')
                            self.remove_ghost_from_box_line(position, i, number)
                    line_two = list(filter((number).__ne__, line_two))


            #Έλεγχος των στηλών για μοναδικές τιμές
            for j in range(9):
                sudo = [row[j] for row in self.sudoku]
                column=[]
                column_two=[]
                for z in sudo:
                    if isinstance(z,list):
                        column.append(z)
                        column_two.extend(z)
                #print(column)
                while len(column)>0:
                    item = column[0]
                    #print(item)
                    if len(item)<4:
                        if column.count(item)>1:
                            positions=[]
                            for y in range(9):
                                if item==self.sudoku[y][j]:
                                    positions.append(y)
                            #print(positions)
                            if len(positions)==2:
                                if not int(positions[0]/3)==int(positions[1]/3):
                                    #print(f'match found in column {j} positions {positions} and numbers {item}')
                                    self.remove_pair_from_column(j, positions, item)
                            #elif len(positions)==3:
                                #print(f'three column match found {item}')

                    column = list(filter((item).__ne__, column))

                while len(column_two)>0:
                    number = column_two[0]
                    position=[]
                    if column_two.count(number)==2 or column_two.count(number)==3:
                        #print(f'possible ghost found line {i} number {number}')
                        for i in range(9):
                            try:
                                if number in self.sudoku[i][j]:
                                    position.append(i)
                            except TypeError:
                                pass
                        #print(position)
                        boxes = [int(k/3) for k in position]
                        #print(boxes)
                        if all(x==boxes[0] for x in boxes) and len(position)>0:
                            #print(f'fffffffffffound ghost in column {j} number {number}')
                            self.remove_ghost_from_box_column(position, j, number)
                    column_two = list(filter((number).__ne__, column_two))

            self.fourth_stage()

    def remove_shadow_from_box(self, spot1, spot2, number1, number2):
        #print('inside shadow box')
        for i in range(1,10):
            if i!=number1 and i!=number2:
                try:
                    self.sudoku[spot1[0]][spot1[1]].remove(i)
                    print(f'removed {i} from position {spot1[0]},{spot1[1]}')
                    label = self.labels[9*spot1[0]+spot1[1]]
                    label_content = label.text()
                    label_content = label_content.replace(str(i), "  ")
                    label.setText(label_content)
                    self.fourth_flag=True
                    self.fifth_flag = True
                    if len(self.sudoku[spot1[0]][spot1[1]])==1:
                        self.unsolved-=1
                        self.sudoku[spot1[0]][spot1[1]]=self.sudoku[spot1[0]][spot1[1]][0]
                        print(f"found [{spot1[0]},{spot1[1]}]={sudoku[spot1[0]][spot1[1]]}")
                        remove_from_box(spot1[0], spot1[1] , self.sudoku[spot1[0]][spot1[1]])
                        remove_from_line(spot1[0], self.sudoku[spot1[0]][spot1[1]])
                        remove_from_column(spot1[1], self.sudoku[spot1[0]][spot1[1]])
                except ValueError as ve:
                    pass
                except AttributeError as ae:
                    pass
                try:
                    self.sudoku[spot2[0]][spot2[1]].remove(i)
                    print(f'removed {i} from position {spot2[0]},{spot2[1]}')
                    label = self.labels[9*spot2[0]+spot2[1]]
                    label_content = label.text()
                    label_content = label_content.replace(str(i), "  ")
                    label.setText(label_content)
                    self.fourth_flag = True
                    self.fifth_flag = True
                    if len(self.sudoku[spot2[0]][spot2[1]])==1:
                        #print(sudoku[spot2[0]][spot2[1]])
                        self.sudoku[spot2[0]][spot2[1]]=self.sudoku[spot2[0]][spot2[1]][0]
                        label.setText(str(self.sudoku[spot2[0]][spot2[1]]))
                        label.setFont(QFont('Arial', 20))
                        label.setAlignment(QtCore.Qt.AlignCenter)
                        print(f"found [{spot2[0]},{spot2[1]}]={sudoku[spot2[0]][spot2[1]]}")
                        self.remove_from_box(spot2[0], spot2[1] , self.sudoku[spot2[0]][spot2[1]])
                        self.remove_from_line(spot2[0], self.sudoku[spot2[0]][spot2[1]])
                        self.remove_from_column(spot2[1], self.sudoku[spot2[0]][spot2[1]])
                except ValueError as ve:
                    pass
                except AttributeError as ae:
                    pass

    def remove_shadow_from_line(self, line, box, number):
        #print('inside shadow line')
        for i in range(3):
            if i!=box:
                for ii in range(3*i,3*i+3):
                    try:
                        self.sudoku[line][ii].remove(number)
                        label = self.labels[9*line+ii]
                        label_content = label.text()
                        label_content = label_content.replace(str(number), "  ")
                        label.setText(label_content)
                        print(f'removed {number} from position {line},{ii}')
                        self.fourth_flag=True
                        if len(self.sudoku[line][ii])==1:
                            self.unsolved-=1
                            self.sudoku[line][ii]=self.sudoku[line][ii][0]
                            print(f"found [{line},{ii}]={self.sudoku[line][ii]}")
                            label.setText(str(self.sudoku[line][ii]))
                            label.setFont(QFont('Arial', 20))
                            label.setAlignment(QtCore.Qt.AlignCenter)
                            self.remove_from_box(line, ii , self.sudoku[line][ii])
                            self.remove_from_line(line, self.sudoku[line][ii])
                            self.remove_from_column(ii, self.sudoku[line][ii])
                    except ValueError as ve:
                        pass
                    except AttributeError as ae:
                        pass

    def remove_shadow_from_column(self, column, box, number):
        #print('inside shadow column')
        #print(f'column {column}, box {box}')
        for i in range(3):
            if i!=box:
                for ii in range(3*i, 3*i+3):
                    try:
                        self.sudoku[ii][column].remove(number)
                        print(f'removed {number} from position {ii},{column}')
                        label = self.labels[9*ii+column]
                        label_content = label.text()
                        label_content = label_content.replace(str(number), "  ")
                        label.setText(label_content)
                        self.fourth_flag=True
                        self.fifth_flag = True
                        if len(self.sudoku[ii][column])==1:
                            self.unsolved-=1
                            self.sudoku[ii][column]=self.sudoku[ii][column][0]
                            print(f"found [{ii},{column}]={self.sudoku[ii][column]}")
                            label.setText(str(self.sudoku[ii][column]))
                            label.setFont(QFont('Arial', 20))
                            label.setAlignment(QtCore.Qt.AlignCenter)
                            self.remove_from_box(ii, column , self.sudoku[ii][column])
                            self.remove_from_line(ii, self.sudoku[ii][column])
                            self.remove_from_column(column, self.sudoku[ii][column])
                    except ValueError as ve:
                        pass
                    except AttributeError as ae:
                        pass

    def remove_trips_shadows_from_box(self, cells, keys):
        #print(cells, keys)
        for cell in cells:
            for i in range(1,10):
                if i not in keys:
                    try:
                        self.sudoku[cell[0]][cell[1]].remove(i)
                        print(f'removed {i} from position {cell}')
                        label = self.labels[9*cell[0]+cell[1]]
                        label_content = label.text()
                        label_content = label_content.replace(str(i), "  ")
                        label.setText(label_content)
                        if len(self.sudoku[cell[0]][cell[1]])==1:
                            self.unsolved-=1
                            print(f"only in cell found (trips) [{ii},{jj}]={self.sudoku[cell[0]][cell[1]][0]}")
                            self.sudoku[cell[0]][cell[1]]=self.sudoku[cell[0]][cell[1]][0]
                            label.setText(str(self.sudoku[cell[0]][cell[1]]))
                            label.setFont(QFont('Arial', 20))
                            label.setAlignment(QtCore.Qt.AlignCenter)
                            self.remove_from_box(cell[0],cell[1],self.sudoku[cell[0]][cell[1]])
                            self.remove_from_line(cell[0],self.sudoku[cell[0]][cell[1]])
                            self.remove_from_column(cell[1],self.sudoku[cell[0]][cell[1]])
                    except TypeError:
                        pass
                    except ValueError:
                        pass

    def remove_ghost_from_box_line(self, columns, line, number):
        #print(columns, line, number)
        box_row = int(line/3)
        box_column = int(columns[0]/3)
        for i in range(3*box_row, 3*box_row+3):
            for j in range(3*box_column, 3*box_column+3):
                if line!=i:
                    try:
                        self.sudoku[i][j].remove(number)
                        self.fifth_flag = True
                        print(f'ghost line removed {number} from {i} {j}')
                        label = self.labels[9*i+j]
                        label_content = label.text()
                        label_content = label_content.replace(str(number), "  ")
                        label.setText(label_content)
                        if len(self.sudoku[i][j])==1:
                            self.unsolved-=1
                            print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                            self.sudoku[i][j]=self.sudoku[i][j][0]
                            label.setText(str(self.sudoku[i][j]))
                            label.setFont(QFont('Arial', 20))
                            label.setAlignment(QtCore.Qt.AlignCenter)
                            self.remove_from_box(i , j , self.sudoku[i][j])
                            self.remove_from_line(i, self.sudoku[i][j])
                            self.remove_from_column(j, self.sudoku[i][j])
                    except TypeError:
                        pass
                    except ValueError:
                        pass
                    except AttributeError:
                        pass
                else:
                    if j not in columns:
                        try:
                            self.sudoku[i][j].remove(number)
                            print(f'ghost line removed {number} from {i} {j}')
                            self.fifth_flag = True
                            label = self.labels[9*i+j]
                            label_content = label.text()
                            label_content = label_content.replace(str(number), "  ")
                            label.setText(label_content)
                            if len(self.sudoku[i][j])==1:
                                self.unsolved-=1
                                print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                                self.sudoku[i][j]=self.sudoku[i][j][0]
                                label.setText(str(self.sudoku[i][j]))
                                label.setFont(QFont('Arial', 20))
                                label.setAlignment(QtCore.Qt.AlignCenter)
                                self.remove_from_box(i , j , self.sudoku[i][j])
                                self.remove_from_line(i, self.sudoku[i][j])
                                self.remove_from_column(j, self.sudoku[i][j])
                        except TypeError:
                            pass
                        except ValueError:
                            pass
                        except AttributeError:
                            pass

    def remove_ghost_from_box_column(self, lines, column, number):
        #print(lines)
        box_row = int(lines[0]/3)
        box_column = int(column/3)
        for i in range(3*box_row, 3*box_row+3):
            for j in range(3*box_column, 3*box_column+3):
                if j!=column:
                    try:
                        self.sudoku[i][j].remove(number)
                        self.fifth_flag = True
                        print(f'ghost column removed {number} from {i} {j}')
                        label = self.labels[9*i+j]
                        label_content = label.text()
                        label_content = label_content.replace(str(number), "  ")
                        label.setText(label_content)
                        if len(self.sudoku[i][j])==1:
                            self.unsolved-=1
                            print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                            self.sudoku[i][j]=self.sudoku[i][j][0]
                            label.setText(str(self.sudoku[i][j]))
                            label.setFont(QFont('Arial', 20))
                            label.setAlignment(QtCore.Qt.AlignCenter)
                            self.remove_from_box(i , j , self.sudoku[i][j])
                            self.remove_from_line(i, self.sudoku[i][j])
                            self.remove_from_column(j, self.sudoku[i][j])
                    except TypeError:
                        pass
                    except ValueError:
                        pass
                    except AttributeError:
                        pass
                else:
                    if i not in lines:
                        try:
                            self.sudoku[i][j].remove(number)
                            print(f'ghost column removed {number} from {i} {j}')
                            label = self.labels[9*i+j]
                            label_content = label.text()
                            label_content = label_content.replace(str(number), "  ")
                            label.setText(label_content)
                            if len(self.sudoku[i][j])==1:
                                self.unsolved-=1
                                print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                                self.sudoku[i][j]=self.sudoku[i][j][0]
                                label.setText(str(self.sudoku[i][j]))
                                label.setFont(QFont('Arial', 20))
                                label.setAlignment(QtCore.Qt.AlignCenter)
                                self.remove_from_box(i , j , self.sudoku[i][j])
                                self.remove_from_line(i, self.sudoku[i][j])
                                self.remove_from_column(j, self.sudoku[i][j])
                        except TypeError:
                            pass
                        except ValueError:
                            pass
                        except AttributeError:
                            pass

    def remove_from_box(self, i, j, number):
        i = int(i/3)
        j = int(j/3)
        for ii in range(3*i,3*i+3):
            for jj in range(3*j, 3*j+3):
                try:
                    self.sudoku[ii][jj].remove(number)
                    label = self.labels[9*ii+jj]
                    label_content = label.text()
                    label_content = label_content.replace(str(number), "  ")
                    label.setText(label_content)
                    if len(self.sudoku[ii][jj])==1:
                        self.unsolved-=1
                        print(f"only in cell found [{ii},{jj}]={self.sudoku[ii][jj][0]}")
                        self.sudoku[ii][jj]=self.sudoku[ii][jj][0]
                        label.setText(str(self.sudoku[ii][jj]))
                        label.setFont(QFont('Arial', 20))
                        label.setAlignment(QtCore.Qt.AlignCenter)
                        self.remove_from_box(ii,jj,self.sudoku[ii][jj])
                        self.remove_from_line(ii,self.sudoku[ii][jj])
                        self.remove_from_column(jj,self.sudoku[ii][jj])
                except AttributeError as ae:
                    #Found an int instead of a list
                    pass

                except ValueError as ve:
                    #Number not found in list
                    pass

        return self.sudoku

    def remove_from_line(self, i , number):
        for j in range(9):
            try:
                self.sudoku[i][j].remove(number)
                label = self.labels[9*i+j]
                label_content = label.text()
                label_content = label_content.replace(str(number), "  ")
                label.setText(label_content)
                if len(self.sudoku[i][j])==1:
                    self.unsolved-=1
                    print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                    self.sudoku[i][j]=self.sudoku[i][j][0]
                    label.setText(str(self.sudoku[i][j]))
                    label.setFont(QFont('Arial', 20))
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    self.remove_from_box(i , j , self.sudoku[i][j])
                    self.remove_from_line(i, self.sudoku[i][j])
                    self.remove_from_column(j, self.sudoku[i][j])
            except AttributeError as ae:
                #Found an int instead of a list
                pass

            except ValueError as ve:
                #Number not found in list
                pass
        return self.sudoku

    def remove_from_column(self, j, number):
        for i in range(9):
            try:
                self.sudoku[i][j].remove(number)
                label = self.labels[9*i+j]
                label_content = label.text()
                label_content = label_content.replace(str(number), "  ")
                label.setText(label_content)
                if len(self.sudoku[i][j])==1:
                    self.unsolved-=1
                    print(f"only in cell found [{i},{j}]={self.sudoku[i][j][0]}")
                    self.sudoku[i][j]=self.sudoku[i][j][0]
                    label.setText(str(self.sudoku[i][j]))
                    label.setFont(QFont('Arial', 20))
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    self.remove_from_box(i , j , self.sudoku[i][j])
                    self.remove_from_line(i, self.sudoku[i][j])
                    self.remove_from_column(j, self.sudoku[i][j])
            except AttributeError as ae:
                #Found an int instead of a list
                pass

            except ValueError as ve:
                #Number not found in list
                pass
        return self.sudoku

    def remove_pair_from_line(self, line, columns, numbers):
        #print('in remove pair form row')
        for j in range(9):
            if isinstance(self.sudoku[line][j], list) and self.sudoku[line][j] != numbers:
                for number in numbers:
                    try:
                        self.sudoku[line][j].remove(number)
                        self.fifth_flag = True
                        print(f'removed {number} from [{line}{j}]')
                        label = self.labels[9*line+j]
                        label_content = label.text()
                        label_content = label_content.replace(str(number), "  ")
                        label.setText(label_content)
                        if len(self.sudoku[line][j])==1:
                            self.unsolved-=1
                            print(f"only in cell found [{line},{j}]={self.sudoku[line][j][0]}")
                            self.sudoku[line][j]=self.sudoku[line][j][0]
                            label.setText(str(self.sudoku[line][j]))
                            label.setFont(QFont('Arial', 20))
                            label.setAlignment(QtCore.Qt.AlignCenter)
                            self.remove_from_box(line , j , self.sudoku[line][j])
                            self.remove_from_line(line, self.sudoku[line][j])
                            self.remove_from_column(j, self.sudoku[line][j])
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def remove_pair_from_column(self, column, rows, numbers):
        #print('in remove pair form column')
        for i in range(9):
            if isinstance(self.sudoku[i][column], list) and self.sudoku[i][column]!=numbers:
                #print(self.sudoku[i][column])
                for number in numbers:
                    try:
                        self.sudoku[i][column].remove(number)
                        self.fifth_flag = True
                        print(f'removed {number} from [{i}{column}]')
                        label = self.labels[9*i+column]
                        label_content = label.text()
                        label_content = label_content.replace(str(number), "  ")
                        label.setText(label_content)
                        if len(self.sudoku[i][column])==1:
                            self.unsolved-=1
                            print(f"only in cell found [{i},{column}]={self.sudoku[i][column][0]}")
                            self.sudoku[i][column]=self.sudoku[i][column][0]
                            label.setText(str(self.sudoku[i][column]))
                            label.setFont(QFont('Arial', 20))
                            label.setAlignment(QtCore.Qt.AlignCenter)
                            self.remove_from_box(i , column , self.sudoku[i][column])
                            self.remove_from_line(i, self.sudoku[i][column])
                            self.remove_from_column(column, self.sudoku[i][column])
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def remove_pairs_from_row(self, i, columns, numbers):
        for j in columns:
            for number in range(1,10):
                if number not in numbers:
                    try:
                        self.sudoku[i][j].remove(number)
                        self.third_flag = True
                        self.fourth_flag = True
                        self.fifth_flag = True
                        print(f'removed {number} from position {i},{j}')
                        label = self.labels[9*i+j]
                        label_content = label.text()
                        label_content = label_content.replace(str(number), "  ")
                        label.setText(label_content)
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def remove_pairs_from_column(self, j, rows, numbers):
        for i in rows:
            for number in range(1,10):
                if number not in numbers:
                    try:
                        self.sudoku[i][j].remove(number)
                        self.third_flag = True
                        self.fourth = True
                        self.fifth_flag = True
                        print(f'removed {number} from position {i},{j}')
                        label = self.labels[9*i+j]
                        label_content = label.text()
                        label_content = label_content.replace(str(number), "  ")
                        label.setText(label_content)
                    except ValueError:
                        pass
                    except AttributeError:
                        pass

    def all_equal(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == x for x in iterator)

    def show_puzzle(self):
        for i in self.sudoku:
            print(i)
            #print()


if __name__=="__main__":
    print('Script started')
    App = QApplication(sys.argv)

    puzzle = Sudoku()

    puzzle.load_sudoku_puzzle()
    puzzle.first_stage()
    puzzle.second_stage()
    puzzle.third_stage()
    puzzle.fourth_stage()
    if puzzle.unsolved != 0:
        puzzle.fifth_stage()

    puzzle.show_puzzle()
    print(puzzle.unsolved)
    sys.exit(App.exec())
