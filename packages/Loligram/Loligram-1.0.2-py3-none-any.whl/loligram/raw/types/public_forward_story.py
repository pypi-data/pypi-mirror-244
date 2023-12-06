#  Loligram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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


class PublicForwardStory(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~loligram.raw.base.PublicForward`.

    Details:
        - Layer: ``167``
        - ID: ``EDF3ADD0``

    Parameters:
        peer (:obj:`Peer <loligram.raw.base.Peer>`):
            N/A

        story (:obj:`StoryItem <loligram.raw.base.StoryItem>`):
            N/A

    """

    __slots__: List[str] = ["peer", "story"]

    ID = 0xedf3add0
    QUALNAME = "types.PublicForwardStory"

    def __init__(self, *, peer: "raw.base.Peer", story: "raw.base.StoryItem") -> None:
        self.peer = peer  # Peer
        self.story = story  # StoryItem

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PublicForwardStory":
        # No flags
        
        peer = TLObject.read(b)
        
        story = TLObject.read(b)
        
        return PublicForwardStory(peer=peer, story=story)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.story.write())
        
        return b.getvalue()
