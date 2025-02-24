from . import config
import json
from .utils import Encoder


class Inventory:
    def __init__(self, master, w=10, h=4):
        self.items = [None for i in range(w * h)]
        self.w = w
        self.h = h
        self.current_item_id = None
        self.current_ind = None
        self.master = master
        self.master_id = master.id
        self.changes = False

    def set_changes(self):
        self.changes = True

    def pop_changes(self):
        if self.changes:
            self.changes = False
            return self.json_dict()
        else:
            return {}

    def json_dict(self):
        d = self.__dict__.copy()
        d.pop('master')
        for i in range(len(d['items'])):
            try:
                d['items'][i] = d['items'][i].__dict__
            except AttributeError:
                pass
        return d
        # return json.dumps(d, cls=Encoder)

    def leave(self):
        if self.current_item_id is not None:
            self.add(self.current_item_id, self.current_ind)
            self.clear_buffer()

    def clear_buffer(self):
        self.current_ind = None
        self.current_item_id = None

    def select(self, index=None, id=None):
        if id is not None:
            self.current_ind = self.items.index(id)
            return
        elif index is not None:
            self.current_ind = index
        else:
            raise RuntimeError("Index and id are None")

    def take(self, index):
        if self.items[index] is None:
            return
        self.select(index)
        self.current_item_id = self.items[self.current_ind]
        self.items[self.current_ind] = None
        self.set_changes()

    def get(self, index):
        return self.items[index]

    def add(self, item, index=None):
        if isinstance(item, str):
            item_id = item
        else:
            item_id = item.id
            item.master_id = self.master_id
        self.set_changes()
        if index is None:
            try:
                self.items[self.items.index(None)] = item_id
                self.clear_buffer()
                return True
            except ValueError:
                return False
        else:
            if self.items[index] is None:
                self.items[index] = item_id
                self.clear_buffer()
                return True
            else:
                return False

    def replace(self, ind):
        item_id = self.items[ind]
        self.items[ind] = self.current_item_id
        self.items[self.current_ind] = item_id
        self.clear_buffer()
        self.set_changes()

    def pop(self, world):
        removed_id = self.current_item_id
        obj = world.get_object(removed_id)
        obj.set_master_id(None)
        obj.set_pos(self.master.x, self.master.y)
        self.remove(ind=self.current_ind)
        self.clear_buffer()
        return obj

    def remove(self, ind):
        self.items[ind] = None
        self.set_changes()
