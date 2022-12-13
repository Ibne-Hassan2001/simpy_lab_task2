#Trying this lab for almost two weeks. I tried to implement as much as I could have.
#Ibne Hassan
#ID : 22241121

import random

import simpy


RANDOM_SEED = 42
NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

#we will surely need a counter no function to track the counter

def new_counter_open(env, numm, interval, machines):
   

    for m in machines:
        env.process(m.run())
        print('Counter: Opened %s' % numm)
    t = random.expovariate(1.0 / interval)    
    yield env.timeout(t)



# imported functions from machine shop,  if it works in case
    # def break_machine(self):
    #     """Break the machine every now and then."""
    #     while True:
    #         yield self.env.timeout(time_to_failure())
    #         if not self.broken:
    #             # Only break the machine if it is currently working.
    #             self.process.interrupt()
# class Machine_shop:

#     def __init__(self, env, resource_dict, machine_id, store):
#         self.env = env
#         self.resource_dict = resource_dict
#         self.machine_id = machine_id
#         self.resource = self.resource_dict[self.machine_id]
#         self.store = store


#     def do_something(self, item):
#         arrive = env.now
#         with self.resource.request() as req:
#             yield req
#             yield self.env.timeout(3)
#         print('%7.4f Counter%00d: Opened' % (arrive, self.machine_id))
#         print(f"{arrive} - counter: {self.machine_id} - deal with item: {item}")

#     def run(self):
#         while True:
#             item = yield self.store.get()
#             self.env.process(self.do_something(item))

def customer(env, name, counter, time_in_bank):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    
    print('%7.4f Counter : Opened' % (arrive))
      
    print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s: Served by Counter ' % (env.now, name))
            

        else:
            # We reneged
            print('%7.4f %s: About to give up after %6.3f' % (env.now, name, wait))
            # print('%7.4f Counter : Opened' % (arrive))



# Setup and start the simulation
print('Bank renege trying hard')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()
