class BaseRepository:

    cType = None
    dType = None
    number = None
    entity = None
    value = None    # alphabeticCode
    label = None    # currency
    numeric_code = None
    minor_unit = None

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def to_dict(self):
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def _mock_standard_params(self):
        params = {
            "cType": self.c_type,
            "dType": self.d_type,
            "number": self.number,
            "entity": self.entity,
            "value": self.value,
            "label": self.label,
            "numericCode": self.numeric_code,
            "minorUnit": self.minor_unit
        }
        return params


class EngagementConfig(BaseRepository):
    cType = "EngagementConfig"


class CurrencyData(EngagementConfig):
    dType = "Currency"

    async def save_to_db(self, db, data):
        collection = db.Metadata

        for item in data:
            item.update({"cType": self.cType, "dType": self.dType})

        await collection.insert_many(data)
