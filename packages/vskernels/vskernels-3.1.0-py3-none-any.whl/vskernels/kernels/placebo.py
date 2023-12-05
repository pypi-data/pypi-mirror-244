from __future__ import annotations

from math import ceil
from typing import Any, Callable

from stgpytools import inject_kwargs_params
from vstools import Transfer, TransferT, core, fallback, inject_self, vs

from .complex import LinearScaler

__all__ = [
    'Placebo'
]


class Placebo(LinearScaler):
    _kernel: str
    """Name of the placebo kernel"""

    # Kernel settings
    taps: float | None
    b: float | None
    c: float | None

    # Filter settings
    clamp: float
    blur: float
    taper: float

    # Quality settings
    antiring: float
    cutoff: float

    # Other settings
    lut_entries: int = 64

    scale_function = core.lazy.placebo.Resample

    def __init__(
        self,
        taps: float | None = None, b: float | None = None, c: float | None = None,
        clamp: float = 0.0, blur: float = 0.0, taper: float = 0.0,
        antiring: float = 0.0, cutoff: float = 0.001,
        **kwargs: Any
    ) -> None:
        self.taps = taps
        self.b = b
        self.c = c
        self.clamp = clamp
        self.blur = blur
        self.taper = taper
        self.antiring = antiring
        self.cutoff = cutoff
        super().__init__(**(dict(curve=Transfer.BT709) | kwargs))

    @inject_self.cached
    @inject_kwargs_params
    def scale(  # type: ignore[override]
        self, clip: vs.VideoNode, width: int, height: int, shift: tuple[float, float] = (0, 0),
        *, linear: bool = True, sigmoid: bool | tuple[float, float] = True, curve: TransferT | None = None,
        **kwargs: Any
    ) -> vs.VideoNode:
        return super().scale(
            clip, width, height, shift, linear=linear, sigmoid=sigmoid,
            trc=Transfer.from_param_or_video(curve, clip).value_libplacebo
        )

    def get_scale_args(
        self, clip: vs.VideoNode, shift: tuple[float, float] = (0, 0),
        width: int | None = None, height: int | None = None,
        *funcs: Callable[..., Any], **kwargs: Any
    ) -> dict[str, Any]:
        return (
            dict(sx=shift[1], sy=shift[0])
            | self.get_clean_kwargs(*funcs)
            | self.get_params_args(False, clip, width, height, **kwargs)
        )

    def get_params_args(
        self, is_descale: bool, clip: vs.VideoNode, width: int | None = None, height: int | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        return dict(
            width=width, height=height, filter=self._kernel,
            radius=self.taps, param1=self.b, param2=self.c,
            clamp=self.clamp, taper=self.taper, blur=self.blur,
            antiring=self.antiring, cutoff=self.cutoff,
            lut_entries=self.lut_entries
        ) | kwargs

    @inject_self.property
    def kernel_radius(self) -> int:  # type: ignore
        from .bicubic import Bicubic

        if self.taps:
            return ceil(self.taps)

        if self.b or self.c:
            return Bicubic(fallback(self.b, 0), fallback(self.c, 0.5)).kernel_radius

        return 2
