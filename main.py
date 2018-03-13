from __future__ import print_function
import random
import sys
import time

###############################################################################
# If it runs too slowly, turn these numbers down.
###############################################################################

MAX_CLIENTS = 1000
WORK_TO_ALLOCATE = 500000


###############################################################################
# Implement all of this.
###############################################################################

# TODO: implement me!
class WorkAllocator(object):
    def __init__(self):
        # TODO: add data structures and initialize here
        pass

    def connect(self, client):
        # TODO: handle this ^ client wanting to connect
        pass

    def give_work(self, work):
        # TODO: give this ^ piece of work to a client
        pass

    def disconnect(self, client):
        # TODO: handle this ^ client wanting to disconnect
        pass


###############################################################################
# This is the client definition. If you'd like to add anything to it, check
# with me.
###############################################################################

WORK = "blah"

class Client(object):
    def __init__(self, _id):
        self._id = _id
        self._work_given = 0
        self.connected = False

    def send(self, work):
        if work != WORK:
            raise Exception(
                "Client %d was given something that wasn't work" % self._id)
        if self.connected:
            self._work_given += 1
        else:
            raise Exception("Work given to disconnected client %d" % self._id)


###############################################################################
# Don't worry about stuff below here.
###############################################################################

CONNECT = "connect"
GIVE_WORK = "give_work"
DISCONNECT = "disconnect"

class Simulator(object):
    def __init__(self):
        self.clients = []
        self.all_clients = []
        self.next_id = 0

    def run(self, allocator):
        start = time.time()
        for i in xrange(WORK_TO_ALLOCATE):
            if time.time() - start >= 1:
                print("%.2f%% (%d/%d) done" % (
                    100*float(i+1)/WORK_TO_ALLOCATE, i, WORK_TO_ALLOCATE))
                start = time.time()
            self.step(allocator)

    def step(self, allocator):
        if len(self.clients) == 0:
            actions = [CONNECT]
        elif len(self.clients) == MAX_CLIENTS:
            actions = [GIVE_WORK, DISCONNECT]
        else:
            actions = [CONNECT, GIVE_WORK, DISCONNECT]

        action = random.choice(actions)
        if action == CONNECT:
            _id = self.next_id
            self.next_id += 1
            c = Client(_id)
            c.connected = True
            self.clients.append(c)
            self.all_clients.append(c)
            allocator.connect(c)
        elif action == GIVE_WORK:
            allocator.give_work(WORK)
        else:
            random.shuffle(self.clients)
            c = self.clients.pop(0)
            c.connected = False
            allocator.disconnect(c)

    def verify(self):
        for c in self.all_clients:
            if c._work_given > 0:
                print("Veriy finished, looks good :)")
                return

        raise Exception("No clients were given any work :(")


def main(argv):
    a = WorkAllocator()
    s = Simulator()
    s.run(a)
    s.verify()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

