import random

x = ["EU","EU_N","USA","USA_E"]
for i in x:
    print(i)
    if random.randint(1,2) == 2:
        x.remove(i)

# for i in range(10):
#     print(f"i = {i}: {x[str(i)]}")
#     if random.randint(1,2) == 2:
#         del x[str(i)]
# print(x)