from __future__ import annotations

import itertools as it
from dataclasses import dataclass
from functools import lru_cache
from statistics import pstdev
from typing import List, Tuple, Union

from staff import MIDIPitch
from staff.orchestration.instrument import Instrument


@dataclass
class VoicedPitch:
    instrument: Instrument
    pitch: MIDIPitch

    def __repr__(self):
        s = "VoicedPitch:\n"
        s += f"  instrument: {self.instrument.name}\n"
        s += f"  pitch: {self.pitch}\n"
        return s

    def __hash__(self) -> int:
        return hash(hash(self.instrument) + hash(self.pitch))


class VoicedChord:
    def __init__(self, voices: List[VoicedPitch]):
        self._voices = voices
        self._spread: float = pstdev(
            (p.number_precise for p in (v.pitch for v in self.voices))
        )

    @property
    def voices(self) -> List[VoicedPitch]:
        return self._voices

    @property
    def spread(self) -> float:
        return self._spread

    def __repr__(self):
        s = "VoicedChord:\n"
        s += f"  spread: {self.spread}\n"
        for voice in reversed(self.voices):
            s += f"  - {voice.instrument.name}: {voice.pitch}\n"
        return s

    def __eq__(self, other):
        return self.spread == other.spread

    def __gt__(self, other):
        return self.spread > other.spread

    def __hash__(self) -> int:
        return hash(
            f"{self.spread}"
            f"{[v.instrument.name for v in self._voices]}"
            f"{[v.pitch.number_precise for v in self._voices]}"
        )

    def contains_crossing(self) -> bool:
        pitch: float = -1
        for voiced_pitch in sorted(self._voices, key=lambda v: v.instrument):
            new_pitch = voiced_pitch.pitch.number_precise
            if new_pitch < pitch:
                return True
            pitch = new_pitch
        return False

    def contains_doubling(self) -> bool:
        return len(set(self.voices)) != len(self.voices)


def voice_pitches(
    pitches: List[MIDIPitch],
    instruments: List[Instrument],
    spread: float = 0.5,
) -> Union[VoicedChord, None]:
    _pitches = tuple(pitches)
    _instruments = tuple(instruments)
    voicings = find_all_voicings(pitches=_pitches, instruments=_instruments)
    if not voicings:
        return None
    spread_ix = max(0, min(len(voicings) - 1, int(spread * len(voicings))))
    return voicings[spread_ix]


@lru_cache
def find_all_voicings(
    pitches: Tuple[MIDIPitch],
    instruments: Tuple[Instrument],
) -> List[VoicedChord]:
    """Voice a list of pitches for a given ensemble of instruments.

    Note:
        Does not maintain ordering, so you could end up with an inversion.

    Args:
        pitches: The pitches to voice.
        instruments: The instruments to voice the pitches for.

    Returns:
        A list of tuples of the form (pitch, instrument).

    Raises:
        ValueError: If the pitches are not all of equal octave divisions.
    """
    _pitches: List[MIDIPitch] = list(pitches)
    _instruments: List[Instrument] = list(instruments)
    if not _validate_eq_octave_divs(pitches=_pitches):
        raise ValueError("Pitches are not all of equal octave divs.")

    pitch_classes: List[MIDIPitch] = [p.pitch_class_precise for p in _pitches]
    candidates = _generate_voicing_candidates(
        instruments=_instruments,
        pitch_classes=pitch_classes,
    )
    allocations = _generate_voicing_allocations(
        instruments=_instruments,
        pitch_classes=pitch_classes,
    )
    voicings = _combine_candidate_allocations(
        instruments=_instruments,
        pitch_classes=pitch_classes,
        candidates=candidates,
        allocations=allocations,
    )
    voicings = sorted(list(set(voicings)))
    # print(f"{len(voicings)} voicings found")
    return voicings


def _validate_eq_octave_divs(pitches: List[MIDIPitch]) -> bool:
    divs = pitches[0].octave_divs
    for pitch in pitches[1:]:
        if pitch.octave_divs != divs:
            return False
    return True


