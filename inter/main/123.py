import threading as th
import time
# counter = 0
 
def data_gen():
    # global counter
    for q in range(100):
        # counter = q
        print(q)
        time.sleep(0.5)
data_gen()

# def data_show():
#     for q in range(100):
#         print(counter)
#         time.sleep(1)
             

# threadnum = th.Thread(target=data_gen)
# threadshow=th.Thread(target=data_show)

# threadnum.start()
# threadshow.start()


 
# for thread in threads:
#     thread.join()
 
# print(f"Final counter value: {counter}")

