import logging
from gui import YattUI

logging.basicConfig(
    filename="/home/alex/.cache/yatt/all.log",  # TODO create dirs
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


def main():
    app = YattUI()
    result = app.run()
    print(result)


if __name__ == "__main__":
    main()
