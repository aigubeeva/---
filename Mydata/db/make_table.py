from .db_helper import get_happy_data
import matplotlib.pyplot as plt
import logging as lg



async def make_table(user_id : int):
    l1 = []
    l2 = []
    for i in await get_happy_data(user_id=user_id):
        l1.append(i[1])
        l2.append(i[2])
    plt.bar(l2, l1)
    lg.info((l2, l1))
    plt.savefig("Mydata\Figure_1.png")
    plt.close()
    return 'ok'
    

# print(run(make_table()))
