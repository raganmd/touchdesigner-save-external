"""
SudoMagic | sudomagic.com
Authors   | Matthew Ragan, Ian Shelanskey
Contact   | contact@sudomagic.com
"""

# pure python
import hashlib
from datetime import datetime

EXCLUDE_OPS = [
    "eval",
    "keyboardin",
    "opfind",
    "folder",
    "examine",
    "select",
    "udpout",
    "udpin",
    "fifo",
    "script",
    "null",
    "info"]

DEFAULT_WORKSHEET_COLOR = (0.1, 0.105, .12)


def gen_hash_from_op(td_operator: callable) -> callable:
    """TODO: complete doc strings

    Args
    ---------------
    td_operator (`TD_Operator`)
    > TouchDesigner operator to generate hash from

    Returns
    ---------------
    op_hash (`callable`)
    > Hash generated from TouchDesigner operator's data    
    """

    allPars = []

    # find all non-external children of an operator
    all_children = get_non_external_children(td_operator)

    # generate a dict of elements that may have changed
    for each_child in all_children:
        child_dict = {}
        child_dict['nodeX'] = each_child.nodeX
        child_dict['nodeY'] = each_child.nodeY
        child_dict['nodeWidth'] = each_child.nodeWidth
        child_dict['nodeHeight'] = each_child.nodeHeight
        child_dict['color'] = each_child.color
        child_dict['path'] = each_child.path
        child_dict['pars_dict'] = {}

        for each_par in each_child.pars():
            if each_par.mode != ParMode.EXPRESSION:
                if each_par.page == "About":
                    pass
                else:
                    child_dict['pars_dict'][each_par.name] = each_par.val
                    allPars.append(child_dict)

    # generate a hash of changed elements
    op_hash = allPars
    return op_hash


def find_all_dats() -> list:
    """Returns a list of all external dats
    """
    external_dats = []
    exclude_list = EXCLUDE_OPS

    for eachOp in root.findChildren(type=DAT):
        if eachOp.type in exclude_list:
            pass

        else:
            if eachOp.par['file'] != '':
                external_dats.append(eachOp)
            else:
                pass
    return external_dats


def find_all_comments() -> list:
    comment_ops = []
    for eachOp in root.findChildren(type=annotateCOMP):
        comment_ops.append(eachOp)
    return comment_ops


def find_external_ops():
    """Returns a list of all external comps
    """
    children = root.findChildren(type=COMP)
    external_ops = [
        eachChild for eachChild in children if eachChild.par.externaltox != '']
    return external_ops


def get_non_external_children(target_op) -> list:

    # look first at only one layer deep
    immediate_children = target_op.findChildren(depth=1)
    non_ext_children = []

    # add ops that are not external to our list
    for each_immediate_child in immediate_children:
        if each_immediate_child.family == "COMP":
            if each_immediate_child.par.externaltox.eval() != '':
                pass
            else:
                non_ext_children.append(each_immediate_child)
        else:
            non_ext_children.append(each_immediate_child)

    # for each non-external op, find their children
    for each_child in non_ext_children:
        if each_child.family == "COMP":
            grand_children = each_child.findChildren(depth=1)

            non_ext_children.extend(grand_children)
        else:
            pass

    return non_ext_children


def ext_parent(target_op) -> callable:
    ext_parent = None
    parent_paths = []
    parent_paths_parts = target_op.parent().path.split('/')
    last_path = ''

    for each_index in parent_paths_parts[1:]:
        last_path = f"{last_path}/{each_index}"
        parent_paths.append(last_path)

    parent_paths.reverse()

    for each_path in parent_paths:
        if op(each_path).par.externaltox != '':
            ext_parent = op(each_path)
            break
        else:
            continue

    return ext_parent


def current_save_time() -> str:
    today = datetime.now()
    time_str = f"{today.year}-{today.month}-{today.day} {today.hour:02d}:{today.minute:02d}:{today.second:02d}"
    return time_str


def flash_bg(flash_color: tuple, duration: int) -> None:
    """ Flashes the background of TouchDesigner

    Used to flash the background of the TD network. 

    Notes
    ---------
    This is a simple tool to flash indicator colors in the
    background to help you have some visual confirmation that
    you have in fact externalized a file.

    Args
    ---------
    flash_color (tuple):
    > this is the string name to match against the parent's pars()
    > for to pull colors to use for changing the background

    duration (int):
    > length in frames for how long the color should replace the background

    Returns
    ---------
    none		
    """

    ui.colors['worksheet.bg'] = flash_color
    delay_script = "ui.colors['worksheet.bg'] = args[0]"

    # want to change the background color back
    run(delay_script, DEFAULT_WORKSHEET_COLOR, delayFrames=duration)

    return


def Open_network_location(network_location):
    """ Moves network to save location
    """
    ui.panes.current.owner = network_location
    ui.panes.current.home()
