def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

def input_list(prompt):
    return list(map(int, input(prompt).strip().split()))

def input_matrix(rows, cols, prompt):
    matrix = []
    print(prompt)
    for i in range(rows):
        row = input_list(f"Enter values for row {i + 1}: ")
        if len(row) != cols:
            print(f"Expected {cols} values for row {i + 1}.")
            return None
        matrix.append(row)
    return matrix

def calculate_available_resources(total_resources, allocation_matrix):
    available_matrix = [total - sum(row) for total, row in zip(total_resources, zip(*allocation_matrix))]
    return available_matrix

def find_all_safe_sequences(allocation_matrix, max_matrix, available_matrix, process_matrix):
    n = len(available_matrix)
    m = len(allocation_matrix)

    need_matrix = [[max_matrix[i][j] - allocation_matrix[i][j] for j in range(n)] for i in range(m)]

    def is_safe(process):
        return all(need_matrix[process][j] <= available_matrix[j] for j in range(n))

    def find_sequences(unfinished, safe_sequence):
        if not unfinished:
            safe_sequences.append(safe_sequence[:])
            return
        for process in unfinished[:]:
            if is_safe(process):
                for j in range(n):
                    available_matrix[j] += allocation_matrix[process][j]
                safe_sequence.append(process_matrix[process])
                unfinished.remove(process)
                find_sequences(unfinished, safe_sequence)
                unfinished.append(process)
                safe_sequence.pop()
                for j in range(n):
                    available_matrix[j] -= allocation_matrix[process][j]

    safe_sequences = []
    unfinished_processes = list(range(m))
    find_sequences(unfinished_processes, [])
    return safe_sequences

m = input_int("Enter the number of processes: ")
process_matrix = input().strip().split()
n = input_int("Enter the number of resource types: ")
total_resources = input_list("Enter total available resources for each type: ")
allocation_matrix = input_matrix(m, n, f"Enter allocation matrix ({m}x{n}): ")

if allocation_matrix:
    available_matrix = calculate_available_resources(total_resources, allocation_matrix)
    print("Available resources calculated:", available_matrix)
    max_matrix = input_matrix(m, n, f"Enter max matrix ({m}x{n}): ")

    if max_matrix:
        safe_sequences = find_all_safe_sequences(allocation_matrix, max_matrix, available_matrix, process_matrix)
        if safe_sequences:
            print("Safe sequences are:")
            for seq in safe_sequences:
                print(seq)
        else:
            print("No safe sequence exists.")
    else:
        print("Invalid input for max matrix.")
else:
    print("Invalid input for allocation matrix.")
