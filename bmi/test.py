import pytest

from bmi.bmi import isvalid_gender, isvalid_height, isvalid_weight, BodyMassIndex


@pytest.fixture
def sample_data():
    return {'Gender': 'Male',
            'HeightCm': 152, 'WeightKg': 55,
            }


@pytest.fixture
def result_data():
    return {'bmi_value': 20.0, 'Category': 'NormalWeight',
            'HealthRisk': 'LowRisk'}


def test_valid_gender(sample_data):
    isvalid_gender(sample_data["Gender"])


def test_valid_height(sample_data):
    isvalid_height(sample_data["HeightCm"])


def test_valid_weight(sample_data):
    isvalid_weight(sample_data["WeightKg"])


def test_verify_bmi(sample_data, result_data):
    assert BodyMassIndex(**sample_data).serialize()["bmi_value"] == result_data["bmi_value"]
