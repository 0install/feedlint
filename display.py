import sys
import os

if os.name == 'nt':
	n_cols = 80
	set_fg = None
	normal = None
else:
	import curses
	curses.setupterm()

	n_cols = curses.tigetnum('cols') or 80
	set_fg = curses.tigetstr('setf') or None
	normal = curses.tigetstr('sgr0') or None

cursor_pos = 0

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

def error_new_line(msg, colour = 'RED'):
	if cursor_pos:
		error('ERROR')
	print highlight(msg, colour)

def highlight(msg, colour):
	if set_fg and normal:
		return curses.tparm(set_fg, COLOURS[colour]) + msg + curses.tparm(normal)
	else:
		return msg
