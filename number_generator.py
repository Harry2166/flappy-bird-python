
pairs = list()

for i in range(-60, 101):
    for j in range(300, 461):
        if abs(i-j) == 325:
            pairs.append([i,j])