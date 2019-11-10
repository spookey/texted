import sys

from PIL import Image, ImageColor, ImageDraw, ImageFont
import click

CLI_PROG = 'texted'
CLI_VERS = '0.0.0'


class PILTrueTypeFontParamType(click.ParamType):
    name = 'PIL TrueType Font'

    def convert(self, value, param, ctx):
        try:
            return ImageFont.truetype(value)
        except IOError:
            self.fail(f'{value} is not a valid font', param, ctx)

    def __repr__(self):
        return 'PILTrueTypeFont'


class PILColorParamType(click.ParamType):
    name = 'PIL Color'

    def convert(self, value, param, ctx):
        try:
            return ImageColor.getrgb(value)
        except ValueError:
            self.fail(f'{value} is not a valid color', param, ctx)

    def __repr__(self):
        return 'PILColor'


@click.command()
@click.version_option(prog_name=CLI_PROG, version=CLI_VERS)
@click.argument(
    'textfile', envvar='INPUT',
    type=click.File(mode='r', lazy=False),
)
@click.argument(
    'imagefile', envvar='OUTPUT',
    type=click.File(mode='wb', lazy=True),
)
@click.option(
    '-f', '--font', 'font', envvar='FONT',
    type=PILTrueTypeFontParamType(),
    default='Helvetica', show_default=True,
    help='TrueType or OpenType font to use (can also be a full path)',
)
@click.option(
    '-s', '--size', 'size', envvar='SIZE',
    type=click.IntRange(min=1),
    default=12, show_default=True,
    help='Font size (in points)',
)
@click.option(
    '-g', '--gap', 'gap', envvar='GAP',
    type=click.IntRange(min=0),
    default=0, show_default=True,
    help='Gap around image (in pixels)',
)
@click.option(
    '-a', '--align', 'align', envvar='ALIGN',
    type=click.Choice(['left', 'center', 'right'], case_sensitive=False),
    default='left', show_default=True,
    help='Text alignment (for multiline)',
)
@click.option(
    '-bg', '--background', 'bg', envvar='COL_BG',
    type=PILColorParamType(),
    default='#ffffff', show_default=True,
    help='Background color (in hex, rgb, rgba, hsl, hsv, X11)',
)
@click.option(
    '-fg', '--foreground', 'fg', envvar='COL_FG',
    type=PILColorParamType(),
    default='#000000', show_default=True,
    help='Foreground color (in hex, rgb, rgba, hsl, hsv, X11)',
)
def main(textfile, imagefile, font, **cargs):

    if font.size != cargs['size']:
        font = font.font_variant(size=cargs['size'])

    text = textfile.read()

    frmt = None if imagefile.name != '-' else 'PNG'

    mode = 'RGBA' if any(
        len(cargs[col]) > 3 for col in ('fg', 'bg')
    ) else 'RGB'

    dims = tuple(
        (2 * cargs['gap']) + dim for dim in font.getsize_multiline(text)
    )

    imag = Image.new(mode, dims, color=cargs['bg'])
    draw = ImageDraw.Draw(imag)

    draw.text(
        (cargs['gap'], cargs['gap']),
        text,
        fill=cargs['fg'],
        font=font,
        align=cargs['align'],
    )

    try:
        imag.save(imagefile, format=frmt)
    except (ValueError, IOError) as ex:
        raise click.UsageError(ex)

    return 0


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    sys.exit(main())
