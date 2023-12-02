"""
Custom data cleaning / preprocessing module for Titanic model

Data columns
key: string
fare_amount: double
pickup_datetime: string
pickup_longitude: double
pickup_latitude: double
dropoff_longitude: double
dropoff_latitude: double
passenger_count: bigint
"""
from typing import List, TYPE_CHECKING

from pyspark.sql import functions as f
from pyspark.sql.types import TimestampType, IntegerType

from nyc_taxi_fare_model.custom_type import NormalizedCoefficients


if TYPE_CHECKING:
    from pyspark.pandas import DataFrame
    from pyspark.sql.dataframe import DataFrame as PySparkDataframe


NORMALIZED_COEF: NormalizedCoefficients = {
    'mean_pickup_longitude': -73.97323721516585,
    'stddev_pickup_longitude': 0.03913489891634451,
    'mean_dropoff_longitude': -73.96882655847182,
    'stddev_dropoff_longitude': 0.036722876699459284,
    'mean_pickup_latitude': 40.752567257364056,
    'stddev_pickup_latitude': 0.029971074292229977,
    'mean_dropoff_latitude': 40.75523957204929,
    'stddev_dropoff_latitude': 0.03242140520466382
}


def set_mormalized_coef(df):
    mean_pickup_longitude = df.select(f.mean(f.col('pickup_longitude'))).first()[0]
    stddev_pickup_longitude = df.select(f.stddev(f.col('pickup_longitude'))).first()[0]
    mean_dropoff_longitude = df.select(f.mean(f.col('dropoff_longitude'))).first()[0]
    stddev_dropoff_longitude = df.select(f.stddev(f.col('dropoff_longitude'))).first()[0]
    mean_pickup_latitude = df.select(f.mean(f.col('pickup_latitude'))).first()[0]
    stddev_pickup_latitude = df.select(f.stddev(f.col('pickup_latitude'))).first()[0]
    mean_dropoff_latitude = df.select(f.mean(f.col('dropoff_latitude'))).first()[0]
    stddev_dropoff_latitude = df.select(f.stddev(f.col('dropoff_latitude'))).first()[0]

    print(
        f'mean_pickup_longitude={mean_pickup_longitude}, stddev_pickup_longitude={stddev_pickup_longitude},'
        f' mean_dropoff_longitude={mean_dropoff_longitude}, stddev_dropoff_longitude={stddev_dropoff_longitude},'
        f' mean_pickup_latitude={mean_pickup_latitude}, stddev_pickup_latitude={stddev_pickup_latitude}, '
        f'mean_dropoff_latitude={mean_dropoff_latitude}, stddev_dropoff_latitude={stddev_dropoff_latitude}'
    )
    NORMALIZED_COEF['mean_pickup_longitude'] = mean_pickup_longitude
    NORMALIZED_COEF['stddev_pickup_longitude'] = stddev_pickup_longitude
    NORMALIZED_COEF['mean_dropoff_longitude'] = mean_dropoff_longitude
    NORMALIZED_COEF['stddev_dropoff_longitude'] = stddev_dropoff_longitude
    NORMALIZED_COEF['mean_pickup_latitude'] = mean_pickup_latitude
    NORMALIZED_COEF['stddev_pickup_latitude'] = stddev_pickup_latitude
    NORMALIZED_COEF['mean_dropoff_latitude'] = mean_dropoff_latitude
    NORMALIZED_COEF['stddev_dropoff_latitude'] = stddev_dropoff_latitude


def clean_missing_numerics(df: 'PySparkDataframe', numeric_columns):
    mean_values = df.select([f.mean(col_name).alias(col_name) for col_name in numeric_columns]).first().asDict()
    # Fill missing values using df.fillna()
    df = df.fillna(mean_values, subset=numeric_columns)
    return df


def replace_zero_by_mean_numerics(df: 'PySparkDataframe', numeric_columns):
    for col in numeric_columns:
        mean_value = df.select(f.mean(col)).first()[0]
        df = df.withColumn(col, f.when(f.col(col) == 0.0, mean_value).otherwise(f.col(col)))
    return df


def clean_fare(df: 'PySparkDataframe'):
    df = df.filter(df['fare_amount'] > 0.99)
    return df


