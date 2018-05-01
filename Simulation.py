from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def simulate_data() -> list:
    """
    Generate data for Monte Carlo Simulation
    :return: a list of data

    >>> np.random.seed(1)
    >>> data=simulate_data()
    >>> print(data[1])
    [28.0, 7.0, 22.0, 20.0, 18.0]
    >>> print(data[0])
    [27, 22, 36, 15, 31]
    """

    # seed=1
    # the number of people in the line
    people=list(range(9))
    prob=[0.04,0.08,0.12,0.16,0.2,0.16,0.12,0.08,0.04]
    #np.random.seed(seed)
    num=int(np.random.choice(people,1,p=list(prob)))

    # the time each person needs to order a cup of coffee (in seconds)
    order_lower, order_upper=5, 60
    order_mu, order_sigma=25, 5
    order=truncnorm((order_lower-order_mu)/order_sigma, (order_upper-order_mu)/order_sigma, loc=order_mu, scale=order_sigma)
    order_time=order.rvs(num+1)
    # the size of a cup of coffee
    cup=["tall","grande","venti"]
    cup_prob=[0.25,0.5,0.25]
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
        make_t=[round(x) for x in make_t]
        order_time=[round(x) for x in order_time]
    return [make_t,order_time,num]

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Barista:
    def __init__(self):
        self.break_t=0
        self.currentOrder = None
        self.timeRemaining = 0

    def busy(self):
        if self.currentOrder != None:
            return True
        else:
            return False

    def tick(self):
        if self.currentOrder != None:
            self.timeRemaining -= 1
            if self.timeRemaining <= 0:
                self.timeRemaining=0
                self.currentOrder = None

    def nextOrder(self,make_t):
        self.timeRemaining=make_t
        self.currentOrder=1

def simulation(times=1) -> list:
    """
    Do Monte Carlo Simulation
    :param times: times of doing Monte Carlo Simulation
    :return: a list of a wait time list and two break time lists

    >>> np.random.seed(1)
    >>> results=simulation()
    >>> print(results)
    [[126], [32], [89]]
    """

    wait_time = []
    break_time_a = []
    break_time_b = []

    for i in range(times):
        data = simulate_data()
        customers_q = Queue()
        after_order = Queue()
        barista_a = Barista()
        barista_b = Barista()
        n = data[2] + 1          # the number of people in the line (including Johanna)
        wait_t = 0

        # construct customers queue
        for i in range(n):
            customers_q.enqueue((data[1][i], data[0][i]))

        # a customer is ordering
        for count in range(n):
            customer = customers_q.dequeue()
            order_t = customer[0]

            while order_t > 0:
                order_t -= 1
                wait_t += 1

                if (not barista_a.busy()) and (after_order.isEmpty()):
                    barista_a.break_t += 1
                elif (not barista_a.busy()):
                    make_t = after_order.dequeue()
                    barista_a.nextOrder(make_t)
                    barista_a.tick()
                else:
                    barista_a.tick()

                if (not barista_b.busy()) and (after_order.isEmpty()):
                    barista_b.break_t += 1
                elif (not barista_b.busy()):
                    make_t = after_order.dequeue()
                    barista_b.nextOrder(make_t)
                    barista_b.tick()
                else:
                    barista_b.tick()
            after_order.enqueue(customer[1])

        # after all customers have finished ordered
        if not barista_a.busy():
            make_t = after_order.dequeue()
            barista_a.nextOrder(make_t)
        elif not barista_b.busy():
            make_t = after_order.dequeue()
            barista_b.nextOrder(make_t)

        while barista_a.busy() or barista_b.busy():
            wait_t += 1
            if (not barista_a.busy()) and (not after_order.isEmpty()):
                make_t = after_order.dequeue()
                barista_a.nextOrder(make_t)
                barista_a.tick()
            elif (not barista_a.busy()):
                barista_a.break_t += 1
            else:
                barista_a.tick()

            if (not barista_b.busy()) and (not after_order.isEmpty()):
                make_t = after_order.dequeue()
                barista_b.nextOrder(make_t)
                barista_b.tick()
            elif (not barista_b.busy()):
                barista_b.break_t += 1
            else:
                barista_b.tick()

        wait_time.append(wait_t)
        break_time_a.append(barista_a.break_t)
        break_time_b.append(barista_b.break_t)

    return [wait_time,break_time_a,break_time_b]

if __name__ == '__main__':

    mysimulations=simulation(5000)

    # summary of Johanna's wait time, barista_a's break time and barista_b's break time
    wait_time = pd.DataFrame(mysimulations[0])
    print(wait_time.describe())

    break_time_a = pd.DataFrame(mysimulations[1])
    print(break_time_a.describe())

    break_time_b = pd.DataFrame(mysimulations[2])
    print(break_time_b.describe())

    # density plot
    plt.figure(1)
    plt.subplot(211)
    sns.distplot(list(wait_time.loc[:,0]), hist = False, kde = True)
    plt.title('Wait Time')

    plt.subplot(212)
    sns.distplot(break_time_a, hist=False, kde=True,label='Barista A')
    sns.distplot(break_time_b, hist=False, kde=True,label='Barista B')
    plt.title('Break Time')
    plt.legend(title='Barista')

    plt.show()