from cpo import CPO

from sys import argv



if len(argv) > 1 and argv[1] == "connect":
    CPO.ip = argv[2]
    CPO.port = int(argv[3])
    CPO.is_client = True
elif len(argv) == 1:
    CPO.is_client = False
    CPO.is_server = False
elif len(argv) > 1 and argv[1] == "host":
    CPO.ip = argv[2]
    CPO.port = int(argv[3])

CPO.start_game()

