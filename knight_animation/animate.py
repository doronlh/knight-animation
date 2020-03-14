import webbrowser
from cairosvg import svg2png
from chess import Board, SquareSet, square
from chess.svg import board as svg_board
from imageio import imread, mimwrite
from webbrowser import Error as WebbrowserError

_WEBBROWSERS_TO_TRY = ['chrome', 'firefox', 'safari', 'windows-default']


def _convert_coord_to_fen(x, y):
    """
    Convert zero-indexed coordinates from top left corner to a FEN (Forsyth–Edwards Notation) of the chess board
    containing the knight at the give position
    Parameters
    ----------
    x: int
        the x position of the knight starting from the top left (zero-indexed)
    y: int
        the y position of the knight starting from the top left (zero-indexed)

    Returns
    -------
    str
        the FEN of the board with the knight at the given position

    """

    # default empty board
    fen = ['8'] * 8

    # generate the row in FEN for the where the knight is located and insert into board
    fen_row = [(str(elem) if elem > 0 else '') for elem in [x, 7 - x]]
    fen_row.insert(1, 'N')
    fen[y] = ''.join(fen_row)

    # join all the rows of the FEN
    return '/'.join(fen)


def _generate_svg(x, y, previous_positions):
    """
    Generate a single svg for one frame of the animation

    Parameters
    ----------
    x: int
        the current x position of the knight starting from the top left (zero-indexed)
    y: int
        the current y position of the knight starting from the top left (zero-indexed)
    previous_positions: list
        a list of previous positions of the knight, which will be marked with an 'x' symbol in the animation

    Returns
    -------
    str
        the SVG of the current position of the knight with previous steps shown

    """

    # represent the knight on the board
    board = Board(_convert_coord_to_fen(x, y))

    # represent the previous positions of the knight
    squares = SquareSet([square(prev_x, 7 - prev_y) for prev_x, prev_y in previous_positions])

    # generate SVG
    return svg_board(board=board, squares=squares)


def _get_webbrowser(webbrowser_name):
    """
    Get a webbrowser controller. Webbrowser name can be specified. If not specified then attempt get a Webbrowser
    controller object from a list of predefined webbrowser names

    Parameters
    ----------
    webbrowser_name: str
        the name of the webbrowser. See https://docs.python.org/2/library/webbrowser.html#webbrowser.register for a list
        of possibilities

    Returns
    -------
    A webbrowser controller object

    """

    if webbrowser_name:
        return webbrowser.get(webbrowser_name)
    else:
        for browser_name in _WEBBROWSERS_TO_TRY:
            try:
                return webbrowser.get(browser_name)
            except WebbrowserError:
                continue
        return webbrowser.get()


def animate_knight(positions, animation_filename=None, open_in_webbrowser=True, webbrowser_name=None):
    """

    Parameters
    ----------
    positions: list
        a list of zero-indexed coordinates from top left of the chess board which represent the path of the knight
    animation_filename: str
        the filename of the output GIF animation
    open_in_webbrowser: bool
        should the browser open and show the GIF animation?
    webbrowser_name: str
        if the open_browser=True, then the name  of the webbrowser to use. See _get_webbrowser() function

    """

    # generate svgs
    previous_positions = []
    svgs_text = []
    for x, y in positions:
        svgs_text.append(_generate_svg(x, y, previous_positions))
        previous_positions.append((x, y))

    # create frames for imageio
    frames = []
    for svg_text in svgs_text:
        png_bytes = svg2png(bytestring=svg_text)
        frames.append(imread(png_bytes))

    # write animation using imageio
    mimwrite(animation_filename, frames, duration=1)

    # open in browser
    if open_in_webbrowser:
        _get_webbrowser(webbrowser_name).open(f'file:///{animation_filename}')
