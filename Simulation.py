from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def simulate_data():
    #seed=1
    # the number of people in the line
    people=list(range(0,9))
    prob=[0.04,0.08,0.12,0.16,0.2,0.16,0.12,0.08,0.04]
    #np.random.seed(seed)
    num=int(np.random.choice(people,1,p=list(prob)))

    # the time each person needs to order a cup of coffee (in seconds)
    order_lower, order_upper=5, 60
    order_mu, order_sigma=25, 5
    order=truncnorm((order_lower-order_mu)/order_sigma, (order_upper-order_mu)/order_sigma, loc=order_mu, scale=order_sigma)
    #np.random.seed(seed)
    order_time=order.rvs(num+1)

    # the size of a cup of coffee
    cup=["tall","grande","venti"]
    cup_prob=[0.25,0.5,0.25]
    #np.random.seed(seed)
    cup_size=np.random.choice(cup,num+1,p=list(cup_prob))

    # the time a barista needs to make a cup of coffee
    make_t=[]
    for i in range(num+1):
        lower,upper=5,80
        if cup_size[i]=="tall":
            mu=25
            sigma=5
        elif cup_size[i]=="grande":
            mu=28
            sigma=7
        elif cup_size[i]=="venti":
            mu=30
            sigma=8
        dist=truncnorm((lower-mu)/sigma, (upper-mu)/sigma, loc=mu, scale=sigma)
        make_t.append(float(dist.rvs(1)))
    return [make_t,list(order_time),num]

def calculate_time(make_t,order_t,n):
    if n==0:
        wait_t=order_t[0]+make_t[0]
        break_t=order_t[0]
    else:
        order_abs=[order_t[0]]
        for i in range(n):
            order_abs.append(order_abs[i]+order_t[i+1])
        make_abs=[[order_t[0],order_t[0]+make_t[0]]]
        for i in range(n):
            start=max(order_abs[i+1],make_abs[i][1])
            end=start+make_t[i+1]
            make_abs.append([start,end])
        wait_t=make_abs[n][1]
        break_t=sum([time[0] for time in make_abs])-sum([time[1] for time in make_abs])+make_abs[n][1]
    return [wait_t,break_t]

if __name__ == '__main__':

    wait_time = []
    break_time = []

    for i in range(10000):
        data = simulate_data()
        result = calculate_time(data[0], data[1], data[2])
        wait_time.append(result[0])
        break_time.append(result[1])

    fig, ax = plt.subplots(2)
    ax[0].hist(wait_time, bins=100, normed=True)
    ax[1].hist(break_time, bins=100, normed=True)
    plt.show()

    wait_time=pd.DataFrame(wait_time)
    print(wait_time.describe())

    break_time = pd.DataFrame(break_time)
    print(break_time.describe())
"""
fig, ax = plt.subplots(3,sharex=True)
ax[0].hist(tall_time,bins=50, normed=True)
ax[1].hist(grande_time,bins=50, normed=True)
ax[2].hist(venti_time,bins=50, normed=True)
plt.show()
"""