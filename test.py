def draw_board():
    board_x = []
    colour_change = 0
    row = -1
    for i in range(8):
        board_y = []
        colour_change = 1 - colour_change
        for i in range(8):
            board_y.append(colour_change)
            colour_change = 1 - colour_change
        board_x.append(board_y)
    for i in board_x:
        row += 1
    return board_x
x = draw_board()
counter = -1
for i in x:
    counter += 1
    y_counter = -1
    for y in i:
        y_counter += 1
        x[counter][y_counter] = None
print(x)