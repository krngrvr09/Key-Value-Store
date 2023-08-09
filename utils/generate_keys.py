
import uuid
import random
import string
def generate_random_text(length):
    characters = string.ascii_letters
    random_text = ''.join(random.choice(characters) for _ in range(length))
    return random_text
f = open("example.data","r")
lines = f.readlines()
lines = [line.split()[0] for line in lines]
lines = set(lines)

f = open("1m_example.data","w")

for i in range(1000000):
    print("i: ",i)
    key = str(uuid.uuid4())
    while key in lines:
        key = str(uuid.uuid4())
    value = generate_random_text(random.randint(10,50))
    f.write(key+" "+value+"\n")
    lines.add(key)

f.close()