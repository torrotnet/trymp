__all__ = [
    'Sector', 'Industry', 'Purpose', 'Scope', 'ValueConclusion', 'Unit', 'LevelOfValue', 'PerShareValueOrValuation',
    'ValuationApproach', 'ValuationApproachDetailedIncomeApproach', 'ValuationApproachDetailedMarketApproach',
    'PurposeOfAnalysis', 'RoundingConventionNumber', 'RoundingConventionPercentage',
    'AttributesDiscountRate', 'AttributesMinorityOrControlling', 'EngagementConfig', 'ThirdPartyData',
]


class BaseRepo:

    code = None
    label = None
    cType = None
    dType = None
    collection = "Metadata"

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def to_dict(self):
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def _mock_standard_params(self):
        params = {
            "code": self.code,
            "label": self.label,
            "cType": self.cType,
            "dType": self.dType,
        }
        return params

    async def save_to_db(self, db):
        collection = db[self.collection]
        data = self.to_dict()
        data.update(self._mock_standard_params())
        result = await collection.insert_one(data)
        return str(result.inserted_id)


class TestConfig(BaseRepo):
    cType = 'TestConfig'


class Test(TestConfig):
    dType = "Test"


# class ThirdPartyData(BaseRepo):
#     cType = "ThirdPartyData"
#     collection = "ThirdPartyData"
