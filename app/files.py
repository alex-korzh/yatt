CHUNK_SIZE = 256


def wisdom():
    with open("./assets/alice-1.txt") as f:
        while content := f.read(CHUNK_SIZE):
            yield content
