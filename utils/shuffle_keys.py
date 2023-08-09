from random import shuffle
f = open("./1m_example.data")
lines = f.readlines()
lines = [line.strip().split()[0] for line in lines]

shuffle(lines)

f = open("./shuffled_1m_example.data","w")
for line in lines:
    f.write(line+"\n")
f.close()
