import re


def is_vehicle_parked(parking_lot: list, plate: str):
    for p in parking_lot:
        if p['plate'] == plate:
            return p
    return False


def is_plate_valid(plate: str):
    return bool(re.match(r"([a-zA-Z]{3})-[0-9]{4}", plate))


def get_time_spent(t1, t2):
    time = (t2 - t1).total_seconds()
    hours = time // 3600
    time = time % 3600
    minutes = time // 60
    return hours, minutes
