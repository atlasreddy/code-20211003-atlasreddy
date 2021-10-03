import json
import os

from bmi.log_module import LogModule
from bmi.config import Configuration as conf


logger = LogModule.get_logger(__name__)

INF = float("inf")
MIN_HEIGHT_CM = 40
MAX_HEIGHT_CM = 300
MIN_WEIGHT_KG = 20
MAX_WEIGHT_KG = 200


def load_data(filename):
    if not os.path.exists(filename):
        logger.critical(f"data file not found at {filename}")
        return []
    try:
        with open(filename, "r") as infile:
            logger.info("Loading the data from the data file")
            data = json.loads(infile.read())
        logger.info("Loaded data successfully")
        return data
    except Exception as e:
        logger.error(e, exc_info=True)


def is_numeric(value):
    return str(value).isnumeric()


def isvalid_height(height):
    if is_numeric(height):
        return MIN_HEIGHT_CM <= height <= MAX_HEIGHT_CM
    else:
        logger.error("Height should be numeric value")
        raise False


def isvalid_weight(weight):
    if is_numeric(weight):
        return MIN_WEIGHT_KG <= weight <= MAX_WEIGHT_KG
    else:
        logger.error("Weight should be numeric value")
        raise False


def isvalid_gender(gender):
    assert isinstance(gender, str), "Gender value must be a string either male or female"
    return gender.lower() in ("male", "female")


class BodyMassIndex:
    def __init__(self, **kwargs):
        logger.info(f"Initialised with {kwargs}")
        self.gender = kwargs.get('Gender', None)
        self.heightCm = kwargs.get('HeightCm', None)
        self.weightKg = kwargs.get('WeightKg', None)

        if not (isvalid_gender(self.gender) or
                isvalid_height(self.heightCm) or
                isvalid_weight(self.weightKg)):
            logger.error("No sufficient information provided. ")
            raise Exception("Insufficient information. ")

    #     Other init level attributes
        self.heightM = self.convert_height_cm_to_m()
        self.bmi_value = self.calculate_bmi()
        self.bmi_category = None
        self.health_risk = None

    def convert_height_cm_to_m(self):
        height_meters = self.heightCm / 100
        logger.info("Height converted successfully")
        return height_meters

    def calculate_bmi(self):
        logger.info("Inside calculate BMI ")
        try:
            float(self.heightM)
            float(self.weightKg)
            logger.debug("Proceeding to calculate bmi value")
        except TypeError:
            logger.error("Only accepted data types for height or weight is "
                         "float or int. ", exc_info=True)
        else:
            try:
                value = float(f"{self.weightKg / (self.heightM ** 2):.1}")
                logger.info("BMI value is calculated. ")
                return value
            except ZeroDivisionError as z:
                logger.error("height should not zero. ", exc_info=True)

    @staticmethod
    def check_in_range(low_number, number, high_number=INF, inclusive=True):
        if inclusive:
            return low_number <= number <= high_number
        else:
            return low_number < number < high_number

    def set_bmi_category_risks(self):
        if not isinstance(self.bmi_value, float):
            self.bmi_category = None
            self.health_risk = None
            logger.error("bmi_value must be of float data type")
            raise TypeError("bmi_value should be float datatype")
        number = self.bmi_value
        logger.info(f"bmi_value : {number}")
        try:
            logger.info("Setting the bmi_category and health_risk")
            if self.check_in_range(0, number, 18.4):
                self.bmi_category = "UnderWeight"
                self.health_risk = "Malnutrition"
            elif self.check_in_range(18.5, number, 24.9):
                self.bmi_category = "NormalWeight"
                self.health_risk = "LowRisk"
            elif self.check_in_range(25, number, 29.9):
                self.bmi_category = "OverWeight"
                self.health_risk = "EnhancedRisk"
            elif self.check_in_range(30, number, 34.9):
                self.bmi_category = "ModeratelyObese"
                self.health_risk = "MediumRisk"
            elif self.check_in_range(35, number, 39.9):
                self.bmi_category = "SeverelyObese"
                self.health_risk = "HighRisk"
            elif self.check_in_range(40, number, INF):
                self.bmi_category = "VerySeverelyObese"
                self.health_risk = "VeryHighRisk"
            else:
                self.bmi_category = "NOTA"
                self.health_risk = "NOTA"

            logger.info("Completed setting up the bmi_category and health risk values")

        except Exception as e:
            logger.exception(f"Exception occurred {e}")

    def serialize(self):
        logger.info("Serializing to key-value pairs for data")
        return {
            "Gender": self.gender,
            "HeightCm": self.heightCm,
            "WeightKg": self.weightKg,
            "bmi_value": self.bmi_value,
            "Category": self.bmi_category,
            "HealthRisk": self.health_risk,
        }


class BodyMassIndexSetUp:

    def __init__(self, data_file):
        self.data = load_data(data_file)
        logger.debug(self.data)
        self.over_weight_count = 0

    def execute(self):
        for data in self.data:
            try:
                bmi = BodyMassIndex(**data)
                bmi.set_bmi_category_risks()
                # print(bmi.serialize())
                logger.info(bmi.serialize())
                if bmi.serialize().get("Category", "") == "OverWeight":
                    self.over_weight_count += 1
            except Exception as e:
                logger.warning(f"Could not proceed with the data {data} -- {e}", exc_info=True)


def main():
    bmi = BodyMassIndexSetUp(conf.DATA_FILE)
    bmi.execute()
    logger.critical(bmi.over_weight_count)


def get_data():
    import random
    genders = ("Male", "Female")

    gender = genders[random.randint(0, 1)]

    height = random.randrange(MIN_HEIGHT_CM, MAX_HEIGHT_CM)
    weight = random.randrange(MIN_WEIGHT_KG, MAX_WEIGHT_KG)

    d = {"Gender": gender,
         "HeightCm": height,
         "WeightKg": weight
         }
    return d


def generate_data(count):
    data = []
    for _ in range(count):
        data.append(get_data())
    with open(conf.DATA_FILE, "w") as f:
        json.dump(data, f)
    return data
