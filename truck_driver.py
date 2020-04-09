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
        for item in items:
            if item not in self.sale_item:
                return (False, '本站不收购%s' % item)
        if len(items) + self.item_pool_amount > 8:
            return (False, '卖出将超出本站库存上限')
        return (True, '')

    def check_buy_item(self, items):
        buy_dict = {x: 0 for x in self.item_pool}
        for item in items:
            if item not in self.item_pool:
                return (False, '本站不出售%s' % item)
            else:
                if buy_dict[item] >= self.item_pool[item]:
                    return (False, '本站商品%s数量不足' % item)
                buy_dict[item] += 1
        return (True, '')

    def sale_item(self, items):
        res, msg = self.check_sale_item(items)
        if res:
            coin = 0
            for item in items:
                self.item_pool[item] += 1
                self.item_pool_amount += 1
                coin += self.sale_item[item]
            return res, coin
        else:
            return res, msg

    def buy_item(self, items):
        res, msg = self.check_buy_item(items)
        if res:
            for item in items:
                pass



