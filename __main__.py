
from module.statik import *
from module.universen.universum2 import universum2
from messagebox import messagebox

msg = messagebox()
msg.state("Start")
uni = universum2()
uni.run()
uni.next_system()
uni.run()