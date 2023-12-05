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

import argparse
from pathlib import Path
from decimal import Decimal
import sys
from . import basic, sample, generate, alternatives
from .misc import print_err, ORDERED_PRESETS


parser = argparse.ArgumentParser(
    prog='ffas',
    description='ffmpeg-auto-settings - various ffmpeg video encoding helpers'
)
subparsers = parser.add_subparsers(required=True, dest='subcommand_level_0', metavar='subcommand')

# command: init
p_init = subparsers.add_parser(
    'init',
    help='initialize the current directory for use with ffas'
)
p_init.add_argument('video_file', type=Path, nargs='?', help='path to source video (as in `ffas import`)')
p_init_group = p_init.add_mutually_exclusive_group()
p_init_group.add_argument('-c', '--copy', action='store_true', help='copy instead of hardlink (as in `ffas import`)')
p_init_group.add_argument('-s', '--symlink', action='store_true', help='symlink instead of hardlink (as in `ffas import`)')

# command: config
p_config = subparsers.add_parser(
    'config',
    help='configure (default) encoding parameters'
)
p_config_group = p_config.add_mutually_exclusive_group()
p_config_group.add_argument('-i', '--interactive', action='store_true', help='run interactive configuration (default)')
p_config_group.add_argument('-f', '--template-file', type=argparse.FileType('r'), help='apply options from toml TEMPLATE_FILE to current configuration')

# command: import
p_import = subparsers.add_parser(
    'import',
    help='Import a video file as source'
)
p_import.add_argument('video_file', type=Path, help='path to source video')
p_import_group = p_import.add_mutually_exclusive_group()
p_import_group.add_argument('-c', '--copy', action='store_true', help='copy instead of hardlink')
p_import_group.add_argument('-s', '--symlink', action='store_true', help='symlink instead of hardlink')

# command: time-based-sample, tbs
long_help = 'Creates a sample from multiple scenes determined by (approx.) evenly distributed timespans'
for p_command, p_help in [('time-based-sample', long_help), ('tbs', 'alias for time-based-sample')]:
    p_time_based_sample = subparsers.add_parser(
        p_command,
        help=p_help,
        description='You need to supply exactly two arguments out of `length`, `scene-length` and `scene-count`.'
    )
    p_time_based_sample.add_argument('-l', '--length', help='target length of full sample')
    p_time_based_sample.add_argument('-t', '--scene-length', help='length of each scene')
    p_time_based_sample.add_argument('-c', '--scene-count', type=int, help='how many scenes to extract')
    p_time_based_sample.add_argument(
        '-n', '--no-update-config', dest='update_config', action='store_false',
        help="don't update 'sample_variant' config afterwards"
    )

# command: export
p_export = subparsers.add_parser('export', help='make internally stored encode available under custom name')
p_export.add_argument('-n', '--no-guess-ext', action='store_true',
                      help="don't attempt to guess an appropriate file extension")
p_export.add_argument('-c', '--copy', action='store_true', help='copy instead of hardlink')
p_export.add_argument('id_or_tag', help='encode id or tag name')
p_export.add_argument('file_name', nargs='?', help='filename to export encode to')

# command: list
p_list = subparsers.add_parser('list', help='list all known encodes')
p_list.add_argument('filter', nargs='*', help='metadata filter(s) in the form `key=value`')

# command: alternatives find / alt find
presets_syntax_help = (
    'You may specify multiple presets separated by commas and/or in ranges. Examples:\n'
    '  --presets medium\n'
    '  --presets fast,faster\n'
    '  --presets faster-slow\n'
    '  --presets slow-faster\n'
    '  --presets veryfast,fast-slower'
)
s_alt = subparsers.add_parser(
    'alternatives',
    aliases=['alt'],
    help='find settings for equivalent quality at different presets',
).add_subparsers(required=True, dest='subcommand_level_1', metavar='subcommand')
p_alt_find = s_alt.add_parser(
    'find',
    help='find preset/crf pairs with matching VMAF scores',
    description=presets_syntax_help,
    formatter_class=argparse.RawTextHelpFormatter
)
p_alt_find.add_argument('-p', '--presets',
                        required=True,
                        help='find alternatives within these presets')
p_alt_find.add_argument('-ch', '--crf-hints',
                        action='store_true',
                        help='use results to preseed crf hints for further invocations')
