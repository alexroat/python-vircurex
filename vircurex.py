import time
import json
import urllib
import urllib2
import hashlib
import random


class Vircurex(object):
    domain = "https://api.vircurex.com"  # domain

    @classmethod
    def simpleRequest(cls, command, **params):
        url = "%s/api/%s.json?%s" % (cls.domain, command, urllib.urlencode(params.items()))  # url
        opener = urllib2.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")]
        data = opener.open(url).read()
        return json.loads(data)

    @classmethod
    def secureRequest(cls, user, secret, command, tokenparams, **params):
        t = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())  # UTC time
        txid = hashlib.sha256(
            "%s-%f" % (t, random.randint(0, 1 << 31))).hexdigest()  # unique trasmission ID using random hash
        # token computation
        vp = [command] + map(lambda x: params[x], tokenparams)
        token_input = "%s;%s;%s;%s;%s" % (secret, user, t, txid, ';'.join(map(str, vp)))
        token = hashlib.sha256(token_input).hexdigest()
        # cbuilding request
        reqp = [("account", user), ("id", txid), ("token", token), ("timestamp", t)] + params.items()
        url = "%s/api/%s.json?%s" % (cls.domain, command, urllib.urlencode(reqp))  # url
        data = urllib.urlopen(url).read()
        return json.loads(data)

    # insert user and a dict with secrets set in your account settings (e.g. : create_order=>q12we34r5t)
    def __init__(self, user=None, secrets=None):
        self.user = user
        if secrets is None:
            self._secrets = {}
        else:
            self.secrets = secrets

    # trade API
    def get_balance(self, currency):
        return Vircurex.secureRequest(self.user, self.secrets["get_balance"], "get_balance", ["currency"],
                                      currency=currency)

    def get_balances(self):
        return Vircurex.secureRequest(self.user, self.secrets["get_balance"], "get_balances", [])

    def create_order(self, ordertype, amount, currency1, unitprice, currency2):
        return Vircurex.secureRequest(self.user, self.secrets["create_order"], "create_order",
                                      ["ordertype", "amount", "currency1", "unitprice", "currency2"],
                                      ordertype=ordertype, amount=amount, currency1=currency1, unitprice=unitprice,
                                      currency2=currency2)

    def release_order(self, orderid):
        return Vircurex.secureRequest(self.user, self.secrets["release_order"], "release_order", ["orderid"],
                                      orderid=orderid)

    def delete_order(self, orderid, otype):
        return Vircurex.secureRequest(self.user, self.secrets["delete_order"], "delete_order", ["orderid", "otype"],
                                      orderid=orderid, otype=otype)

    def read_order(self, orderid, otype):
        return Vircurex.secureRequest(self.user, self.secrets["read_order"], "read_order", ["orderid"], orderid=orderid,
                                      otype=otype)

    def read_orders(self, otype):
        return Vircurex.secureRequest(self.user, self.secrets["read_orders"], "read_orders", [], otype=otype)

    def read_orderexecutions(self, orderid):
        return Vircurex.secureRequest(self.user, self.secrets["read_orderexecutions"], "read_orderexecutions",
                                      ["orderid"], orderid=orderid)

    def create_coupon(self, amount, currency):
        return Vircurex.secureRequest(self.user, self.secrets["create_coupon"], "create_coupon", ["amount", "currency"],
                                      amount=amount, currency=currency)

    def redeem_coupon(self, coupon):
        return Vircurex.secureRequest(self.user, self.secrets["redeem_coupon"], "redeem_coupon", ["coupon"],
                                      coupon=coupon)

    #  # info API
    def get_lowest_ask(self, base, alt):
        return Vircurex.simpleRequest("get_lowest_ask", base=base, alt=alt)

    def get_highest_bid(self, base, alt):
        return Vircurex.simpleRequest("get_highest_bid", base=base, alt=alt)

    def get_last_trade(self, base, alt):
        return Vircurex.simpleRequest("get_last_trade", base=base, alt=alt)

    def get_volume(self, base, alt):
        return Vircurex.simpleRequest("get_volume", base=base, alt=alt)

    def get_info_for_currency(self):
        return Vircurex.simpleRequest("get_info_for_currency")

    def get_info_for_1_currency(self, base, alt):
        return Vircurex.simpleRequest("get_info_for_1_currency", base=base, alt=alt)

    def orderbook(self, base, alt):
        return Vircurex.simpleRequest("orderbook", base=base, alt=alt)

    def orderbook_alt(self, alt):
        return Vircurex.simpleRequest("orderbook_alt", alt=alt)

    def trades(self, base, alt, since):
        return Vircurex.simpleRequest("trades", base=base, alt=alt, since=since)

    def get_currency_info(self):
        return Vircurex.simpleRequest("get_currency_info")
