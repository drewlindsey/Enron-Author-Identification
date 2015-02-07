import os
import re
import multiprocessing as mp
import sys
import string

def remove_quoted(my_file):
    lines = []
    lines.clear()
    count = 0
    flag = False
    for line in my_file:
        count += 1
        if line.lower().startswith("to:") and count > 8:
            flag = True
            break
        lines.append(line);
    if flag is True:
        for line in reversed(lines):
            if not (line.isspace() or not line):
                lines.remove(line)
            else:
                break    
        
    return lines

def extract_body(my_file):
    save = False
    is_valid = False        

    lines = remove_quoted(my_file)
    my_lines = []
    
    for line in lines:
       # print(line)
        split_line = re.split("\s+", line)
        last_name = my_file.name.split("\\")[4].split("-")[0]
        if len(split_line) > 1 and split_line[0].find("From:") == 0 and \
           split_line[1].find(last_name) != -1 and \
           split_line[1].find("enron.com") != -1:
            is_valid = True

        pattern = '".*?"\s*\<.*?@.*?\>\s*on\s*.*?\s*\d\d:\d\d:\d\d\s+\w\w.*'
        if line.find("--------- Inline attachment") != -1 or \
           line.find("-----Original Message-----") != -1 or \
           line.find("---------------------- Forwarded") != -1 or \
           line.find("----- Forwarded") != -1 or \
           line.find("@ENRON") != -1 or \
           line.find("--------------------------") != -1 or \
           line.find(">") == 0 or \
           (save and re.search(pattern, line) is not None):
            break
        
        if line.isspace() or not line:
            continue
        
        if save:
            regex = re.compile('[%s]' % re.escape(string.punctuation))
            reg1 = re.compile('\t')
            reg = re.compile('\d')
            out1 = reg1.sub('', line)
            out = regex.sub('', out1)
            out = reg.sub("@", out)
            my_lines.append(out.lower().strip() + "\n")
                
        if line.find("X-FileName") != -1 and is_valid:
            save = True
    return my_lines

def write_to_file(fileName, messages):
    my_file = open(fileName, 'w+')
    for line in messages:
        my_file.write(line + "\n")
    my_file.close()

def handle_file(root, file_name):
    my_file = open(os.path.join(root,file_name))
    lines = extract_body(my_file)
    my_file.close()
    path = os.path.join("C:\\", "Project", "extracted", root.split("C:\\Project\\enron_mail\\maildir\\")[1])
    if len(lines) > 0:
        if not os.path.exists(path):
            os.makedirs(path)
        write_to_file(path + "\\" + file_name, lines)

def main():
    results = []
    pool = mp.Pool(mp.cpu_count()*2)
    for root, dirs, files in os.walk(os.path.join("C:\\", "Project", "enron_mail", "maildir")):
        for name in files:
            results.append(pool.apply_async(handle_file,[root,name]))
    pool.close()
    pool.join()
            
if __name__ == '__main__':
    main()
