#
# Copyright 2015 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import numpy as np
from numpy import isnan
from decimal import Decimal
import math


# Fuzzy symbol delimiters that may break up a company symbol and share class
_delimited_symbol_delimiters_regex = re.compile(r'[./\-_]')
_delimited_symbol_default_triggers = frozenset({np.nan, None, ''})


def split_delimited_symbol(symbol):
    """
    Takes in a symbol that may be delimited and splits it in to a company
    symbol and share class symbol. Also returns the fuzzy symbol, which is the
    symbol without any fuzzy characters at all.

    Parameters
    ----------
    symbol : str
        The possibly-delimited symbol to be split

    Returns
    -------
    company_symbol : str
        The company part of the symbol.
    share_class_symbol : str
        The share class part of a symbol.
    """
    # return blank strings for any bad fuzzy symbols, like NaN or None
    if symbol in _delimited_symbol_default_triggers:
        return '', ''

    symbol = symbol.upper()

    split_list = re.split(
        pattern=_delimited_symbol_delimiters_regex,
        string=symbol,
        maxsplit=1,
    )

    # Break the list up in to its two components, the company symbol and the
    # share class symbol
    company_symbol = split_list[0]
    if len(split_list) > 1:
        share_class_symbol = split_list[1]
    else:
        share_class_symbol = ''

    return company_symbol, share_class_symbol


def tolerant_equals(a, b, atol=10e-7, rtol=10e-7, equal_nan=False):
    """Check if a and b are equal with some tolerance.

    Parameters
    ----------
    a, b : float
        The floats to check for equality.
    atol : float, optional
        The absolute tolerance.
    rtol : float, optional
        The relative tolerance.
    equal_nan : bool, optional
        Should NaN compare equal?

    See Also
    --------
    numpy.isclose

    Notes
    -----
    This function is just a scalar version of numpy.isclose for performance.
    See the docstring of ``isclose`` for more information about ``atol`` and
    ``rtol``.
    """
    if equal_nan and isnan(a) and isnan(b):
        return True
    return math.fabs(a - b) <= (atol + rtol * math.fabs(b))


def round_if_near_integer(a, epsilon=1e-4):
    """
    Round a to the nearest integer if that integer is within an epsilon
    of a.
    """
    if abs(a - round(a)) <= epsilon:
        return round(a)
    else:
        return a
