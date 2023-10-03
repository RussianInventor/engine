class Config:
    scale = 1
    min_scale = 0.1
    max_scale = 2
    CHUNK_SIZE = 25
    world_percents = {"water": 40,
                      "mountains": 5,
                      "desert": 20}
    biome_percents = {"water": (15, 40),
                      "mountains": (10, 20),
                      "desert": (15, 40)}
    world_size = {"test": 7,
                  "small": 35,
                  "medium": 50,
                  "big": 80}

    @classmethod
    def set_scale(cls, delta):
        cls.scale += delta
        if cls.scale > cls.max_scale:
            cls.scale = cls.max_scale
        if cls.scale < cls.min_scale:
            cls.scale = cls.min_scale