def extract_features_from_timestamp(df: 'PySparkDataframe', datetime_column: str):
    df_col = f.col(datetime_column)

    df = df.withColumn(datetime_column, f.to_timestamp(df_col, "yyyy-MM-dd HH:mm:ss 'UTC'").cast(TimestampType())) \
        .withColumn(f'{datetime_column}_month', f.month(df_col)) \
        .withColumn(f'{datetime_column}_day', f.dayofmonth(df_col)) \
        .withColumn(f'{datetime_column}_hour', f.hour(df_col)) \
        .withColumn(f'{datetime_column}_minute', f.minute(df_col)) \
        .withColumn(f'{datetime_column}_day_of_week', f.dayofweek(df_col)) \
        .withColumn(f'{datetime_column}_is_weekend', f.dayofmonth(df_col).isin([5, 6]).cast(IntegerType())) \
        .drop(df_col)
    # add is_rush_hour
    return df


def normalize(df):
    mean_pickup_longitude = NORMALIZED_COEF['mean_pickup_longitude']
    stddev_pickup_longitude = NORMALIZED_COEF['stddev_pickup_longitude']
    mean_dropoff_longitude = NORMALIZED_COEF['mean_dropoff_longitude']
    stddev_dropoff_longitude = NORMALIZED_COEF['stddev_dropoff_longitude']
    mean_pickup_latitude = NORMALIZED_COEF['mean_pickup_latitude']
    stddev_pickup_latitude = NORMALIZED_COEF['stddev_pickup_latitude']
    mean_dropoff_latitude = NORMALIZED_COEF['mean_dropoff_latitude']
    stddev_dropoff_latitude = NORMALIZED_COEF['stddev_dropoff_latitude']

    # Normalize and make positive the specified columns
    normalized_df = df.withColumn('pickup_longitude', ((f.col('pickup_longitude') * (-1) - mean_pickup_longitude) / stddev_pickup_longitude))
    normalized_df = normalized_df.withColumn('dropoff_longitude', ((f.col('dropoff_longitude') * (-1) - mean_dropoff_longitude) / stddev_dropoff_longitude))

    normalized_df = normalized_df.withColumn('pickup_latitude', ((f.col('pickup_latitude') - mean_pickup_latitude) / stddev_pickup_latitude))
    normalized_df = normalized_df.withColumn('dropoff_latitude', ((f.col('dropoff_latitude') - mean_dropoff_latitude) / stddev_dropoff_latitude))
    return normalized_df


def get_distance(df):
    return df.withColumn('distance', f.sqrt((f.col('pickup_longitude') - f.col('dropoff_longitude')) ** 2 + (
                f.col('pickup_latitude') - f.col('dropoff_latitude')) ** 2))


def haversine_distance(df):
    """
    Calculating the great circle distance between two points on the earth (specified in decimal degrees)
    :param df:, :type PySparkDataframe
    :return: df: df with added distance column, :type PySparkDataframe
    """
    def haversine(lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = f.radians(lon1), f.radians(lat1), f.radians(lon2), f.radians(lat2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = f.sin(dlat / 2) ** 2 + f.cos(lat1) * f.cos(lat2) * f.sin(dlon / 2) ** 2
        c = 2 * f.asin(f.sqrt(a))
        km = 6367 * c
        return km

    return df.withColumn(
        'distance',
        haversine(
            f.col('pickup_longitude'), f.col('pickup_latitude'),
            f.col('dropoff_longitude'), f.col('dropoff_latitude')
        )
    )


def drop_not_nyc_coordinates(df):
    df = df.where(df['pickup_longitude'] > -75.0)
    df = df.where(df['pickup_longitude'] < -72.0)
    df = df.where(df['pickup_latitude'] > 40.0)
    df = df.where(df['pickup_latitude'] < 42.0)
    df = df.where(df['dropoff_longitude'] > -74.0)
    df = df.where(df['dropoff_longitude'] < -72.0)
    df = df.where(df['dropoff_latitude'] > 40.0)
    df = df.where(df['dropoff_latitude'] < 42.0)

    return df


def process_dataframe(df: 'DataFrame') -> 'DataFrame':
    print("Processing dataframe")
    df = df.drop_duplicates()
    df = clean_fare(df)
    df = drop_not_nyc_coordinates(df)

    numeric_cols: List[str] = df.columns
    numeric_cols.remove('key')
    numeric_cols.remove('pickup_datetime')

    df = clean_missing_numerics(df, numeric_cols)
    df = replace_zero_by_mean_numerics(df, numeric_cols)
    df = extract_features_from_timestamp(df, 'pickup_datetime')
    df = haversine_distance(df)

    return df
