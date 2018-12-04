# Top line
# elif math.floor(coordinate[0]) == 0 and math.floor(coordinate[1]) > 0 and math.floor(coordinate[1]) < nRows :
#    occupancy_grid[math.floor(math.floor(coordinate[0]))][math.floor(math.floor(coordinate[1]))] = 15
# Left line
# elif math.floor(coordinate[1]) == 0 and coordinate[0] > 0 and coordinate[0] < nCols:
#        occupancy_grid[math.floor(coordinate[0])][math.floor(coordinate[1])] = 15
# elif math.floor(coordinate[0]) == 0 and coordinate[1] > 0 and coordinate[1] < nCols:
#        occupancy_grid[math.floor(coordinate[0])][math.floor(coordinate[1])] = 15

# if(dist<30):
#    occupancy_grid[math.floor(bresenham_line[-1][0])][math.floor(bresenham_line[-1][1])] = 15

# for x in bresenham_lines:
# for i in range(0, len(bresenham_lines)):
# Traverse its elements
# dist = calculate_distance(bresenham_lines[len(bresenham_lines) - 1][0],
#                          bresenham_lines[len(bresenham_lines) - 1][1],robot_row,robot_col)

#    for j in range(0, len(bresenham_lines[i])):
# Set their grid value to visited
#        if math.floor(bresenham_lines[i][j][0]) < nRows and bresenham_lines[i][j][1] < nCols and\
#                        math.floor(bresenham_lines[i][j][0]) > 0 and math.floor(bresenham_lines[i][j][1]) > 0:
#            occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 0
# Top line
#    elif math.floor(bresenham_lines[i][j][0]) == 0 and bresenham_lines[i][j][1] > 0 and bresenham_lines[i][j][1] < nRows :
#        occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 15
# Left line
#    elif math.floor(bresenham_lines[i][j][1]) == 0 and bresenham_lines[i][j][0] > 0 and bresenham_lines[i][j][0] < nRows :
#        occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 15
# Bottom line
#    elif math.floor(bresenham_lines[i][j][1]) == 0 and bresenham_lines[i][j][0] > 0 and bresenham_lines[i][j][0] < nCols:
#        occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 15
# Right line
#    elif math.floor(bresenham_lines[i][j][0]) == 0 and bresenham_lines[i][j][1] > 0 and bresenham_lines[i][j][1] < nCols:
#        occupancy_grid[math.floor(bresenham_lines[i][j][0])][math.floor(bresenham_lines[i][j][1])] = 15

# if math.floor(bresenhamLines[i][len(bresenhamLines[i])]) - 1][0]) < nRows and math.floor(bresenhamLines[i][len(bresenhamLines[i]) - 1][0]) < nCols and \
#        math.floor(bresenhamLines[i][len(bresenhamLines[i])]) > 0 and math.floor(bresenhamLines[i][len(bresenhamLines[i])]) > 0:
# if math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][0]) < nRows and \
#    math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][1]) < nCols and \
#     math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][0]) > 0 and \
#      math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][1]) > 0:
#    occupancy_grid[math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][0])][math.floor(bresenham_lines[i][len(bresenham_lines[i]) - 1][1])] = 15

# Update the map