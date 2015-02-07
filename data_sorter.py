import os
import multiprocessing as mp
import random as rand
import shutil

def handle_files(name, files):
    path = os.path.join("C:\\", "Project", "data", name)
    if not os.path.exists(path):
        os.makedirs(path)
    for file in files:       
        prob1 = rand.random()
        loc = "test" if (prob1 < .2) else "validate" if prob1 < .4 else "train"
        file_path = os.path.join("C:\\", "Project", "data", name, loc, file.split("\\")[4])
        if not os.path.exists(file_path):
            os.makedirs(file_path)
                
        shutil.copy(file,file_path)

count = 177518
my_files = {}
for root, dirs, files in os.walk(os.path.join("C:\\", "Project", "extracted")):
    for name in files:
        my_name = root.split("\\")[3]
        if my_name not in my_files:
            my_files[my_name] = []
        my_files[my_name].append(os.path.join(root, name))


#pool = mp.Pool(mp.cpu_count()*2)
results = []
for name in my_files:
    handle_files(name,my_files[name])
    #results.append(pool.apply_async(handle_files,[name,my_files[name]]))
#pool.close()
#pool.join()
