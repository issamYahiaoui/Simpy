import simpy
import numpy as np 




def generate_interarrival():
	return np.random.exponential(1./3.0)

def generate_service():
	return np.random.exponential(1. / 4.0)


def CafeShop_run(env, servers ):
	i=0
	while True:
		i +=1
		yield env.timeout(generate_interarrival())
		env.process(customer(env,i,servers))




wait_t =[] 


def customer(env, customer, servers):
	with servers.request() as request:
		t_arrivaal = env.now
		print  (env.now ,  'customer {} arrives'.format(customer))
		yield request
		print  (env.now ,  'customer {} is being served '.format(customer))

		yield env.timeout(generate_service())
		print  (env.now ,  'customer {} departs'.format(customer))
		t_depart = env.now
		wait_t.append(t_depart - t_arrivaal)

obs_times =[]
q_length = []

def observe  (env , servers):
	while True :
		obs_times.append(env.now)
		q_length.append(len(servers.queue))
		yield env.timeout(1.0)

np.random.seed(0)


env = simpy.Environment()
servers  =  simpy.Resource(env, capacity=1)
env.process(CafeShop_run(env,servers))
env.process(observe(env,servers))


env.run(until=10)

def getTempsMoy():
	result = 0
	for w in wait_t:
		result = result + w
	return result / len(wait_t)

import matplotlib.pyplot as plt
index  = 0

for wa in wait_t:
	index = index + 1
	print "------------------------------------------"
	print "Customer",index, "| Waited ", wa - generate_service(), "min "

print(len(wait_t))
print("Temps d'attente moyen " , getTempsMoy())
print(obs_times)
print(q_length)
plt.figure()
plt.hist(wait_t)
plt.xlabel("Waiting time (min) ")
plt.ylabel("Number of customers ")
plt.title("Waiting time ")
plt.show()
plt.figure()
plt.step(obs_times,q_length)
plt.xlabel("Time (min) ")
plt.ylabel("Queue length ")
plt.title("Queue Length")

plt.show()











