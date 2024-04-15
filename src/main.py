from config_loader import config
from helpers import time_it


@time_it
def main():
    print(config)


if __name__ == '__main__':
    main()
