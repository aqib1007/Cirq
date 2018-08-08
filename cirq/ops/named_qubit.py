# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cirq.ops import raw_types


class NamedQubit(raw_types.QubitId):
    """A qubit identified by name."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'cirq.NamedQubit({})'.format(repr(self.name))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return _pad_digits(self.name) >= _pad_digits(other.name)

    def __gt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return _pad_digits(self.name) > _pad_digits(other.name)

    def __le__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return _pad_digits(self.name) <= _pad_digits(other.name)

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return _pad_digits(self.name) < _pad_digits(other.name)

    def __hash__(self):
        return hash((NamedQubit, self.name))


def _pad_digits(text: str) -> str:
    """A str method with hacks to support better lexicographic ordering.

    The output strings are not intended to be human readable.

    The returned string will have digit-runs zero-padded up to at least 8
    digits. That way, instead of 'a10' coming before 'a2', 'a000010' will come
    after 'a000002'.

    Also, the original length of each digit-run is appended after the
    zero-padded run. This is so that 'a0' continues to come before 'a00'.
    """

    was_on_digits = False
    last_transition = 0
    chunks = []

    def handle_transition_at(k):
        chunk = text[last_transition:k]
        if was_on_digits:
            chunk = chunk.rjust(8, '0') + ':' + str(len(chunk))
        chunks.append(chunk)

    for i in range(len(text)):
        on_digits = text[i].isdigit()
        if was_on_digits != on_digits:
            handle_transition_at(i)
            was_on_digits = on_digits
            last_transition = i

    handle_transition_at(len(text))
    return ''.join(chunks)