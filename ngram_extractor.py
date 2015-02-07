import os
import multiprocessing as mp
import sys
import operator
from collections import OrderedDict

def extract_ngrams(root, name, n):
    results = { }
    my_file = open(os.path.join(root, name))
    type(results)
    for line in my_file:
        for i in range(0, len(line)-(n+1)):
            ngram = ''.join(line[i:i+n])
            if results.get(ngram) is None:
                results.update({ngram : 1})                
            else:
                new_val = results.get(ngram)+1
                results.update({ngram : new_val})
    #print(name)
    #print(results)
    #exit()
    results = {k: v for k, v in results.items() if v > 1}
                
    d = OrderedDict(sorted(results.items(), key=lambda t: t[1]))
    
    path = os.path.join("C:\\", "Project", "data", root.split("\\")[3])
    print(path)
    write_to_file(path + "\\" + str(n)+'grams.txt', d)

def write_to_file(fileName, ngrams):
    my_file = open(fileName, 'w+')
    for entry in ngrams:
        my_file.write(entry + ' ' + str(ngrams[entry]) + '\n')
    #ngrams.clear()
            
def main():
    char_trigrams = []
    char_quadgrams = []
    pool = mp.Pool(mp.cpu_count()*2)
    for root, dirs, files, in os.walk(os.path.join("C:\\", "Project", "data")):
        for name in files:
            #print(name, name == "data.txt")
            if name == "data.txt":
                print(name)
                #print(root)
                #extract_ngrams(root,name,3)
                #extract_ngratms(root,name,4)
                #extract_ngrams(root,name,3)
                char_trigrams.append(pool.apply_async(extract_ngrams, [root, name, 3]))
                char_quadgrams.append(pool.apply_async(extract_ngrams, [root, name, 4]))
    

if __name__ == '__main__':
    main()
