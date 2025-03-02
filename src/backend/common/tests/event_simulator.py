import copy
import datetime
import json
from collections import defaultdict

from google.appengine.ext import ndb
from pyre_extensions import none_throws

from backend.common.consts.alliance_color import ALLIANCE_COLORS, AllianceColor
from backend.common.consts.comp_level import CompLevel
from backend.common.helpers.match_helper import MatchHelper
from backend.common.manipulators.event_details_manipulator import (
    EventDetailsManipulator,
)
from backend.common.manipulators.match_manipulator import MatchManipulator
from backend.common.models.event import Event
from backend.common.models.event_details import EventDetails
from backend.common.models.match import Match
from backend.common.tests.fixture_loader import load_fixture


class EventSimulator:
    """
    Steps through an event in time. At step = 0, only the Event exists:
    (step 0) Add all unplayed qual matches
    (step 1, substep n) Add results of each of the n qual matches +
        rankings being updated (if has_event_details)
    (step 2) Add alliance selections (if has_event_details)
    (step 3) Add unplayed QF matches
    (step 4, substep n) Add results of each of the n QF matches +
        update SF matches with advancing alliances (if not batch_advance) +
        update alliance selection backups (if has_event_details)
    (step 5) Add unplayed SF matches (if batch_advance)
    (step 6, substep n) Add results of each of the n SF matches +
        update F matches with advancing alliances (if not batch_advance) +
        update alliance selection backups (if has_event_details)
    (step 7) Add unplayed F matches (if batch_advance)
    (step 8, substep n) Add results of each of the n F matches +
        update alliance selection backups (if has_event_details)
    """

    def __init__(self, has_event_details=True, batch_advance=False):
        self._step = 0
        self._substep = 0
        # whether to update rankings and alliance selections
        self._has_event_details = has_event_details
        # whether to update next playoff level all at once, or as winners are determined
        self._batch_advance = batch_advance

        # Load and save complete data
        load_fixture(
            "test_data/fixtures/2016nytr_event_team_status.json",
            kind={"EventDetails": EventDetails, "Event": Event, "Match": Match},
            post_processor=self._event_key_adder,
        )
        event = Event.get_by_id("2016nytr")

        # Add 3rd matches that never got played
        unplayed_matches = [
            Match(
                id="2016nytr_qf1m3",
                year=2016,
                event=event.key,
                comp_level="qf",
                set_number=1,
                match_number=3,
                alliances_json=json.dumps(
                    {
                        "red": {
                            "teams": ["frc3990", "frc359", "frc4508"],
                            "score": -1,
                        },
                        "blue": {
                            "teams": ["frc3044", "frc4930", "frc4481"],
                            "score": -1,
                        },
                    }
                ),
                time=datetime.datetime(2016, 3, 19, 18, 34),
            ),
            Match(
                id="2016nytr_qf3m3",
                year=2016,
                event=event.key,
                comp_level="qf",
                set_number=3,
                match_number=3,
                alliances_json=json.dumps(
                    {
                        "red": {
                            "teams": ["frc20", "frc5254", "frc229"],
                            "score": -1,
                        },
                        "blue": {
                            "teams": ["frc3003", "frc358", "frc527"],
                            "score": -1,
                        },
                    }
                ),
                time=datetime.datetime(2016, 3, 19, 18, 48),
            ),
            Match(
                id="2016nytr_sf1m3",
                year=2016,
                event=event.key,
                comp_level="sf",
                set_number=1,
                match_number=3,
                alliances_json=json.dumps(
                    {
                        "red": {
                            "teams": ["frc3990", "frc359", "frc4508"],
                            "score": -1,
                        },
                        "blue": {
                            "teams": ["frc5240", "frc3419", "frc663"],
                            "score": -1,
                        },
                    }
                ),
                time=datetime.datetime(2016, 3, 19, 19, 42),
            ),
        ]

        self._event_details = event.details
        self._alliance_selections_without_backup = copy.deepcopy(
            event.details.alliance_selections
        )
        self._alliance_selections_without_backup[1]["backup"] = None
        self._played_matches = MatchHelper.organized_matches(event.matches)[1]
        self._all_matches = MatchHelper.organized_matches(
            event.matches + unplayed_matches
        )[1]

        # Delete data
        event.details.key.delete()
        ndb.delete_multi([match.key for match in event.matches])
        ndb.get_context().clear_cache()

        # Used to keep track of non-batch advancement
        self._advancement_alliances = defaultdict(dict)

    def _event_key_adder(self, obj):
        obj.event = ndb.Key(Event, "2016nytr")

    def _update_rankings(self) -> None:
        """
        Generates and saves fake rankings
        """
        event = none_throws(Event.get_by_id("2016nytr"))

        team_wins = defaultdict(int)
        team_losses = defaultdict(int)
        team_ties = defaultdict(int)
        teams = set()
        for match in event.matches:
            if match.comp_level == CompLevel.QM:
                for alliance in ALLIANCE_COLORS:
                    for team in match.alliances[alliance]["teams"]:
                        teams.add(team)
                        if match.has_been_played:
                            if alliance == match.winning_alliance:
                                team_wins[team] += 1
                            elif match.winning_alliance == "":
                                team_ties[team] += 1
                            else:
                                team_losses[team] += 1

        rankings = []
        for team in sorted(teams):
            wins = team_wins[team]
            losses = team_losses[team]
            ties = team_ties[team]
            rankings.append(
                {
                    "team_key": team,
                    "record": {
                        "wins": wins,
                        "losses": losses,
                        "ties": ties,
                    },
                    "matches_played": wins + losses + ties,
                    "dq": 0,
                    "sort_orders": [2 * wins + ties, 0, 0, 0, 0],
                    "qual_average": None,
                }
            )
        rankings = sorted(rankings, key=lambda r: -r["sort_orders"][0])

        for i, ranking in enumerate(rankings):
            ranking["rank"] = i + 1

        EventDetailsManipulator.createOrUpdate(
            EventDetails(
                id="2016nytr",
                rankings2=rankings,
            )
        )

    def step(self) -> None:
        if self._step == 0:  # Qual match schedule added
            for match in copy.deepcopy(self._all_matches[CompLevel.QM]):
                for alliance in ALLIANCE_COLORS:
                    match.alliances[alliance]["score"] = -1
                match.alliances_json = json.dumps(match.alliances)
                match.score_breakdown_json = None
                match.actual_time = None
                MatchManipulator.createOrUpdate(match)

            self._step += 1
        elif self._step == 1:  # After each qual match
            MatchManipulator.createOrUpdate(
                self._played_matches[CompLevel.QM][self._substep]
            )
            if self._substep < len(self._played_matches[CompLevel.QM]) - 1:
                self._substep += 1
            else:
                self._step += 1
                self._substep = 0
            EventDetailsManipulator.createOrUpdate(EventDetails(id="2016nytr"))
        elif self._step == 2:  # After alliance selections
            EventDetailsManipulator.createOrUpdate(
                EventDetails(
                    id="2016nytr",
                    alliance_selections=self._alliance_selections_without_backup,
                )
            )
            ndb.get_context().flush()
            ndb.get_context().clear_cache()

            self._step += 1
        elif self._step == 3:  # QF schedule added
            for match in copy.deepcopy(self._all_matches[CompLevel.QF]):
                for alliance in ALLIANCE_COLORS:
                    match.alliances[alliance]["score"] = -1
                match.alliances_json = json.dumps(match.alliances)
                match.score_breakdown_json = None
                match.actual_time = None
                MatchManipulator.createOrUpdate(match)
            self._step += 1
        elif self._step == 4:  # After each QF match
            new_match = MatchHelper.play_order_sorted_matches(
                self._played_matches[CompLevel.QF]
            )[self._substep]
            MatchManipulator.createOrUpdate(new_match)

            if not self._batch_advance:
                win_counts = {
                    AllianceColor.RED: 0,
                    AllianceColor.BLUE: 0,
                }
                for i in range(new_match.match_number):
                    win_counts[
                        none_throws(  # pyre-ignore[6]
                            Match.get_by_id(
                                Match.render_key_name(
                                    none_throws(new_match.event.string_id()),
                                    new_match.comp_level,
                                    new_match.set_number,
                                    i + 1,
                                )
                            )
                        ).winning_alliance
                    ] += 1
                for alliance, wins in win_counts.items():
                    if wins == 2:
                        s = new_match.set_number
                        if s in {1, 2}:
                            self._advancement_alliances["sf1"][
                                AllianceColor.RED if s == 1 else AllianceColor.BLUE
                            ] = new_match.alliances[alliance]["teams"]
                        elif s in {3, 4}:
                            self._advancement_alliances["sf2"][
                                AllianceColor.RED if s == 3 else AllianceColor.BLUE
                            ] = new_match.alliances[alliance]["teams"]
                        else:
                            raise Exception("Invalid set number: {}".format(s))

                        for match_set, alliances in self._advancement_alliances.items():
                            if match_set.startswith("sf"):
                                for i in range(3):
                                    for match in copy.deepcopy(
                                        self._all_matches[CompLevel.SF]
                                    ):
                                        key = "2016nytr_{}m{}".format(match_set, i + 1)
                                        if match.key.id() == key:
                                            for color in ALLIANCE_COLORS:
                                                match.alliances[color]["score"] = -1
                                                match.alliances[color][
                                                    "teams"
                                                ] = alliances.get(color, [])
                                            match.alliances_json = json.dumps(
                                                match.alliances
                                            )
                                            match.score_breakdown_json = None
                                            match.actual_time = None
                                            MatchManipulator.createOrUpdate(match)

            if self._substep < len(self._played_matches[CompLevel.QF]) - 1:
                self._substep += 1
            else:
                self._step += 1 if self._batch_advance else 2
                self._substep = 0
        elif self._step == 5:  # SF schedule added
            if self._batch_advance:
                for match in copy.deepcopy(self._all_matches[CompLevel.SF]):
                    for alliance in ALLIANCE_COLORS:
                        match.alliances[alliance]["score"] = -1
                    match.alliances_json = json.dumps(match.alliances)
                    match.score_breakdown_json = None
                    match.actual_time = None
                    MatchManipulator.createOrUpdate(match)
                self._step += 1
        elif self._step == 6:  # After each SF match
            new_match = MatchHelper.play_order_sorted_matches(
                self._played_matches[CompLevel.SF]
            )[self._substep]
            MatchManipulator.createOrUpdate(new_match)

            if not self._batch_advance:
                win_counts = {
                    AllianceColor.RED: 0,
                    AllianceColor.BLUE: 0,
                }
                for i in range(new_match.match_number):
                    win_counts[
                        none_throws(  # pyre-ignore[6]
                            Match.get_by_id(
                                Match.render_key_name(
                                    none_throws(new_match.event.string_id()),
                                    new_match.comp_level,
                                    new_match.set_number,
                                    i + 1,
                                )
                            )
                        ).winning_alliance
                    ] += 1
                for alliance, wins in win_counts.items():
                    if wins == 2:
                        self._advancement_alliances["f1"][
                            AllianceColor.RED
                            if new_match.set_number == 1
                            else AllianceColor.BLUE
                        ] = new_match.alliances[alliance]["teams"]

                        for match_set, alliances in self._advancement_alliances.items():
                            if match_set.startswith("f"):
                                for i in range(3):
                                    for match in copy.deepcopy(
                                        self._all_matches[CompLevel.F]
                                    ):
                                        key = "2016nytr_{}m{}".format(match_set, i + 1)
                                        if match.key.id() == key:
                                            for color in ALLIANCE_COLORS:
                                                match.alliances[color]["score"] = -1
                                                match.alliances[color][
                                                    "teams"
                                                ] = alliances.get(color, [])
                                            match.alliances_json = json.dumps(
                                                match.alliances
                                            )
                                            match.score_breakdown_json = None
                                            match.actual_time = None
                                            MatchManipulator.createOrUpdate(match)

            # Backup robot introduced
            if self._substep == 3:
                EventDetailsManipulator.createOrUpdate(
                    EventDetails(
                        id="2016nytr",
                        alliance_selections=self._event_details.alliance_selections,
                    )
                )
            if self._substep < len(self._played_matches[CompLevel.SF]) - 1:
                self._substep += 1
            else:
                self._step += 1 if self._batch_advance else 2
                self._substep = 0
        elif self._step == 7:  # F schedule added
            if self._batch_advance:
                for match in copy.deepcopy(self._all_matches[CompLevel.F]):
                    for alliance in ALLIANCE_COLORS:
                        match.alliances[alliance]["score"] = -1
                    match.alliances_json = json.dumps(match.alliances)
                    match.score_breakdown_json = None
                    match.actual_time = None
                    MatchManipulator.createOrUpdate(match)
                self._step += 1
        elif self._step == 8:  # After each F match
            MatchManipulator.createOrUpdate(
                MatchHelper.play_order_sorted_matches(
                    self._played_matches[CompLevel.F]
                )[self._substep]
            )
            if self._substep < len(self._played_matches[CompLevel.F]) - 1:
                self._substep += 1
            else:
                self._step += 1
                self._substep = 0

        ndb.get_context().clear_cache()
        # Re fetch event matches
        # event = Event.get_by_id("2016nytr")
        # MatchHelper.delete_invalid_matches(event.matches, event)
        # ndb.get_context().clear_cache()
        self._update_rankings()
