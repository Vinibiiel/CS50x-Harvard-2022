def main():
    hashes = input("Height: ")
    while(not hashes.isdigit() or int(hashes)<=0 or int(hashes)>= 9):
        hashes = input("Height: ")
    hashes = int(hashes)


    for i in range(1,hashes+1):
        value = hashes-i
        print(f' ' * value)
        print("#"*i,end="  ")
        print("#"*i)
main()