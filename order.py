from __future__ import print_function
import click
from random import sample

@click.command()
@click.option('--first', default=1, help='First number of the range.')
@click.option('--last', default=10, help='Last number of the range')

def printRandNumber(first, last):
    listRandNumbers = sample(range(first, last+1), last) # Append Uniqe random numbers in a list.
    for i in range(len(listRandNumbers)):
        print(listRandNumbers[i], end = '  ')

if __name__ == '__main__':
    printRandNumber()
