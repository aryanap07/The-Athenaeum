from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Move:
    start: tuple[int, int]
    end: tuple[int, int]
    captures: tuple[tuple[int, int], ...] = field(default_factory=tuple)
    promoted: bool = False

    @property
    def is_capture(self) -> bool:
        return len(self.captures) > 0

    @property
    def is_promotion(self) -> bool:
        return self.promoted

    @property
    def jump_count(self) -> int:
        return len(self.captures)
