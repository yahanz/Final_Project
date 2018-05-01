# Title: Coffee Shop Monte Carlo Simulation

## Team Member(s):
Zhongwei Huang, Yahan Zhang

# Monte Carlo Simulation Scenario & Purpose:
Johanna comes to a coffee shop and wants to buy a cup of coffee. There are some people waiting in a line, so Johanna wants to estimate how long she needs to wait for to get a coffee.

The statistics we are interested in are Johanna's wait time and two baristas’ break time.

## Simulation's variables of uncertainty
1. besides Johanna, the number of people in the line
      Number      0     1    2     3     4     5     6     7     8
      Pr        0.04  0.08  0.12  0.16  0.2   0.16  0.12  0.08  0.04

2. size of a cup of coffee: tall, grande, venti
      Size      Tall      Grande      Venti
      Pr        0.25        0.5       0.25

3. time of ordering a cup of coffee: Truncated Normal (mean=25, s.d=5, lower=5, upper=60)
4. time of making a tall cup of coffee: Truncated Normal (mean=25, s.d=5, lower=5, upper=80)
5. time of making a grande cup of coffee: Truncated Normal (mean=28, s.d=7, lower=5, upper=80)
6. time of making a venti cup of coffee:Truncated Normal (mean=30, s.d=8, lower=5, upper=80)

After we generate times from truncated normal distributions, we would round them into integers.

## Hypothesis or hypotheses before running the simulation:


## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)


## Instructions on how to use the program:
Run Simulation.py
By changing the argument in function simulation, you can change the times of Monte Carlo Simulation.

## All Sources Used:
Miller & Ranum: Problem Solving with Algorithms and Data Structures Using Python, Section 3.4, pages 106-119
