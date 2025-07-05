history = []

def is_anomaly(data, threshold=2.5):
    global history
    price = data['price']
    history.append(price)
    if len(history) < 10:
        return False

    recent = history[-10:]
    avg = sum(recent) / len(recent)
    deviation = abs(price - avg) / avg

    return deviation > threshold / 100