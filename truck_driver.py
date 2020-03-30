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
        self.sale_item1 = init_data['sale_item1']  # ('pig', 4)
        self.sale_item2 = init_data['sale_item2']  # ('pea', 2)
        self.item_pool = {self.init_item: 5,
                          self.sale_item1[0]: 0,
                          self.sale_item2[0]: 0}

    def check_sale_item(self, items):
        for item in items:
            if item not in [self.sale_item1[0], self.sale_item2[0]]:
                return (False, '本站不收购%s' % item)
        if len(items) + self.item_pool[self.init_item] \
                + self.item_pool[self.sale_item1[0]] \
                + self.item_pool[self.sale_item2[0]] > 8:
            return (False, '卖出将超出本站库存上限')
        return (True, '')

    def check_buy_item(self, items):
        buy_dict = {self.sale_item1[0]: 0,
                    self.sale_item2[0]: 0,
                    self.init_item: 0,}
        for item in items:
            if item not in [self.sale_item1[0], self.sale_item2[0], self.init_item]:
                return (False, '本站不出售%s' % item)
            else:
                if buy_dict[item] >= self.item_pool[item]:
                    return (False, '本站商品%s数量不足' % item)
                buy_dict[item] += 1
        return (True, '')

    def sale_item(self, items):
        res, mgs = self.check_sale_item(items)
        if res:
            pass

