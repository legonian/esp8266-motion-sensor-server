import uos, machine, gc, webrepl, os, socket, time, network

webrepl.start()

def print_file(file_name):
    file_arr = open(file_name).read().split('\n')
    for line in file_arr:
        print(line)

def print_m():
    print_file("main.py")
