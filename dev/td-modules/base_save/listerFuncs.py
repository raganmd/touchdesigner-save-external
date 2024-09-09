import saveUtils
POP_MENU = parent.save.op('popMenu')


def parse_col(info: dict) -> None:
    col_name_func_map = {
        "save": save_tox,
        "view": view_tox,
        "show_file": open_folder,
        "reload": reinit_tox,
        "reload_ext": reinit_extensions
    }

    row = info.get('row')
    col_name = info.get('colName')

    # skip clicks that are not on a valid row
    if row != -1:
        # find function by column name
        func = col_name_func_map.get(col_name)

        # handle any possible None objects
        if func != None:
            # call function and pass the info object
            func(info)
        else:
            pass
        pass

    else:
        pass


def parse_right_click(info: dict) -> None:
    """
    """
    row = info.get('row')
    col_name = info.get('colName')

    if row != -1 and col_name == 'version':
        def pop_cb(cb_info: dict):
            pop_menu_selection(cb_info)

        POP_MENU.Open(callback=pop_cb, callbackDetails=info)
        pass

    else:
        pass


def pop_menu_selection(info: dict) -> None:
    """Runs based on the pop menu selection
    """
    current_tox = _get_op_from_tox_path(info.get("details"))
    current_version = current_tox.par['Toxversion'].eval()
    version_split = current_version.split('.')
    split_ints = [int(each) for each in version_split]
    index = info.get("index")

    if index == 0:
        version_update = f'{split_ints[0]+1}.0.0'

    elif index == 1:
        version_update = f'{split_ints[0]}.{split_ints[1]+1}.0'
    else:
        version_update = ''
        pass

    parent.save.Save_over_tox(current_tox, version_update)


def _get_op_from_tox_path(info: dict) -> callable:
    return op(info.get('rowData').get('toxPath'))


def save_tox(info: dict) -> None:
    parent.save.Save_over_tox(_get_op_from_tox_path(info))


def view_tox(info: dict) -> None:
    """Moves current pane to view the contents of the tox / COMP
    """
    saveUtils.Open_network_location(_get_op_from_tox_path(info))


def open_folder(info: dict) -> None:
    """Opens containing directory for a tox file
    """
    target_op = _get_op_from_tox_path(info)
    ui.viewFile(target_op.par.externaltox.eval(), showInFolder=True)


def reinit_tox(info: dict) -> None:
    """Reloads an entire TOX
    """
    target_op = _get_op_from_tox_path(info)
    target_op.par.reinitnet.pulse()


def reinit_extensions(info: dict) -> None:
    """Reinitialize the extension for an COMP
    """
    target_op = _get_op_from_tox_path(info)
    target_op.par.reinitextensions.pulse()
