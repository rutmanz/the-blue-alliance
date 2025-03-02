import calendar
import logging
from typing import Any, cast, Dict, Optional

from pyre_extensions import none_throws

from backend.common.consts.notification_type import NotificationType
from backend.common.models.event import Event
from backend.common.models.match import Match
from backend.common.models.notifications.notification import Notification


class EventScheduleNotification(Notification):
    def __init__(self, event: Event, next_match: Optional[Match] = None) -> None:
        self.event = event

        if not next_match:
            from backend.common.helpers.match_helper import MatchHelper

            upcoming = MatchHelper.upcoming_matches(event.matches, 1)
            self.next_match = upcoming[0] if upcoming and len(upcoming) > 0 else None
        else:
            self.next_match = next_match

    @classmethod
    def _type(cls) -> NotificationType:
        return NotificationType.SCHEDULE_UPDATED

    @property
    def fcm_notification(self) -> Optional[Any]:
        body = f"The {self.event.normalized_name} match schedule has been updated."
        if self.next_match and self.next_match.time:
            time = self.next_match.time.strftime("%H:%M")
            # Add timezone, if possible
            if self.event.timezone_id:
                try:
                    import pytz

                    timezone = pytz.timezone(self.event.timezone_id)
                    time += timezone.localize(self.next_match.time).strftime(" %Z")
                except Exception as e:
                    logging.warning(
                        f"Unable to add timezone to match schedule notification: {e}"
                    )

            body += f" The next match starts at {time}."

        from firebase_admin import messaging

        return messaging.Notification(
            title="{} Schedule Updated".format(self.event.event_short.upper()),
            body=body,
        )

    @property
    def data_payload(self) -> Optional[Dict[str, str]]:
        return {"event_key": self.event.key_name}

    @property
    def webhook_message_data(self) -> Optional[Dict[str, Any]]:
        payload = cast(Dict[str, Any], none_throws(self.data_payload))
        if self.next_match and self.next_match.time:
            payload["first_match_time"] = calendar.timegm(
                self.next_match.time.utctimetuple()
            )
        payload["event_name"] = self.event.name
        return payload
