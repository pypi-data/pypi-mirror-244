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
from pathlib import Path
import shutil
from typing import Literal
import decimal
from decimal import Decimal
from dataclasses import dataclass
from prettytable import PrettyTable
from .terminal import write_terminal_line
from .encoding import create_sample_encode, calculate_vmaf
from .config import Config, get_configured_sample
from .misc import ORDERED_PRESETS, get_extension_for_mimetype, print_err, freeform_presets_to_list
from .videostore import VideoStore, Video, NoResultFound


def export_generated_encode(encode: Video) -> Literal['hardlink', 'symlink', 'copy', 'skipped']:
    """
    Export a generated encode under an informative name

    Does nothing if encode was already exported (returns "skipped")
    :param encode: sample-encode to export
    :return: the method used to export
    """
    # create directory for each sample base
    dirname = get_configured_sample().variant
    Path(dirname).mkdir(exist_ok=True)

    # build basename
    sorting_number = f'{ORDERED_PRESETS.index(encode.preset)}'  # provides better sorting in directory view
    basename = f'{sorting_number}_{encode.preset}_{encode.crf}'

    # guess extension
    try:
        from magic import Magic  # delay import for systems without libmagic
        mimetype = Magic(mime=True).from_file(encode.filename)
        extension = f'.{get_extension_for_mimetype(mimetype)}'
    except ImportError as e:
        print_err(f'Warning: cannot guess extension without magic, but: {e}')
        extension = ''
    except KeyError:
        print_err(f'Warning: mimetype {mimetype} has no known file extension')
        extension = ''

    # make paths
    source_path = Path(encode.filename)
    target_path = Path(f'{dirname}/{basename}{extension}')

    # export file in order of most convenient methods: hardlink > symlink > copy
    if target_path.is_file():
        # should be okay
        return 'skipped'
    try:
        target_path.hardlink_to(source_path)
        return 'hardlink'
    except Exception:
        try:
            target_path.symlink_to(source_path)
            return 'symlink'
        except Exception:
            shutil.copyfile(source_path, target_path)  # may ultimately raise an error
            return 'copy'


def cmd_generate(args):
    # create list of presets
    try:
        presets = freeform_presets_to_list(args.presets)
    except ValueError as e:
        sys.exit(f'Invalid presets argument: {e}')

    # create list of crf values
    if '-' in args.crf_range:
        # got range
        try:
            start, end = args.crf_range.split('-')
        except ValueError:
            # tuple unpack into two parts makes too few *and* too many dashes a ValueError
            sys.exit(f'Invalid crf range "{args.crf_range}"')

        try:
            start = Decimal(start)
        except decimal.InvalidOperation:
            sys.exit(f'Invalid crf on left side of range: "{start}"')

        try:
            end = Decimal(end)
        except decimal.InvalidOperation:
            sys.exit(f'Invalid crf on right side of range: "{end}"')

        crfs = [start]
        if start < end:
            # increasing values
            while crfs[-1] + args.step_width <= end:
                crfs.append(crfs[-1] + args.step_width)
        else:
            # decreasing values
            while crfs[-1] - args.step_width >= end:
                crfs.append(crfs[-1] - args.step_width)

        # explicitly include range end in crfs, even if it's not in (start + n * step_width)
        if crfs[-1] != end:
            crfs.append(end)
    else:
        # got single value
        try:
            crf = Decimal(args.crf_range)
        except decimal.InvalidOperation:
            sys.exit(f'Invalid crf "{args.crf_range}"')
        if not (0 <= crf <= 51):
            sys.exit(f'crf "{crf}" is out of bounds! Needs to be between 0 and 51.')
        crfs = [crf]

    generate_encodes(presets, crfs)


def generate_encodes(presets: list[str], crfs: list[Decimal]):
    # setup
    log_lines = []
    config = Config()
    store = VideoStore()
    sample = get_configured_sample()

    # 4 newlines to push terminal output down
    print('\n\n\n')

    n_current_encode = 1
    n_total_encodes = len(presets) * len(crfs)
    exported_by_copy_at_least_once = False
    for preset in presets:
        n_current_sample_encode = 1
        for crf in crfs:
            # check if we already encoded this combination or didn't finish vmaf calculation
            try:
                existing_encode = store.get_video(
                    type='sample-encode',
                    encoder=config['encoder'],
                    preset=preset,
                    crf=crf,
                    variant=sample.variant
                )

                if existing_encode.vmaf is None:
                    write_terminal_line(-4, 'Fixing interrupted run -- calculating stray vmaf-less sample-encode')
                    calculate_vmaf(sample, existing_encode)

                # increment progress counters; export
                n_current_sample_encode += 1
                n_current_encode += 1
                try:
                    export_method = export_generated_encode(existing_encode)
                    if export_method == 'copy':
                        exported_by_copy_at_least_once = True
                except Exception as e:
                    log_lines.append(f'Unable to export file: [{e.__class__.__name__}] {str(e)}')

                # skip to next encode
                continue
            except NoResultFound:
                # the usual case, we have to create the encode first
                pass

            write_terminal_line(
                -4,
                (
                    f'Generating encode {n_current_encode}/{n_total_encodes}'
                    f' ({n_current_sample_encode}/{len(crfs)} of preset {preset})'
                )
            )

            # encode video, calculate vmaf
            encode = create_sample_encode(encoder=config['encoder'], preset=preset, crf=crf)
            calculate_vmaf(sample, encode)

            # increment progress counters; export
            n_current_sample_encode += 1
            n_current_encode += 1
            try:
                export_method = export_generated_encode(encode)
                if export_method == 'copy':
                    exported_by_copy_at_least_once = True
            except Exception as e:
                log_lines.append(f'Unable to export file: [{e.__class__.__name__}] {str(e)}')

    if exported_by_copy_at_least_once:
        log_lines.append('Warning: Had to copy instead of link files at least once')

    # show results
    show_info(sample, presets, crfs)

    if log_lines:
        print('')  # newline
        for line in log_lines:
            print(line)


@dataclass
class VideoStub:
    preset: str
    crf: Decimal
    vmaf: str = 'n/a'
    vmaf_harmonic: str = 'n/a'


def show_info(sample: Video, presets: list[str], crfs: list[Decimal]):
    store = VideoStore()
    config = Config()

    t = PrettyTable()
    t.field_names = ['preset', 'crf', 'vmaf_harmonic', 'vmaf']
    for preset in presets:
        for crf in crfs:
            try:
                encode = store.get_video(
                    type='sample-encode',
                    encoder=config['encoder'],
                    preset=preset,
                    crf=crf,
                    variant=sample.variant
                )
            except NoResultFound:
                encode = VideoStub(preset=preset, crf=crf)

            t.add_row([
                encode.preset,
                encode.crf,
                encode.vmaf_harmonic,
                encode.vmaf
            ])

    print(f'\nSample: {sample.variant}')
    print(t)
