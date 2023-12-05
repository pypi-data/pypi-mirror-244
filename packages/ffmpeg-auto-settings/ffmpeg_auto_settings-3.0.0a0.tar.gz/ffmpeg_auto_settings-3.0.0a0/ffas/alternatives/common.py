# Copyright (C) 2023 liancea
#
# This file is part of ffmpeg-auto-settings.
#
# ffmpeg-auto-settings is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License Version 3 as published by the Free Software Foundation.
#
# ffmpeg-auto-settings is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with ffmpeg-auto-settings. If not, see
# <https://www.gnu.org/licenses/>.

import sys
from decimal import Decimal
from ..config import Config, get_configured_sample
from ..encoding import create_sample_encode, calculate_vmaf
from ..terminal import write_terminal_line
from ..videostore import VideoStore, NoResultFound


def derive_target_vmaf(preset: str, crf: Decimal, only_use_db: bool) -> Decimal:
    store = VideoStore()
    config = Config()
    configured_metric = 'vmaf_harmonic' if config['use_harmonic_mean'] else 'vmaf'
    encoder = config['encoder']

    needs_encode = False
    try:
        encode = store.get_video(
            type='sample-encode',
            encoder=encoder,
            preset=preset,
            crf=crf
        )
        if encode.vmaf:
            # vmaf values were already calculated, can return instantly
            return getattr(encode, configured_metric)
        if only_use_db:
            raise LookupError('A matching encode exists, but vmaf was not yet calculated.')
    except NoResultFound:
        needs_encode = True
        if only_use_db:
            raise LookupError('No matching encode found')

    write_terminal_line(-4, f'Determining VMAF for crf {crf:.2f} @{preset}')

    if needs_encode:
        encode = create_sample_encode(encoder=encoder, preset=preset, crf=crf)
    calculate_vmaf(get_configured_sample(), encode)

    return getattr(encode, configured_metric)


def ensure_valid_args_combination(from_preset: str | None, from_crf: Decimal | None, vmaf: Decimal | None):
    # crunch values into bool of them being defined (not None) to make function more readable
    # while not accidentally acting on other truthy/falsy values
    from_preset = from_preset is not None
    from_crf = from_crf is not None
    vmaf = vmaf is not None

    all_missing = not (from_preset or from_crf or vmaf)
    wrongly_mixed_usage = (from_preset or from_crf) and vmaf
    from_group_incomplete = (from_preset != from_crf)  # "xor"

    if all_missing or wrongly_mixed_usage or from_group_incomplete:
        sys.exit('Invalid argument combination: Set either (--from-preset + --from-crf) OR --vmaf')
