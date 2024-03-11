class Config:
    scale = 10
    min_scale = 0.1
    max_scale = 200
    CHUNK_SIZE = 25
    world_percents = {"water": 50,
                      "mountains": 5,
                      "desert": 20}
    biome_percents = {"water": (15, 20),
                      "mountains": (10, 20),
                      "desert": (25, 40)}
    world_size = {"test": 7,
                  "small": 35,
                  "medium": 50,
                  "big": 80}