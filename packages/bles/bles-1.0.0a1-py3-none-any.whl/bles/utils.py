# bles --- Event Sourcing library
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import json
from datetime import datetime, timezone

from bles import Event


def event_to_string(event: Event) -> str:
    return json.dumps(
        {
            "stream_id": event.stream_id,
            "version": event.version,
            "name": event.name,
            "data": event.data,
            "position": event.position if event.position else None,
            "recorded_at": (
                event.recorded_at.isoformat() if event.recorded_at else None
            ),
        }
    )


def event_from_string(string: str) -> Event:
    data = json.loads(string)
    if recorded_at := data.get("recorded_at", ""):
        data["recorded_at"] = datetime.fromisoformat(recorded_at)
        data["recorded_at"] = data["recorded_at"].replace(tzinfo=timezone.utc)

    return Event(
        stream_id=data["stream_id"],
        version=data["version"],
        name=data["name"],
        data=data["data"],
        position=data["position"],
        recorded_at=data["recorded_at"],
    )
