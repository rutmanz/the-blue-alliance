import collections
import datetime
import logging
import re
from typing import Dict, List, Mapping, MutableSequence, Sequence, Tuple

import pytz
from pyre_extensions import none_throws

from backend.common.consts.comp_level import COMP_LEVELS, CompLevel
from backend.common.consts.playoff_type import DoubleElimBracket
from backend.common.helpers.playoff_type_helper import PlayoffTypeHelper
from backend.common.models.event import Event
from backend.common.models.match import Match


TOrganizedMatches = Dict[CompLevel, List[Match]]
TOrganizedDoubleElimMatches = Mapping[
    DoubleElimBracket, Mapping[CompLevel, List[Match]]
]


class MatchHelper(object):

    """
    Helper to put matches into sub-dictionaries for the way we render match tables
    Allows us to sort matches by key name.
    Note: Matches within a comp_level (qual, qf, sf, f, etc.) will be in order,
    but the comp levels themselves may not be in order. Doesn't matter because
    XXX_match_table.html checks for comp_level when rendering the page
    """

    @classmethod
    def natural_sorted_matches(cls, matches: List[Match]) -> List[Match]:
        def convert(text):
            return int(text) if text.isdigit() else text.lower()

        def alphanum_key(match):
            return [convert(c) for c in re.split("([0-9]+)", str(match.key_name))]

        return sorted(matches, key=alphanum_key)

    @classmethod
    def play_order_sorted_matches(
        cls, matches: Sequence[Match], reverse: bool = False
    ) -> List[Match]:
        return sorted(matches, key=lambda m: m.play_order, reverse=reverse)

    @classmethod
    def organized_matches(
        cls, match_list: List[Match]
    ) -> Tuple[int, TOrganizedMatches]:
        match_list = cls.natural_sorted_matches(match_list)
        matches = dict([(comp_level, list()) for comp_level in COMP_LEVELS])
        count = len(match_list)
        while len(match_list) > 0:
            match = match_list.pop(0)
            matches[match.comp_level].append(match)

        return count, matches

    # Assumed that organized_matches is called first
    @classmethod
    def organized_double_elim_matches(
        cls, organized_matches: TOrganizedMatches
    ) -> TOrganizedDoubleElimMatches:
        matches = collections.defaultdict(lambda: collections.defaultdict(list))
        for level in COMP_LEVELS:
            level_matches = organized_matches[level]
            if level == CompLevel.QM:
                continue
            for match in level_matches:
                bracket = PlayoffTypeHelper.get_double_elim_bracket(
                    level, match.set_number
                )
                matches[bracket][level].append(match)
        return matches

    @classmethod
    def recent_matches(cls, matches: List[Match], num: int = 3) -> List[Match]:
        matches = list(filter(lambda x: x.has_been_played, matches))
        matches = cls.play_order_sorted_matches(matches)
        return matches[-num:]

    @classmethod
    def upcoming_matches(cls, matches: List[Match], num: int = 3) -> List[Match]:
        matches = cls.play_order_sorted_matches(matches)

        last_played_match_index = None
        for i, match in enumerate(reversed(matches)):
            if match.has_been_played:
                last_played_match_index = len(matches) - i
                break

        upcoming_matches = []
        for i, match in enumerate(matches[last_played_match_index:]):
            if i == num:
                break
            if not match.has_been_played:
                upcoming_matches.append(match)
        return upcoming_matches

    @classmethod
    def add_match_times(cls, event: Event, matches: MutableSequence[Match]) -> None:
        """
        Calculates and adds match times given an event and match time strings (from USFIRST)
        Assumes the last match is played on the last day of comeptition and
        works backwards from there.
        """
        if (
            event.timezone_id is None
        ):  # Can only calculate match times if event timezone is known
            logging.warning(
                "Cannot compute match time for event with no timezone_id: {}".format(
                    event.key_name
                )
            )
            return

        matches_reversed = cls.play_order_sorted_matches(matches, reverse=True)
        tz = pytz.timezone(event.timezone_id)

        last_match_time = None
        cur_date = event.end_date + datetime.timedelta(
            hours=23, minutes=59, seconds=59
        )  # end_date is specified at midnight of the last day
        for match in matches_reversed:
            r = none_throws(
                re.search(r"(\d+):(\d+) (am|pm)", match.time_string.lower())
            )
            hour = int(r.group(1))
            minute = int(r.group(2))
            if hour == 12:
                hour = 0
            if r.group(3) == "pm":
                hour += 12

            match_time = datetime.datetime(
                cur_date.year, cur_date.month, cur_date.day, hour, minute
            )
            if (
                last_match_time is not None
                and last_match_time + datetime.timedelta(hours=6) < match_time
            ):
                cur_date = cur_date - datetime.timedelta(days=1)
                match_time = datetime.datetime(
                    cur_date.year, cur_date.month, cur_date.day, hour, minute
                )
            last_match_time = match_time

            match.time = match_time - tz.utcoffset(match_time)

    """
    @classmethod
    def delete_invalid_matches(cls, match_list: List[Match], event: Event) -> List[Match]:
        \"""
        A match is invalid iff it is an elim match that has not been played
        and the same alliance already won in 2 match numbers in the same set.
        \"""
        red_win_counts = collections.defaultdict(int)  # key: <comp_level><set_number>
        blue_win_counts = collections.defaultdict(int)  # key: <comp_level><set_number>
        for match in match_list:
            if match.has_been_played and match.comp_level in ELIM_LEVELS:
                key = "{}{}".format(match.comp_level, match.set_number)
                if match.winning_alliance == "red":
                    red_win_counts[key] += 1
                elif match.winning_alliance == "blue":
                    blue_win_counts[key] += 1

        return_list = []
        for match in match_list:
            if match.comp_level in ELIM_LEVELS and not match.has_been_played:
                if (
                    event.playoff_type != PlayoffType.ROUND_ROBIN_6_TEAM
                    or match.comp_level == "f"
                ):  # Don't delete round robin semifinal matches
                    key = "{}{}".format(match.comp_level, match.set_number)
                    n = 3 if event.playoff_type == PlayoffType.BO5_FINALS else 2
                    if red_win_counts[key] == n or blue_win_counts[key] == n:
                        try:
                            MatchManipulator.delete(match)
                            logging.warning("Deleting invalid match: %s" % match.key_name)
                        except Exception:
                            logging.warning(
                                "Tried to delete invalid match, but failed: %s"
                                % match.key_name
                            )
                        continue
            return_list.append(match)

        return return_list
    """
