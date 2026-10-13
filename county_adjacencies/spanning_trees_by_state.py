import csv
from pathlib import Path

# create folder to store output files

output_dir = Path("county_adjacencies_by_state")
output_dir.mkdir(exist_ok=True)

adjacencies = []

states = set()

# Determinant using Gaussian elimination
def determinant(mat, n):
    det = 1.0

    for i in range(n):

        # Find pivot
        pivot = i
        for j in range(i + 1, n):
            if abs(mat[j][i]) > abs(mat[pivot][i]):
                pivot = j

        # If pivot is zero → determinant = 0
        if abs(mat[pivot][i]) < 1e-9:
            return 0

        # Swap rows
        if i != pivot:
            mat[i], mat[pivot] = mat[pivot], mat[i]
            det *= -1

        det *= mat[i][i]

        # Eliminate below
        for j in range(i + 1, n):
            factor = mat[j][i] / mat[i][i]
            for k in range(i, n):
                mat[j][k] -= factor * mat[i][k]

    return det

# Function to compute number of spanning trees
# using adjacency matrix
def numOfSpanningTree(graph, v):

    # Laplacian matrix
    L = [[0.0] * v for _ in range(v)]

    for i in range(v):
        degree = 0

        for j in range(v):
            if graph[i][j] == 1:
                degree += 1
                if i != j:
                    L[i][j] = -1

        L[i][i] = degree

    # Minor matrix
    minor = [[0.0] * (v - 1) for _ in range(v - 1)]

    for i in range(v - 1):
        for j in range(v - 1):
            minor[i][j] = L[i][j]

    # Determinant
    return round(determinant(minor, v - 1))


# make a file with all adjacencies in the file

with open("us_census_data_county_adjacency.csv") as raw:
    for line in raw:
        cells = line.split("|")
        if cells[0] != "County Name":
            adjacencies.append([cells[0], cells[2], cells[3]])
            states.add(cells[0][-2:])

# make state list

states = sorted(list(states))

for state in states:

    # create folder for states output

    state_dir = Path("county_adjacencies_by_state") / state
    state_dir.mkdir(parents=True, exist_ok=True)

    # makes list of counties in specific state

    counties_in_state = {}

    i = 0

    for row in adjacencies:
        if row[0][-2:] == state:
            if row[0] not in counties_in_state:
                counties_in_state[row[0]] = i
                i += 1

    # print number of counties for user to verify count

    if i == 1:   print(f"\nOne county found for {state}.")
    else:   print(f"\n{i} counties found for {state}.")

    # make state-specific adjacency matrix

    adjacency_matrix = [[0 for i in range(len(counties_in_state))]
                           for j in range(len(counties_in_state))]

    for row in adjacencies:
        if row[0] in counties_in_state and row[1] in counties_in_state:
            adjacency_matrix[counties_in_state[row[0]]][counties_in_state[row[1]]] = 1

    v = len(adjacency_matrix)

    if len(adjacency_matrix) > 0:
        print(state, numOfSpanningTree(adjacency_matrix, v))

