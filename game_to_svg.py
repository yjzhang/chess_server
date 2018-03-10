import svgutils.transform as sg

PIECE_MAP = {
        2: 'Chess_pdt45.svg',
        4: 'Chess_rdt45.svg',
        6: 'Chess_ndt45.svg',
        8: 'Chess_bdt45.svg',
        10: 'Chess_qdt45.svg',
        12: 'Chess_kdt45.svg',
        14: 'Chess_mdt45.svg',

        3: 'Chess_plt45.svg',
        5: 'Chess_rlt45.svg',
        7: 'Chess_nlt45.svg',
        9: 'Chess_blt45.svg',
        11: 'Chess_qlt45.svg',
        13: 'Chess_klt45.svg',
        15: 'Chess_mlt45.svg',
        }

def game_to_svg(game_state):
    """
    converts game to an svg
    """
    board = game_state.board
    fig = sg.fromfile('baroque_chess_images/' + 'chess_50.svg')
    for i in range(8):
        for j in range(8):
            pos = board[i][j]
            if pos > 1:
                if pos == 2:
                    print('pawn')
                filename = PIECE_MAP[pos]
                svg_file = sg.fromfile('baroque_chess_images/'+filename)
                piece_svg = svg_file.getroot()
                piece_svg.moveto(j*50+2, i*50+2)
                fig.append(piece_svg)
    return fig

"""
    chess_board = svgwrite.Drawing(filename='chess.svg',
            size=('400px', '400px'))
    # chess pieces are 60x60 px
    # so board squares should be ... 80x80?
    #chess_board.add(dwg.rect((0,0), (640,640), fill='white'))
    for i in range(8):
        for j in range(8):
            color = 'rgb(255,206,158)' # light color
            if i%2 == 0:
                if j%2 == 0:
                    color = 'rgb(209,139,71)' # dark color
            else:
                if j%2 == 1:
                    color = 'rgb(209,139,71)'
            chess_board.add(chess_board.rect((i*50, j*50),
                                ((i+1)*50, (j+1)*50),
                                fill=color))
"""
