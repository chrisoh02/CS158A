Before running the 1st terminal, make sure myleprocess.py says 
sip, sp, cip, cp = read_config('config1.txt')
node = Node(sip, sp, cip, cp, 'log1.txt')
Then run python3 myleprocess.py

Open a 2nd terminal and change myleprocess.py to say 
sip, sp, cip, cp = read_config('config2.txt')
node = Node(sip, sp, cip, cp, 'log2.txt')
and then run the process.

Repeat as with config3 and log3 for the 3rd terminal. 

This should finish the ring and let the election begin.

Note: it would've made more sense to simply pass the config and log file names as arguments in the terminal, but PyCharm would not allow for additional arguments.
