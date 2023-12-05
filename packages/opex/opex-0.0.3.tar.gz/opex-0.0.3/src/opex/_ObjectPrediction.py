from typing import Dict

from wai.json.object import OptionallyPresent, StrictJSONObject
from wai.json.object.property import StringProperty, NumberProperty, MapProperty

from ._BBox import BBox
from ._Polygon import Polygon


class ObjectPrediction(StrictJSONObject['ObjectPrediction']):
    """
    A single object prediction.
    """
    # The score given to the prediction
    score: OptionallyPresent[float] = NumberProperty(minimum=0.0, optional=True)

    # The predicted label of the object
    label: str = StringProperty(min_length=1)

    # The bounding box around the prediction
    bbox: BBox = BBox.as_property()

    # The polygon around the prediction
    polygon: Polygon = Polygon.as_property()

    # Any meta-data
    meta: OptionallyPresent[Dict[str, str]] = MapProperty(
        value_property=StringProperty(),
        optional=True
    )

    def __str__(self):
        """
        Returns a short string representation of itself.

        :return: the string representation
        :rtype: str
        """
        return "score=%s, label=%s" % (str(self.score), self.label)
