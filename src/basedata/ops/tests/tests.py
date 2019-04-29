"""
Unittests for base.data.ops submodule __init__.py code
"""
from unittest import TestCase

import pandas as pd

from .. import BaseDataOps
from .test_databuild import make_dirty_numeric_dataframe


keycol = 'test'


class BaseDataOpsTests(TestCase):
    """unittests for base.BaseDataOps class"""

    def test_BaseDataOps_invoke(self):
        """ensure BaseDataOps.from_object invokes __init__ of parent class"""
        df_test = make_dirty_numeric_dataframe(keycol)
        df_read = BaseDataOps.from_object(df_test).df
        self.assertEqual(
            pd.testing.assert_frame_equal(df_test, df_read),
            None,
        )
