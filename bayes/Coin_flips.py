import numpy as np
data_coin_flips = np.random.randint(2, size=1000)


print(np.mean(data_coin_flips))


bernoulli_flips = np.random.binomial(n=1, p=.5, size=1000)
print(np.mean(bernoulli_flips))
