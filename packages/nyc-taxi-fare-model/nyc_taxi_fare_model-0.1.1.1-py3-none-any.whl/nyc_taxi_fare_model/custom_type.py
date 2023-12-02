from typing import TypedDict


class NormalizedCoefficients(TypedDict):
    mean_pickup_longitude: float
    stddev_pickup_longitude: float
    mean_dropoff_longitude: float
    stddev_dropoff_longitude: float
    mean_pickup_latitude: float
    stddev_pickup_latitude: float
    mean_dropoff_latitude: float
    stddev_dropoff_latitude: float
