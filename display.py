import sys
import curses

curses.setupterm()

cursor_pos = 0
n_cols = curses.tigetnum('cols') or 80

COLOURS = {
	'BLACK'		: 0,
	'BLUE'		: 1,
	'GREEN'		: 2,
	'CYAN'		: 3,
	'RED'		: 4,
	'MAGENTA'	: 5,
	'YELLOW'	: 6,
	'WHITE'		: 7,
}

set_fg = curses.tigetstr('setf') or ''
normal = curses.tigetstr('sgr0') or ''

def checking(msg, indent = 2):
	global cursor_pos
	if cursor_pos:
		result('!', 'RED')
	msg = (' ' * indent) + msg
	cursor_pos = len(msg)
	sys.stdout.write(msg)
	sys.stdout.flush()

def result(msg, colour = 'GREEN'):
	global cursor_pos
	result_col = n_cols - max(15, len(msg) + 5)
	if cursor_pos > result_col:
		print
		cursor_pos = 0
	if colour:
		msg = highlight(msg, colour)
	print " " * (result_col - cursor_pos), "[ %s ]" % msg
	cursor_pos = 0

def error(msg):
	result(msg, 'RED')

def error_new_line(msg):
	if cursor_pos:
		error('ERROR')
	print highlight(msg, 'RED')

def highlight(msg, colour):
	return curses.tparm(set_fg, COLOURS[colour]) + msg + curses.tparm(normal)
