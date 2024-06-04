from os import path


class Config:
    SOURCE = path.join("common", "source")
    scale_step = 0.1
    min_scale = 0.5
    max_scale = 10
    scales = [i/10 for i in range(int(min_scale*10), max_scale*10, int(scale_step*10))]
    scale_index = len(scales)-1
    CHUNK_SIZE = 175
    world_percents = {"water": 50,
                      "mountains": 5,
                      "desert": 20}
    biome_percents = {"water": (15, 20),
                      "mountains": (10, 20),
                      "desert": (25, 40)}
    world_size = {"test": 10,
                  "small": 35,
                  "medium": 50,
                  "big": 80}

    @classmethod
    @property
    def scale(cls):
        return cls.scales[cls.scale_index]

