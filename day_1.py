import numpy as np

numbers = np.loadtxt('dat/day_1.txt')

products = np.outer(numbers, np.ones(numbers.shape[0])) + numbers
i, j = np.where(products == 2020)[0]

print(f'2 number product: {numbers[i] * numbers[j]:.0f}')

print(numbers.shape)
print(numbers.reshape(1, numbers.shape[0]).shape)
triple_product = (numbers.reshape((numbers.shape[0], 1, 1))
                  + numbers.reshape((1, numbers.shape[0], 1))
                  + numbers.reshape((1, 1, numbers.shape[0])))
print(f'''3 number product: {np.product(numbers[list(set(
    np.where(triple_product == 2020)[0]))]):.0f}''')
