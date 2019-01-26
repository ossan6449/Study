def get_fortune():
    import random # randamではなく、randomなので注意です
    results = ['大吉', '吉', '小吉', '凶', '大凶', '末吉']
    return random.choice(results)