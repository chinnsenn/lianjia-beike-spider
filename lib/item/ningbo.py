#!/usr/bin/env python
# coding=utf-


class Ningbo(object):
    def __init__(self, date, contract_no, district, street, record):
        self.date = date
        self.contract_no = contract_no
        self.district = district
        self.street = street
        self.record = record

    def text(self):
        return self.date + "," + \
            self.contract_no + "," + \
            self.district + "," + \
            self.street + "," + \
            self.record
