from fastapi import FastAPI, Response, status
from datetime import datetime
from utils import is_plate_valid, is_vehicle_parked, get_time_spent
import uuid

history = []
vacancies = []

app = FastAPI()


@app.get("/plates", status_code=200)
def get_vehicles():
    return {'vehicles': vacancies}


@app.get("/history", status_code=200)
def get_history():
    global history
    return {'history': history}


@app.get("/plates/{plate}", status_code=200)
def get_vehicles(plate: str, response: Response):
    if not is_plate_valid(plate):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {'message': f'Vehicle {plate} does not have a valid plate'}

    vehicle = is_vehicle_parked(vacancies, plate)
    if vehicle:
        return {'vehicle': vehicle}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'Vehicle {plate} is not registered in the parking lot'}


@app.post("/register/{plate}", status_code=200)
def register_vehicle(plate: str, response: Response):
    global vacancies
    global history
    if is_plate_valid(plate) and not is_vehicle_parked(vacancies, plate):
        today_date = datetime.now()
        _id = uuid.uuid4()
        history.append({
            'id': _id,
            'plate': plate,
            'register_time': today_date,
            'is_paid': False
        })
        vacancies.append({
            'id': _id,
            'plate': plate,
            'register_time': today_date,
            'is_paid': False
        })
        return {'message': f'Vehicle {plate} registered at {today_date}'}

    elif not is_plate_valid(plate):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {'message': f'Vehicle {plate} does not have a valid plate'}

    elif is_vehicle_parked(vacancies, plate):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {'message': f'Vehicle {plate} is already parked'}


@app.put("/pay/{plate}", status_code=200)
def pay_vehicle(plate: str, response: Response):
    global vacancies
    vehicle = is_vehicle_parked(vacancies, plate)
    if is_plate_valid(plate) and vehicle:
        if vehicle['is_paid']:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'message': f'Vehicle {plate} parking is already paid'}
        else:
            vehicle['is_paid'] = True
            history.append(vehicle)
            return {'message': f'Vehicle {plate} parking is now paid'}
    elif not is_plate_valid(plate):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {'message': f'Vehicle {plate} does not have a valid plate'}
    elif not vehicle:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {'message': f'Vehicle {plate} is not parked'}


@app.put("/out/{plate}", status_code=200)
def out_vehicle(plate: str, response: Response):
    global vacancies
    global history
    vehicle = is_vehicle_parked(vacancies, plate)
    if is_plate_valid(plate) and vehicle:
        if not vehicle['is_paid']:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'message': f'Vehicle {plate} parking is not paid yet'}
        vehicle['time_leaving'] = datetime.now()
        history.append(vehicle)
        vacancies = list(filter(lambda i: i['plate'] != plate, vacancies))
        return {'message': f'Vehicle {plate} can pass'}
    elif not is_plate_valid(plate):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {'message': f'Vehicle {plate} does not have a valid plate'}
    elif not vehicle:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {'message': f'Vehicle {plate} is not parked'}
