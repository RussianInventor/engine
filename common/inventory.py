from . import config


class Inventory:
    def __init__(self, master, w=10, h=4):
        self.items = [None for i in range(w * h)]
        self.w = w
        self.h = h
        self.current_item = None
        self.current_ind = None
        self.master = master
        self.master_id = master.id

    def leave(self):
        if self.current_item is not None:
            self.add(self.current_item, self.current_ind)
            self.clear_buffer()

    def clear_buffer(self):
        self.current_ind = None
        self.current_item = None

    def select(self, index):
        self.current_ind = index

    def take(self, index):
        self.select(index)
        self.current_item = self.items[self.current_ind]
        self.items[self.current_ind] = None

    def get(self, index):
        return self.items[index]

    def add(self, item, index=None):
        item.master_id = self.master_id
        if index is None:
            try:
                self.items[self.items.index(None)] = item
                self.clear_buffer()
                return True
            except ValueError:
                return False
        else:
            if self.items[index] is None:
                self.items[index] = item
                self.clear_buffer()
                return True
            else:
                return False

    def replace(self, ind):
        item = self.items[ind]
        self.items[ind] = self.current_item
        self.items[self.current_ind] = item
        self.clear_buffer()

    def pop(self):
        self.current_item.master_id = None
        self.current_item.x, self.current_item.x = self.master.x, self.master.y
        self.clear_buffer()

    def remove(self, ind):
        self.items[ind] = None
