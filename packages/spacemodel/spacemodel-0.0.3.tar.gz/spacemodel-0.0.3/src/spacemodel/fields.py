from typing import Annotated
from pydantic import (
    AfterValidator,
    PlainSerializer,
    WithJsonSchema,
)

import datetime


LargeInt = Annotated[int,
    AfterValidator(lambda x: x),
    PlainSerializer(lambda x: str(x), return_type=str, when_used='unless-none'),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]


LargeFloat = Annotated[float,
    AfterValidator(lambda x: x),
    PlainSerializer(lambda x: str(x), return_type=str, when_used='unless-none'),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]


UtcTimestamp = Annotated[
    datetime.datetime,
    AfterValidator(lambda x: x),
    PlainSerializer(lambda x: str(x.timestamp()), return_type=str, when_used='unless-none'),
    WithJsonSchema({'type': 'integer'}, mode='serialization'),
]
