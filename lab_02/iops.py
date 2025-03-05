from sys import exit

def read_data(filename: str):
    with open(filename, 'r') as file:
        table = []

        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        z_count = sum([1 for x in lines if 'z' in x])
        idx = 0
        for i in range(z_count):
            table.append([])
            idx += 2
            for _ in range(z_count):
                line = lines[idx].split()[1:]
                table[i].append(list(map(float, line)))
                idx += 1
        return table