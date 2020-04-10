import random

CardPool = []
DropCardPool = []

def generate_card_pool():
    global CardPool
    CardPool.clear()
    CardPool += ['cow'] * 8 + ['pig'] * 8 + ['corn'] * 15 + ['pea'] * 15 \
                + ['1step'] * 10 + ['2step'] * 6 + ['3step'] * 3

def shuffle_card(card_pool):
    for i in range(len(card_pool)-1, 0, -1):
        j = random.randint(0, i)
        tmp = card_pool[j]
        card_pool[j] = card_pool[i]
        card_pool[i] = tmp

class PlaceCard:
    def __init__(self, init_data):
        self.name = init_data['name']
        self.park_truck = None
        self.init_item = init_data['init_item']    # 'pig'
        self.sale_item = init_data['sale_item']    # {'pig': 4, 'pea':4}
        self.item_pool = self.get_item_pool()
        self.item_pool_amount = 5

    def get_item_pool(self):
        item_pool = {x: 0 for x in self.sale_item}
        item_pool[self.init_item] = 5
        return item_pool

    def check_sale_item(self, items):
        # param: ('pea': 2):
        if items[0] not in self.sale_item:
            return (False, '本站不收购%s' % items[0])
        if items[1] + self.item_pool_amount > 8:
            return (False, '卖出将超出本站库存上限')
        return (True, '')

    def check_buy_item(self, items):
        # 规则 买回本站收购的商品时 需要2个对应商品订单
        # param: ('pea': 2):
        if items[0] not in self.item_pool:
            return (False, '本站不出售%s' % items[0])
        if items[0] in self.sale_item:
            if items[1] % 2 != 0:
                return (False, '买回本站收购的商品时 需要2个对应商品订单')
            if items[1] // 2 > self.item_pool[items[0]]:
                return (False, '商品%s数量不足' % items[0])
        else:
            if items[1] > self.item_pool[items[0]]:
                return (False, '商品%s数量不足' % items[0])
        return (True, '')

    def sale_item(self, items):
        # 货车使用订单卖出货物 赚取金币
        res, msg = self.check_sale_item(items)
        if res:
            coin = 0
            self.item_pool[items[0]] += items[1]
            self.item_pool_amount += items[1]
            coin += self.sale_item[items[0]]
            return res, coin
        else:
            return res, msg

    def buy_item(self, items):
        # 货车使用订单装运货物
        res, msg = self.check_buy_item(items)
        if res:
            if items[0] in self.sale_item:
                self.item_pool[items[0]] -= items[1] // 2
                self.item_pool_amount -= items[1] // 2
                return res, (items[0], items[1] // 2)
            else:
                self.item_pool[items[0]] -= items[1]
                self.item_pool_amount -= items[1]
                return res, items
        else:
            return res, msg


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.coin = 5
        self.card = []
        self.items = {"pea": 0,
                      "corn": 0,
                      "cow": 0,
                      "pig": 0}
        self.item_amount = 0

    def use_order_card(self, index_list):
        pass

    def use_oil_card(self, index_list):
        pass

    def exchange_card(self, index_list):
        pass

    def get_card(self):
        pass

    def load_item(self, items):
        pass

    def unload_item(self, items):
        pass



