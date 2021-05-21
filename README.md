# Order CLI application
> Order is simple application to print your orders.

## Table of contents
* [Introduction](#introduction)
* [Requirements](#requirements)
* [Usage](#usage)
* [Contributing](#contributing)
* [Contact](#contact)
* [License](#license)

# Introduction

`Order` is a simple CLI application for printing the numbers from 1 to 10 in random to the terminal.

## Requirements

* You need `Python` to run Order CLI application. You can have multiple python versions (2.x and 3.x) installed on the same system without problems. By default python installed on all Linux distributions and MacOS, but if you need to install the python on your system, please follow below instructions:

In Fedora, RHEL 8 and CentOS 8 you can install python 3 like this:

```sh
sudo dnf install python3 python3-pip
```

In Ubuntu, Mint and Debian you can install Python 3 like this:

```sh
sudo apt-get install python3 python3-pip
```

In MacOS, you can install python like this:

```sh
brew install python
```

For other Linux flavors and Windows, packages are available at [Python website](https://www.python.org/getit/).

* Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `click` Python package.

```sh
pip3 install click
```

If you have Python 2, you need to use `pip` and run this command:

```sh
pip install click
```

## Usage

To run `Order` CLI application you just need to open a terminal on your system and run the application like this:

```sh
python3 order.py
```

The application by default print the numbers from 1 to 10 in random, but If you want to print your orders on different range you can use `--first` and `--last` option to define your range. For example:

```sh
python3 order.py --first 1 --last 20
```

For more information about the application, please read the help:

```sh
python3 order.py --help
```

Sample help output:

```sh
python3 order.py --help
Usage: order.py [OPTIONS]

Options:
  --first INTEGER  First number of the range.
  --last INTEGER   Last number of the range
  --help           Show this message and exit.
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

**Project website**: https://github.com/hos7ein/order

**Personal website**: https://fedorafans.com

**Author**: Hossein Aghaie <hossein.a97@gmail.com>

**Twitter**: Hossein Aghaie [@hos7ein](https://twitter.com/hos7ein)

## License

`Order applicaion` source code is available under the GPL-3.0 [License](/LICENSE).