def _generate_voicing_candidates(
    instruments: List[Instrument],
    pitch_classes: List[MIDIPitch],
) -> List[Tuple[Instrument, List[List[MIDIPitch]]]]:
    """`MIDIPitches` for each pitch class within each instrument's range."""
    candidates: List[Tuple[Instrument, List[List[MIDIPitch]]]] = []
    for instrument in instruments:
        pitches_in_range: List[List[MIDIPitch]] = []
        for i, pitch_class in enumerate(pitch_classes):
            pitch_class_in_range: List[MIDIPitch] = []
            pitches_in_range.append(pitch_class_in_range)
            pitch = pitch_class
            while pitch <= instrument.range.top:
                if instrument.in_range(pitch=pitch):
                    pitches_in_range[i].append(pitch)
                pitch = pitch.octave_up()
        assert len(pitches_in_range) == len(pitch_classes)
        candidates.append((instrument, pitches_in_range))
        # Verbose
        # print(instrument.name)
        # for pcl in pitches_in_range:
        #     print(f"    {[p.number for p in pcl]}")
    return candidates


def _generate_voicing_allocations(
    instruments: List[Instrument],
    pitch_classes: List[MIDIPitch],
) -> List[List[VoicedPitch]]:
    """Pitch-class combinations assigned to the given instruments."""
    allocations: List[List[VoicedPitch]] = []
    for combination in it.combinations_with_replacement(
        pitch_classes, len(instruments)
    ):
        if set(combination) != set(pitch_classes):
            continue
        for permutation in it.permutations(combination):
            candidate_allocations: List[VoicedPitch] = []
            for i, pitch in enumerate(permutation):
                candidate_allocations.append(VoicedPitch(instruments[i], pitch))
            allocations.append(candidate_allocations)
    # Verbose
    # print(f"Found {len(allocations)} allocation candidates")
    # for i, allocation in enumerate(allocations[:3]):
    #     print(f"\nCandidate {i}")
    #     for voice in allocation:
    #         print(f"    {voice.instrument.name:16}{voice.pitch}")
    return allocations


def _combine_candidate_allocations(
    instruments: List[Instrument],
    pitch_classes: List[MIDIPitch],
    candidates: List[Tuple[Instrument, List[List[MIDIPitch]]]],
    allocations: List[List[VoicedPitch]],
) -> List[VoicedChord]:
    voiced: List[VoicedChord] = []
    for allocation in allocations:
        pc_candidates: List[Tuple[Instrument, List[MIDIPitch]]] = []
        for voice in allocation:
            pitches_ix = pitch_classes.index(voice.pitch)
            instrument_ix = [i.name for i in instruments].index(voice.instrument.name)
            pc_candidates.append(
                (candidates[instrument_ix][0], candidates[instrument_ix][1][pitches_ix])
            )
        pitch_candidates = list(it.product(*(pcc[1] for pcc in pc_candidates)))
        for pc in pitch_candidates:
            voices = [VoicedPitch(i, p) for i, p in zip(instruments, pc)]
            vc = VoicedChord(voices=voices)
            if vc.contains_doubling() or vc.contains_crossing():
                continue
            voiced.append(vc)
    return voiced


if __name__ == "__main__":
    from staff.db.instruments import load_instrument

    instruments = (
        load_instrument("Violins 1", category="BBC Symphony Orchestra"),
        load_instrument("Violins 2", category="BBC Symphony Orchestra"),
        load_instrument("Violas", category="BBC Symphony Orchestra"),
        load_instrument("Celli", category="BBC Symphony Orchestra"),
        load_instrument("Basses", category="BBC Symphony Orchestra"),
    )

    pitches = (MIDIPitch(0), MIDIPitch(3), MIDIPitch(7), MIDIPitch(10))

    voicings = find_all_voicings(pitches=pitches, instruments=instruments)

    for v in voicings[-3:]:
        print(v)
