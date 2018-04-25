from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import numpy as np

def simulate_data():
    seed=1
    # the number of people in the line
    people=list(range(0,9))
    prob=[0.04,0.08,0.12,0.16,0.2,0.16,0.12,0.08,0.04]
    np.random.seed(seed)
    num=int(np.random.choice(people,1,p=list(prob)))

    # the time each person needs to order a cup of coffee (in seconds)
    order_lower, order_upper=5, 60
    order_mu, order_sigma=20, 5
    order=truncnorm((order_lower-order_mu)/order_sigma, (order_upper-order_mu)/order_sigma, loc=order_mu, scale=order_sigma)
    np.random.seed(seed)
    order_time=order.rvs(num+1)

    # the size of a cup of coffee
    cup=["tall","grande","venti"]
    cup_prob=[0.25,0.5,0.25]
    np.random.seed(seed)
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
data=simulate_data()

def breaktime(make_t,order_t,n):
    break_t = np.empty(n + 1)
    # besides Johanna, there is no person in the line
    if n==0:
        break_t[0] = order_t[0]

    # besides Johanna, there is a person in the line
    elif n==1:
        break_t[0] = order_t[0]
        if make_t[0] <= order_t[1]:
            break_t[1] = order_t[1] - make_t[0]
        else:
            break_t[1] = 0

    # generally, there are n people besides Johanna (n>1)
    else:
        break_t[0] = order_t[0]
        if make_t[0] <= order_t[1]:  # begin making the first order
            break_t[1] = order_t[1] - make_t[0]
            extra_t = 0
        else:
            break_t[1] = 0
            extra_t = make_t[0] - order_t[1]
        for i in range(2, n + 1):
            if extra_t:
                if (make_t[i - 1] + extra_t) <= order_t[i]:
                    break_t[i - 1] = order_t[i] - make_t[i - 1] - extra_t
                    extra_t = 0
                else:
                    break_t[i] = 0
                    extra_t = make_t[i - 1] + extra_t - order_t[i]
            else:
                if make_t[i - 1] <= order_t[i]:
                    break_t[i] = order_t[i] - make_t[i - 1]
                    extra_t = 0
                else:
                    break_t[i] = 0
                    extra_t = make_t[i - 1] - order_t[i]
    return break_t.sum()

print(breaktime(data[0],data[1],data[2]))

"""
fig, ax = plt.subplots(3,sharex=True)
ax[0].hist(tall_time,bins=50, normed=True)
ax[1].hist(grande_time,bins=50, normed=True)
ax[2].hist(venti_time,bins=50, normed=True)
plt.show()
"""