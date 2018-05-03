# Title: Coffee Shop Monte Carlo Simulation

## Team Member(s):
Zhongwei Huang, Yahan Zhang

# Monte Carlo Simulation Scenario & Purpose:
Johanna comes to a coffee shop and wants to buy a cup of coffee. There are some people waiting in a line, so Johanna wants to estimate how long she needs to wait for to get a coffee.

The statistics we are interested in are Johanna's wait time and two baristas’ break time.

## Simulation's variables of uncertainty
besides Johanna, the number of people in the line     

      Number      0     1    2     3     4     5     6     7     8
      
      Pr        0.04  0.08  0.12  0.16  0.2   0.16  0.12  0.08  0.04

size of a cup of coffee: tall, grande, venti     

      Size      Tall      Grande      Venti
      
      Pr        0.25        0.5       0.25

time of ordering a cup of coffee: Truncated Normal (mean=25, std=5, lower=5, upper=60)

time of making a tall cup of coffee: Truncated Normal (mean=25, std=5, lower=5, upper=80)

time of making a grande cup of coffee: Truncated Normal (mean=28, std=7, lower=5, upper=80)

time of making a venti cup of coffee:Truncated Normal (mean=30, std=8, lower=5, upper=80)

After we generate times from truncated normal distributions, we would round them into integers.

## Hypothesis or hypotheses before running the simulation:
The wait time and break time may follow normal distribution. 

The barista B may have more break time.

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)
The wait time and break time do follow normal distribution. 

The barista B does have more break time.

## Instructions on how to use the program:
Run Simulation.py

By changing the argument in function simulation, you can change the times of Monte Carlo Simulation.

## All Sources Used:
Miller & Ranum: Problem Solving with Algorithms and Data Structures Using Python, Section 3.4, pages 106-119
