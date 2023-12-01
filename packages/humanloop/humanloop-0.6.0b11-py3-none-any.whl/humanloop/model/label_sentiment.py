# coding: utf-8

"""
    Humanloop API

    The Humanloop API allows you to interact with Humanloop from your product or service.  You can do this through HTTP requests from any language or via our official Python or TypeScript SDK.  To install the official [Python SDK](https://pypi.org/project/humanloop/), run the following command:  ```bash pip install humanloop ```  To install the official [TypeScript SDK](https://www.npmjs.com/package/humanloop), run the following command:  ```bash npm i humanloop ```  ---  Guides and further details about key concepts can be found in [our docs](https://docs.humanloop.com/).

    The version of the OpenAPI document: 4.0.1
    Generated by: https://konfigthis.com
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from humanloop import schemas  # noqa: F401


class LabelSentiment(
    schemas.EnumBase,
    schemas.StrSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    How a label should be treated in calculating model config performance.

Used by a project's PAPV metric.
    """


    class MetaOapg:
        enum_value_to_name = {
            "positive": "POSITIVE",
            "negative": "NEGATIVE",
            "neutral": "NEUTRAL",
            "unset": "UNSET",
        }
    
    @schemas.classproperty
    def POSITIVE(cls):
        return cls("positive")
    
    @schemas.classproperty
    def NEGATIVE(cls):
        return cls("negative")
    
    @schemas.classproperty
    def NEUTRAL(cls):
        return cls("neutral")
    
    @schemas.classproperty
    def UNSET(cls):
        return cls("unset")
