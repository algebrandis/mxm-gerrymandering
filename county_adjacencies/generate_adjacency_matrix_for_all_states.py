import csv
from pathlib import Path

# create folder to store output files

output_dir = Path("county_adjacencies_by_state")
output_dir.mkdir(exist_ok=True)

adjacencies = []

states = set()

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

    if i == 1:   print(f"\nOne county found for {state}.\n")
    else:   print(f"\n{i} counties found for {state}.\n")

    # make state-specific adjacency matrix

    adjacency_matrix = [[0 for i in range(len(counties_in_state))]
                           for j in range(len(counties_in_state))]

    for row in adjacencies:
        if row[0] in counties_in_state and row[1] in counties_in_state:
            adjacency_matrix[counties_in_state[row[0]]][counties_in_state[row[1]]] = 1

    # print adjacency matrix (spams console a little bit, you can comment out without harming code)

    # print(f"Adjacency matrix for {state}:\n")
    #
    # for r in adjacency_matrix:
    #     for c in r:
    #         print(c, end=' ')
    #     print()
    # print()

    # save county list into directory

    with open(state_dir / f'{state}_county_list.csv', 'w') as county_list_output:
        cl_writer = csv.writer(county_list_output)
        cl_writer.writerows([[c] for c in counties_in_state.keys()])

    print(f"Saved county list to county_adjacenies\\{state}\\{state}_county_list.csv.\n")

    # save adjacency matrix

    with open(state_dir / f'{state}_county_adjacencies.csv', 'w') as county_adjacency_output:
        ca_writer = csv.writer(county_adjacency_output)
        ca_writer.writerows(adjacency_matrix)

    print(f"Saved county adjacencies to county_adjacencies\\{state}\\{state}_county_adjacencies.csv.\n")
