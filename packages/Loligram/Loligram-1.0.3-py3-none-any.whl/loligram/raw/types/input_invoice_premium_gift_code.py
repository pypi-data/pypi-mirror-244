#  Loligram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2023-present Loli <https://github.com/delivrance>
#
#  This file is part of Loligram.
#
#  Loligram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Loligram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Loligram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from loligram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from loligram.raw.core import TLObject
from loligram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class InputInvoicePremiumGiftCode(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~loligram.raw.base.InputInvoice`.

    Details:
        - Layer: ``167``
        - ID: ``98986C0D``

    Parameters:
        purpose (:obj:`InputStorePaymentPurpose <loligram.raw.base.InputStorePaymentPurpose>`):
            N/A

        option (:obj:`PremiumGiftCodeOption <loligram.raw.base.PremiumGiftCodeOption>`):
            N/A

    """

    __slots__: List[str] = ["purpose", "option"]

    ID = 0x98986c0d
    QUALNAME = "types.InputInvoicePremiumGiftCode"

    def __init__(self, *, purpose: "raw.base.InputStorePaymentPurpose", option: "raw.base.PremiumGiftCodeOption") -> None:
        self.purpose = purpose  # InputStorePaymentPurpose
        self.option = option  # PremiumGiftCodeOption

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputInvoicePremiumGiftCode":
        # No flags
        
        purpose = TLObject.read(b)
        
        option = TLObject.read(b)
        
        return InputInvoicePremiumGiftCode(purpose=purpose, option=option)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.purpose.write())
        
        b.write(self.option.write())
        
        return b.getvalue()
