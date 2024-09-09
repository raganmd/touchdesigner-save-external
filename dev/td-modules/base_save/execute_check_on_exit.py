# me - this DAT
# 
# frame - the current frame
# state - True if the timeline is paused
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

def onStart():
	return

def onCreate():
	return

def onExit():
	prompt()
	return

def onFrameStart(frame):
	return

def onFrameEnd(frame):
	return

def onPlayStateChange(state):
	return

def onDeviceChange():
	return

def onProjectPreSave():
	return

def onProjectPostSave():
	return

def findDirtyTox():
	op('table_dirty_ops').clear(keepFirstRow=True)
	children = op.Project.findChildren(type=COMP)
	for each in children:
		if each.dirty:
			op('table_dirty_ops').appendRow([each.name, each.path])

	op('window1').par.winopen.pulse()

def prompt():
	bodyCopy = '''Before you leave,
do you want to check to see if there are 
any unsaved toxes in your network?'''

	msg = ui.messageBox("Check All External Toxes", bodyCopy, buttons=["Yes", "No"])
	if msg:
		pass
	
	else:
		parent().Find_dirty_tox()