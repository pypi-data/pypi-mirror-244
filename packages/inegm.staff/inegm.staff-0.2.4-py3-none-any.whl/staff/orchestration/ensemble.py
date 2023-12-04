from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import List, Union

from staff import MIDIPitch
from staff.orchestration.instrument import Instrument
from staff.orchestration.voicing import VoicedChord, voice_pitches


@total_ordering
class SATBRole(Enum):
    SOPRANO = "soprano"
    ALTO = "alto"
    TENOR = "tenor"
    BASS = "bass"

    def _order(self) -> List[SATBRole]:
        return [
            SATBRole.BASS,
            SATBRole.TENOR,
            SATBRole.ALTO,
            SATBRole.SOPRANO,
        ]

    def __lt__(self, other: SATBRole) -> bool:
        return self._order().index(self) < self._order().index(other)


@total_ordering
@dataclass(frozen=True)
class SATBEnsembleInstrument:
    """An instrument in an SATB ensemble."""

    instrument: Instrument
    role: SATBRole

    def __lt__(self, other: SATBEnsembleInstrument) -> bool:
        """Return whether or not the instrument is lower than another.

        Compares the roles first, then the bottom of the ranges, then the top of
        the ranges.

        Args:
            other: The other instrument to compare to.

        Returns:
            True if the instrument is lower than the other, False otherwise.
        """
        if self.role == other.role:
            if self.instrument.range.bottom == other.instrument.range.bottom:
                return (
                    self.instrument.range.top.number
                    - self.instrument.range.bottom.number
                ) < (
                    other.instrument.range.top.number
                    - other.instrument.range.bottom.number
                )
            return self.instrument.range.bottom < other.instrument.range.bottom
        return self.role < other.role


@dataclass
class SATBEnsemble:
    """An SATB (sopreano, alto, tenor, bass) ensemble.

    Note:
        This class can be stored and retrieved from a database.
        See the documentation for the `staff.db` module for more information.
    """

    name: str
    instruments: List[SATBEnsembleInstrument]
    description: str = ""
    category: str = "Default"

    def __post_init__(self) -> None:
        self.instruments.sort()

    def add_instrument(
        self,
        instrument: Instrument,
        role: str,
    ) -> SATBEnsemble:
        """Add an instrument to the ensemble."""
        role = role.lower()
        try:
            SATBRole(role)
        except ValueError:
            raise ValueError(
                f"Invalid role: '{role}'. "
                f"Valid roles include: {[role.value for role in SATBRole]}."
            )
        instruments = self.instruments
        instruments.append(SATBEnsembleInstrument(instrument, SATBRole(role)))
        return SATBEnsemble(
            name=self.name,
            instruments=instruments,
            description=self.description,
            category=self.category,
        )


@dataclass
class Ensemble:
    name: str
    instruments: List[Instrument]
    description: str = ""
    category: str = "Default"

    def __post_init__(self) -> None:
        self.instruments = sorted(self.instruments)

    def add_instrument(self, instrument: Instrument) -> Ensemble:
        """Add an instrument to the ensemble."""
        instruments = self.instruments
        instruments.append(instrument)
        return Ensemble(
            name=self.name,
            instruments=instruments,
            description=self.description,
            category=self.category,
        )

    def voice(
        self,
        pitches: List[MIDIPitch],
        openness: float = 0.5,
    ) -> Union[VoicedChord, None]:
        if (openness > 1.0) or (openness < 0.0):
            raise ValueError("spread must be between 0 and 1")
        return voice_pitches(
            pitches=pitches, instruments=self.instruments, spread=openness
        )

    def voice_lead(
        self,
        start: VoicedChord,
        end: List[MIDIPitch],
    ) -> Union[VoicedChord, None]:
        pass
