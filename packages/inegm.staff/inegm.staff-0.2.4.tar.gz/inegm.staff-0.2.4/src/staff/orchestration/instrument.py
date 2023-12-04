from __future__ import annotations

from dataclasses import dataclass
from typing import List

from staff import MIDIPitch


@dataclass
class Articulation:
    """An articulation of a musical instrument.

    Note:
        Some articulations change the instrument's range, such as mutes for brass
        or harmonics for strings. These range changes are not yet implemented.

    Args:
        name: The name of the articulation.
        key_switch: The key switch that triggers the articulation.
        abbreviation: The abbreviation of the articulation.
        description: The description of the articulation.
    """

    # TODO Add support for articulations that change the instrument's range.

    name: str
    key_switch: MIDIPitch
    abbreviation: str = ""
    description: str = ""


@dataclass
class InstrumentRange:
    bottom: MIDIPitch
    top: MIDIPitch


@dataclass
class Instrument:
    """A musical instrument.

    Note:
        This class can be stored and retrieved from a database.
        See the documentation for the `staff.db` module for more information.

    Args:
        name: The name of the instrument.
        section: The section the instrument belongs to.
        range: The range of the instrument.
        articulations: The articulations of the instrument.
        is_continuous: Whether or not the instrument is continuous (like a string
            instrument or a trombone).
        abbreviation: The abbreviation of the instrument.
        category: The category the instrument belongs to, which only serves to keep
            instruments organised. An example use would be to group by VST
            plugins.
        description: The description of the instrument.
    """

    # TODO: Add CC numbers for vibrato, expression, etc.

    name: str
    section: str
    range: InstrumentRange
    articulations: List[Articulation]
    is_continuous: bool = False
    abbreviation: str = ""
    category: str = "Default"
    description: str = ""

    def __eq__(self, other) -> bool:
        return (self.name == other.name) and (self.category == other.category)

    def __gt__(self, other) -> bool:
        """Greater, here, signifies being a conventionally higher voice."""
        if self.range.bottom > other.range.bottom:
            return True
        elif self.range.top > other.range.top:
            return True
        elif self.range == other.range:
            return self.name < other.name
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.name + self.category)

    def __repr__(self) -> str:
        """Return a string representation of the instrument."""
        return (
            f"Instrument(name='{self.name}', "
            f"category='{self.category}', "
            f"description='{self.description}')"
        )

    def in_range(self, pitch: MIDIPitch) -> bool:
        """Check if a pitch is in the instrument's range.

        Args:
            pitch: The pitch to check.

        Returns:
            True if the pitch is in the instrument's range, False otherwise.
        """
        return self.range.bottom <= pitch <= self.range.top

    def to_range(
        self,
        pitch: MIDIPitch,
        close_to: MIDIPitch,
    ) -> MIDIPitch:
        """Finds the pitch within the instrument's range, closest to another.

        Args:
            pitch: The pitch to coerce.
            close_to: A pitch close to where the resulting pitch should be.

        Returns:
            The coerced pitch.

        Raises:
            ValueError: If `close_to` is not in the instrument's range.

        Examples:
            >>> from staff import MIDIPitch
            >>> from staff.orchestration.instrument import Instrument, InstrumentRange
            >>> instrument = Instrument(
            ...     name="Violin",
            ...     section="Strings",
            ...     range=InstrumentRange(
            ...         bottom=MIDIPitch.from_string("G3"),
            ...         top=MIDIPitch.from_string("C#7"),
            ...     ),
            ...     articulations=[],
            ...     is_continuous=True,
            ... )

            >>> pitch = MIDIPitch.from_string("E1")
            >>> close_to = MIDIPitch.from_string("E4")  # In range
            >>> expected = MIDIPitch.from_string("E4")
            >>> expected == instrument.to_range(pitch=pitch, close_to=close_to)
            True

            >>> pitch = MIDIPitch.from_string("E1")
            >>> close_to = MIDIPitch.from_string("E7")  # Above range
            >>> expected = MIDIPitch.from_string("E6")
            >>> expected == instrument.to_range(pitch=pitch, close_to=close_to)
            True

            >>> pitch = MIDIPitch.from_string("E1")
            >>> close_to = MIDIPitch.from_string("E3")  # Below range
            >>> expected = MIDIPitch.from_string("E4")
            >>> expected == instrument.to_range(pitch=pitch, close_to=close_to)
            True

            >>> pitch = MIDIPitch.from_string("G1")
            >>> close_to = MIDIPitch.from_string("E4")
            >>> expected = MIDIPitch.from_string("G4")
            >>> expected == instrument.to_range(pitch=pitch, close_to=close_to)
            True

            >>> pitch = MIDIPitch.from_string("G1")
            >>> close_to = MIDIPitch.from_string("E7")
            >>> expected = MIDIPitch.from_string("G6")
            >>> expected == instrument.to_range(pitch=pitch, close_to=close_to)
            True
        """
        if self.in_range(close_to):
            distance = pitch.pitch_class - close_to.pitch_class
            if abs(distance) > (pitch.octave_divs / 2):
                if distance > 0:
                    distance = distance - pitch.octave_divs
                else:
                    distance = distance + pitch.octave_divs
            number = close_to.number + distance
            coerced_pitch = MIDIPitch(
                number=number,
                bend=pitch.bend,
                diapason=pitch.diapason,
                octave_divs=pitch.octave_divs,
            )
            if coerced_pitch < self.range.bottom:
                return coerced_pitch.octave_up()
            elif coerced_pitch > self.range.top:
                return coerced_pitch.octave_down()
            return coerced_pitch

        if close_to < self.range.bottom:
            number = self.range.bottom.number
            while (number % pitch.octave_divs) != pitch.pitch_class:
                number += 1
            return MIDIPitch(
                number=number,
                bend=pitch.bend,
                diapason=pitch.diapason,
                octave_divs=pitch.octave_divs,
            )

        # if close_to > self.range.top:
        number = self.range.top.number
        while (number % pitch.octave_divs) != pitch.pitch_class:
            number -= 1
        return MIDIPitch(
            number=number,
            bend=pitch.bend,
            diapason=pitch.diapason,
            octave_divs=pitch.octave_divs,
        )

    def get_articulation(self, name: str) -> Articulation:
        """Get an articulation by name.

        Args:
            name: The name of the articulation.

        Returns:
            The articulation.

        Raises:
            ValueError: If the articulation does not exist.
        """
        for articulation in self.articulations:
            if articulation.name == name:
                return articulation
        raise ValueError(f"Articulation '{name}' does not exist.")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