p_alt_find.add_argument('-d', '--vmaf-delta',
                        type=Decimal,
                        default='0.2',
                        help='allowed tolerance for VMAF values (vmaf <= target <= vmaf + vmaf_delta)')
p_alt_find.add_argument('-fp', '--from-preset',
                        type=lambda s: s.lower(),
                        choices=ORDERED_PRESETS,
                        metavar='FROM_PRESET',
                        help='derive VMAF from encoding settings (use together with --from-crf)')
p_alt_find.add_argument('-fc', '--from-crf',
                        type=Decimal,
                        help='derive VMAF from encoding settings (use together with --from-preset)')
p_alt_find.add_argument('-v', '--vmaf',
                        type=Decimal,
                        help='specify target VMAF directly')

# command: alternatives show / alt show
p_alt_show = s_alt.add_parser(
    'show',
    help='show preset/crf pairs found in `alternatives find',
    description=presets_syntax_help,
    formatter_class=argparse.RawTextHelpFormatter
)
p_alt_show.add_argument('-p', '--presets',
                        required=True,
                        help='show alternatives within these presets')
p_alt_show.add_argument('-d', '--vmaf-delta',
                        type=Decimal,
                        default='0.2',
                        help='allowed tolerance for vmaf values (vmaf <= target <= vmaf + vmaf_delta)')
p_alt_show.add_argument('-fp', '--from-preset',
                        type=lambda s: s.lower(),
                        choices=ORDERED_PRESETS,
                        metavar='FROM_PRESET',
                        help='derive VMAF from encoding settings (use together with --from-crf)')
p_alt_show.add_argument('-fc', '--from-crf',
                        type=Decimal,
                        help='derive VMAF from encoding settings (use together with --from-preset)')
p_alt_show.add_argument('-v', '--vmaf',
                        type=Decimal,
                        help='specify target VMAF directly')

# command: generate
crf_range_help = (
    'crf ranges can have a start and an end, separated by a dash, or just one value. Examples:\n'
    '  --crf-range 18-35\n'
    '  --crf-range 35-18\n'
    '  --crf-range 22\n'
    '  --crf-range 27.5'
)
generate_export_help = 'All requested encodes will be exported to your project directory for assessment.'
p_generate = subparsers.add_parser(
    'generate',
    aliases=['gen'],
    help='generate sample-encodes, calculate VMAF and export files',
    description=f'{presets_syntax_help}\n\n{crf_range_help}\n\n{generate_export_help}',
    formatter_class=argparse.RawTextHelpFormatter
)
p_generate.add_argument('-p', '--presets', required=True, help='generate using these preset(s)')
p_generate.add_argument('-c', '--crf-range',
                        required=True,
                        help='"<start>-<end>" to generate within a range, or just "<crf>" to generate a single encode')
p_generate.add_argument('-s', '--step-width',
                        type=Decimal,
                        default='1',
                        help='generate one encode every <step-width> crf')

# command: version
p_version = subparsers.add_parser('version', help='show version and license info')

# parse arguments and run
args = parser.parse_args()
command_map = {
    'top-level': {
        'init': basic.cmd_init,
        'import': basic.cmd_import,
        'config': basic.cmd_config,
        'time-based-sample': sample.cmd_time_based_sample,
        'tbs': sample.cmd_time_based_sample,
        'export': basic.cmd_export,
        'list': basic.cmd_list,
        'alternatives': 'alternatives',
        'alt': 'alternatives',
        'generate': generate.cmd_generate,
        'version': basic.cmd_version
    },
    'alternatives': {
        'find': alternatives.find.cmd_alt_find,
        'show': alternatives.show.cmd_alt_show
    }
}
if args.subcommand_level_0 not in ('init', 'version'):
    if not Path('.ffas').is_dir():
        print_err('Not inside a ffas project (.ffas directory was not found).')
        print_err('To start a new project, create an empty directory, `cd` into it and run `ffas init [<file>]`')
        sys.exit(1)

use_map = command_map['top-level']
level = 0
while True:
    argparse_name = f'subcommand_level_{level}'
    cmd_name = getattr(args, argparse_name)
    if isinstance(use_map[cmd_name], str):
        # descend into deeper map
        level += 1
        use_map = command_map[use_map[cmd_name]]
        continue  # superfluous, only added for clarity
    else:
        # resolve function from current map
        cmd_function = use_map[cmd_name]
        break

sys.exit(cmd_function(args))
