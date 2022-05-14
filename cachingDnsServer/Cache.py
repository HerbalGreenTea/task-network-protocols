import os
from time import time
import pickle


class Record:
    def __init__(self, name_domain, msg_type, ttl, addresses, time_record):
        self.name_domain = name_domain
        self.resp_type = msg_type
        self.ttl = ttl
        self.addresses = addresses
        self.time_record = time_record

    def get_string(self):
        return "domain: {domain}\ntype: {type}\nttl: {ttl}\naddresses: {addresses}".format(
            domain=self.name_domain,
            type=self.resp_type,
            ttl=self.ttl,
            addresses=self.addresses
        )


class Cache:
    def __init__(self):
        self.file_name = "cache.txt"
        self.records = self.load_cache()

    def load_cache(self):
        try:
            if os.path.getsize(self.file_name) > 0:
                with open(self.file_name, 'rb+') as cache_file:
                    cache = pickle.load(cache_file)
                    return cache
        except FileNotFoundError:
            return {}

        return {}

    def save_cache(self):
        with open(self.file_name, 'wb') as cache_file:
            pickle.dump(self.records, cache_file)

    def clear_cache(self):
        with open(self.file_name, 'w') as cache_file:
            cache_file.close()

    def add_record(self, name_domain, msg_type, addresses, ttl):
        self.records[name_domain + msg_type] = Record(name_domain, msg_type, ttl, addresses, int(round(time())))
        self.save_cache()

    def remove_record(self, name_domain, msg_type):
        self.records.pop(name_domain + msg_type)
        self.save_cache()

    def get_record(self, name_domain, msg_type):
        return self.records.get(name_domain + msg_type)

    def print_cache(self):
        for rec in self.records.values():
            print(rec.get_string())
