import os,random,argparse,sys

template = """#pragma once

REPLACE_ME_WORDLIST

REPLACE_ME_FILEWORDS

"""

banner = '''___   ___  __       ___       ______   ____    ____  ___         
\  \ /  / |  |     /   \     /  __  \  \   \  /   / /   \     /  __  \  
 \  V  /  |  |    /  ^  \   |  |  |  |  \   \/   / /  ^  \   |  |  |  | 
  >   <   |  |   /  /_\  \  |  |  |  |   \_    _/ /  /_\  \  |  |  |  | 
 /  .  \  |  |  /  _____  \ |  `--'  |     |  |  /  _____  \ |  `--'  | 
/__/ \__\ |__| /__/     \__\ \______/      |__| /__/     \__\ \______/   J

A tool that converts shellcode randomly using a dictionary!
                                                    Github:https://github.com/xiaoyaoxianj
'''

def nop_code(file,num):
    file_size = os.path.getsize(file)
    with open(file, 'rb') as contents:
        save = contents.read()
    tempfile = "temp_infile"
    with open(tempfile, 'wb') as contents:
        contents.write(b"\x90" * num)
        contents.write(save)
    file = open(tempfile, 'rb')
    contents_nop = file.read()
    file.close()
    os.system("del {}".format(tempfile))
    #linux rm
    return contents_nop

def Shellcode2Words(contents,stub):
    if os.path.exists("dict.txt") == False:
        print("[+] Please Set your dictionary!")
    f = open("dict.txt", "r")
    wordlist = f.readlines()
    f.close()
    chosen = []
    cwordstring = "extern const char* words[256] = {"
    for i in range(256):
        selection = wordlist[random.randint(0, len(wordlist))].strip("\n")
        cwordstring += '"{}", '.format(selection)
        chosen.append(selection)
        if (i + 1) % 16 == 0:
            cwordstring += '\n'
    cwordstring = cwordstring[:-2]
    cwordstring += "};"
    fwordsstring = "extern const char* filewords[{}] = {{".format(len(contents))

    filewords = [None] * len(contents)
    for i in range(len(contents)):
        filewords[i] = chosen[int(contents[i])]
        fwordsstring += '"{}", '.format(filewords[i])
        if (i + 1) % 16 == 0:
            fwordsstring += '\n'
    fwordsstring = fwordsstring[:-2]
    fwordsstring += "};"
    stub = stub.replace("REPLACE_ME_WORDLIST", cwordstring)
    stub = stub.replace("REPLACE_ME_FILEWORDS", fwordsstring)
    file = open("stub.h", "w")
    file.write(stub)
    file.close()

def main(file,num):
    print(banner)
    contents = nop_code(file,num)
    Shellcode2Words(contents,template)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shellcode To English Word')
    parser.add_argument("file", help="File containing raw shellcode", type=str)
    parser.add_argument('-n',"--num",dest='number', help='the number of the nops', type=int)

    if len(sys.argv) < 2:
        print(banner)
        parser.print_help()
        sys.exit()

    args = parser.parse_args()
    main(args.file,args.number)
