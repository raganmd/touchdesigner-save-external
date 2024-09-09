"""
SudoMagic | sudomagic.com
Authors   | Matthew Ragan, Ian Shelanskey
Contact   | contact@sudomagic.com
"""

# pure python
import os

# td python mods
import saveOp
import saveUtils


class ExternalFiles:
    """
        The ExternalFiles class is used to handle working with both 
        externalizing files, as well as ingesting files that were previously 
        externalized. This helps to minimize the amount of manual work that 
        might need to otherwise be use for handling external files. 
    """
    FLASH_DURATION = 14
    UNLOCK_TAGS = [
        "unlockOnSave"
    ]

    def __init__(self, my_op: callable) -> None:
        """Stands in place of an execute dat - ensures all elements start-up 
        correctly

        Notes
        ---------

        Args
        ---------
        myOp (touchDesignerOperator):
        > the operator that is loading the current extension

        Returns
        ---------
        none		
        """

        self.my_op = my_op
        self._log_label = "--> SAVE COMP |"
        self.Defaultcolor = self.my_op.parGroup.Defaultcolor
        self.op_none_color = (0.5450000166893005,
                              0.5450000166893005,
                              0.5450000166893005)
        self.Ext_ops = op('table_all_external_ops')

        self._ops_manager = saveOp.SaveOpManager()

        init_msg = f"Start up and Init at {absTime.frame}"

        self.Colors_map = self._colors_map()
        self.Tag_to_color_map = self._tag_to_color_map()
        self.Title_text_to_tag_map = self._title_text_to_tag_map()

        self.Logtotextport(init_msg)

        return

    def _colors_map(self) -> dict:
        """A map of colors
        Structure of this dict is:
            Classification (TouchDesigner | Python | Comments)
            -> Color type (e.g. python_extension or comment_note)
                -> tags and colors for type

        """
        colors_map = {
            "TouchDesigner": {
                "external_op": {
                    "color": self.my_op.parGroup.Externalop,
                    "tags": []
                }
            },
            "Python":  {
                "default": {
                    "color": self.my_op.parGroup.Pythondefault,
                    "tags": []
                },
                "python_extension": {
                    "color": self.my_op.parGroup.Pythonextension,
                    "tags": ["EXT"]
                },
                "python_module": {
                    "color": self.my_op.parGroup.Pythonmodule,
                    "tags": ["MOD"]
                }
            },
            "Comments": {
                "bug": {
                    "color": self.my_op.parGroup.Commentbug,
                    "tags": ["comment_bug"],
                    "title_text": "#BUG"
                },
                "hack": {
                    "color": self.my_op.parGroup.Commenthack,
                    "tags": ["comment_hack"],
                    "title_text": "#HACK"
                },
                "fix": {
                    "color": self.my_op.parGroup.Commentfix,
                    "tags": ["comment_fix"],
                    "title_text": "#FIXME"
                },
                "note": {
                    "color": self.my_op.parGroup.Commentnote,
                    "tags": ["comment_note"],
                    "title_text": "#NOTE"
                }
            }
        }
        return colors_map

    def _tag_to_color_map(self) -> dict:
        """Builds a map of colors by tag
        """
        tag_to_color_map = {}
        for classification, classificaion_vals in self.Colors_map.items():
            for each_type, type_vals in classificaion_vals.items():
                for each_tag in type_vals.get("tags"):
                    tag_to_color_map[each_tag] = type_vals.get("color")
        return tag_to_color_map

    def _title_text_to_tag_map(self) -> dict:
        """Builds a map of colors by title_text
        """
        title_text_to_tag_map = {}
        comments_dict = self.Colors_map.get("Comments")
        for each_type, type_vals in comments_dict.items():
            text_key = type_vals.get("title_text")
            title_text_to_tag_map[text_key] = type_vals.get("tags")[0]
        return title_text_to_tag_map

    @property
    def Ops_manager(self) -> callable:
        return self._ops_manager

    @property
    def get_current_location(self) -> callable:
        return ui.panes.current.owner

    def Prompt_to_save(self) -> None:
        """The method used to save an external TOX to file

        Notes
        ---------

        Args
        ---------
        current_loc (str):
        > the operator that's related to the currently focused 
        > pane object. This is required to ensure that we correctly
        > grab the appropriate COMP and check to see if needs to be saved

        Returns
        ---------
        none		
        """
        current_loc = self.get_current_location

        external_op_color = self.Colors_map.get(
            "TouchDesigner").get("external_op").get("color")
        msg_box_title = "TOX Save"
        msg_box_msg = "Replacing External\n\nYou are about to overwrite an exnteral TOX"
        msg_box_buttons = ["Cancel", "Continue"]

        sav_msg_box_title = "Externalize Tox"
        sav_msg_box_msg = "This TOX is not yet externalized\n\nWould you like to externalize this TOX?"
        sav_msg_box_buttons = ["No", "Yes"]

        save_msg_buttons_parent_too = [
            "No", "This COMP Only", "This COMP and the Parent"]

        # check if location is the root of the project
        if current_loc == '/':
            # skip if we're at the root of the project
            pass

        else:
            # if we're not at the root of the project

            # check if external
            if current_loc.par.externaltox != '':
                confirmation = ui.messageBox(
                    msg_box_title, msg_box_msg,
                    buttons=msg_box_buttons)

                if confirmation:

                    # save external file
                    self.Save_over_tox(current_loc)

                else:
                    # if the user presses "cancel" we pass
                    pass

            # in this case we are not external, so let's ask if we want to
            # externalize the file
            else:

                # check if the parent is externalized
                if current_loc.parent().par.externaltox != '':
                    save_ext = ui.messageBox(
                        sav_msg_box_title,
                        sav_msg_box_msg,
                        buttons=save_msg_buttons_parent_too)

                    # save this comp only
                    if save_ext == 1:
                        self.Save_tox(current_loc)

                    # save this comp and the parent
                    elif save_ext == 2:
                        self.Save_tox(current_loc)
                        self.Logtotextport("save this tox")

                        # save parent() COMP
                        self.Save_over_tox(current_loc.parent())
                        self.Logtotextport("Save the parent too!")

                    # user selected 'No'
                    else:
                        pass

                # the parent is not external, so let's ask about externalizing
                # the tox
                else:
                    save_ext = ui.messageBox(
                        sav_msg_box_title,
                        sav_msg_box_msg,
                        buttons=sav_msg_box_buttons)

                    if save_ext:
                        self.Save_tox(current_loc)

                    else:
                        # the user selected "No"
                        pass

        return

    def Save_over_tox(self, current_loc):
        # update custom pars
        self.update_version_pars(current_loc)
        self.update_save_time(current_loc)

        self._save_tox(current_loc)
        return

    def Save_tox(self, current_loc):
        ext_color = self.Colors_map.get(
            "TouchDesigner").get("external_op").get("color")

        # ask user for a save location
        save_loc = ui.chooseFolder(title="TOX Location", start=project.folder)

        # construct a relative path and relative loaction for our elements
        rel_path = tdu.collapsePath(save_loc)

        # check to see if the location is at the root of the project folder structure
        if rel_path == "$TOUCH":
            rel_loc = '{new_tox}/{new_tox}.tox'.format(
                new_tox=current_loc.name)

        # save path is not in the root of the project
        else:
            rel_loc = '{new_module}/{new_tox}/{new_tox}.tox'.format(
                new_module=rel_path, new_tox=current_loc.name)

        # create path and directory in the OS
        new_path = '{selected_path}/{new_module}'.format(
            selected_path=save_loc, new_module=current_loc.name)

        try:
            os.mkdir(new_path)
            valid_external_path = True
        except:
            self.alert_failed_dir_creation(
                new_path=new_path, current_loc=current_loc)
            valid_external_path = False

        if valid_external_path:
            # format our tox path
            tox_path = '{dir_path}/{tox}.tox'.format(
                dir_path=new_path, tox=current_loc.name)

            # setup our module correctly
            current_loc.par.externaltox = '' if current_loc.par['Sudotool'] else rel_loc
            current_loc.par.savebackup = False

            # set color for COMP
            current_loc.color = self.op_none_color if current_loc.par['Sudotool'] else (
                ext_color[0], ext_color[1], ext_color[2])

            # setup about page
            self.custom_page_setup(current_loc)

            # private save method
            self._save_tox(current_loc)

            # track new SaveOp
            self._ops_manager.Check_external_ops()

        else:
            pass

        return

    def _save_tox(self, current_loc: str) -> None:
        ext_color = self.Colors_map.get(
            "TouchDesigner").get("external_op").get("color")
        external_path = current_loc.par.externaltox

        # Run pre-save event
        self.preToxSave(current_loc)

        # save tox
        current_loc.save(external_path)

        # Run post-save event
        self.postToxSave(current_loc)

        # set color for COMP
        current_loc.color = (ext_color[0], ext_color[1], ext_color[2])

        # flash color
        worksheet_color = self.my_op.parGroup["Bgcolor"]
        saveUtils.flash_bg(worksheet_color, ExternalFiles.FLASH_DURATION)

        # set external file colors
        self.Set_external_file_colors()

        # set comment colors
        self.Set_annotate_colors()

        # update hash_list
        self._ops_manager.Update_save_op_by_path(
            current_loc,
            False)

        # create and print log message
        log_msg = "{} saved to {}/{}".format(
            current_loc,
            project.folder,
            external_path)

        self.Logtotextport(log_msg)

    def preToxSave(self, tox):
        """ pre tox save event handling """

        for child in tox.findChildren(tags=['unlockOnSave']):
            child.lock = False
        return

    def postToxSave(self, tox):
        """ post tox save event handling """
        for child in tox.findChildren(tags=['unlockOnSave']):
            child.lock = True
        return

    def alert_failed_dir_creation(self, **kwargs):
        op.TDResources.op('popDialog').Open(
            title="OVERWRITE WARNING",
            text="""It looks like there is an existing
TOX in this directory. 

Please check your to make sure
this TOX does not already exist.
""",
            buttons=["Cancel", "Replace"],
            escButton=1,
            callback=self.dialogChoice,
            details=kwargs
        )

    def dialogChoice(self, info):
        button_selection = info.get('button')

        if button_selection == 'Cancel':
            pass

        else:
            current_loc = info.get('details').get('current_loc')
            new_path = info.get('details').get('new_path')

            # format our tox path
            tox_path = '{dir_path}/{tox}.tox'.format(
                dir_path=new_path, tox=current_loc.name)

            # update custom pars
            self.update_version_pars(current_loc)

            # save our tox
            current_loc.save(tox_path)

            # flash color
            self.Flash_bg("Bgcolor")

            # create and print log message
            log_msg = "{} saved to {}/{}".format(
                current_loc,
                project.folder,
                tox_path)
            self.Logtotextport(log_msg)

    def update_custom_str_par(self, targetOp, par, value, par_label="Temp"):
        if targetOp.par[par] != None:
            targetOp.par[par] = value
        else:
            about_page = targetOp.appendCustomPage("About")
            about_page.appendStr(par, label=par_label)
            targetOp.par[par] = value
            targetOp.par[par].readOnly = True

    def update_version_pars(self, target_op: callable) -> None:
        if target_op.par['Toxversion'] == None:
            self.update_custom_str_par(
                target_op, "Toxversion", "1.0.0", "Tox Version")
        else:
            new_patch_version = self._patch_update(target_op)
            self.update_custom_str_par(
                target_op, 'Toxversion', new_patch_version)
        self.update_custom_str_par(target_op, "Tdversion", app.version)
        self.update_custom_str_par(target_op, "Tdbuild", app.build)

    def _patch_update(self, target_op: callable) -> str:
        patch_str = target_op.par.Toxversion.eval()
        split_str_default = [1, 0, 0]
        if len(patch_str.split('.')) > 1:
            try:
                split_str = patch_str.split('.')
            except:
                split_str = split_str_default
        else:
            split_str = split_str_default

        return f"{split_str[0]}.{split_str[1]}.{int(split_str[2])+1}"

    def update_save_time(self, target_op: callable) -> None:
        # add par and set time
        if target_op.par['Lastsaved'] == None:
            self.update_custom_str_par(
                target_op,
                "Lastsaved",
                saveUtils.current_save_time(),
                "Last Saved")

        # update time
        else:
            self.update_custom_str_par(
                target_op,
                "Lastsaved",
                saveUtils.current_save_time(),
                "Last Saved")

    def custom_page_setup(self, target_op):
        self.update_custom_str_par(
            target_op,
            "Tdversion",
            app.version,
            "TD Version")
        self.update_custom_str_par(
            target_op,
            "Tdbuild",
            app.build,
            "TD Build")
        self.update_custom_str_par(
            target_op,
            "Toxversion",
            "1.0.0",
            "Tox Version")
        self.update_custom_str_par(
            target_op,
            "Lastsaved",
            saveUtils.current_save_time(),
            "Last Saved")

    def Logtotextport(self, logMsg):
        ui.status = f"{self._log_label} {logMsg}"
        if parent().par.Logtotextport:
            print(f"{self._log_label} {logMsg}")
        else:
            pass
        return

    def Set_ext_tox_colors(self):
        externalChildren = saveUtils.find_external_ops()
        colors = self.Colors_map.get(
            "TouchDesigner").get("external_op").get("color")
        for eachOp in externalChildren:
            eachOp.color = (colors[0], colors[1], colors[2])
        pass

    def Set_external_file_colors(self):
        """Sets colors for external files
        """

        external_dats = saveUtils.find_all_dats()
        default_color = self.Colors_map.get(
            "Python").get("default").get("color")

        for eachDat in external_dats:
            dat_color = default_color
            for each_tag in eachDat.tags:
                if each_tag in self.Tag_to_color_map.keys():
                    if self.Tag_to_color_map.get(each_tag) != None:
                        dat_color = self.Tag_to_color_map.get(each_tag)
            eachDat.color = dat_color
        pass

    def Set_annotate_colors(self):
        network_comments = saveUtils.find_all_comments()

        # update tag on annotates
        for each_new_comment in network_comments:
            title_text = each_new_comment.par.Titletext.eval()
            first_word = title_text.split(" ")[0]
            if first_word in self.Title_text_to_tag_map.keys():
                target_tag = self.Title_text_to_tag_map.get(first_word)
                each_new_comment.tags.add(target_tag)

        # set color by tag
        for eachComment in network_comments:
            for each_tag in eachComment.tags:
                if each_tag in self.Tag_to_color_map.keys():
                    if self.Tag_to_color_map.get(each_tag) != None:
                        eachComment.color = self.Tag_to_color_map.get(each_tag)

    def Open_network_location(self, network_location: str):
        """ Moves network to save location
        """
        ui.panes.current.owner = network_location
        ui.panes.current.home()

    def Ignore_current_changes(self, op_id: int):
        self._ops_manager.Ignore_current_dirty_state(op_id)

    def Open_floating_external_tox_window(self) -> None:
        """Opens window for tox files
        """
        # run dirty check
        # self._ops_manager.Dirty_check()
        # force cook op to see current status
        self.my_op.op('script1').cook(force=True)
        # open window for external tox files
        parent.save.op('window1').par.winopen.pulse()

    def Keyboard_input(self, shortcut):
        """Keyboard input handler
        """
        shortcut_lookup = {
            'ctrl.w': self.Prompt_to_save,
            'ctrl.shift.w': self.Open_floating_external_tox_window
        }

        func = shortcut_lookup.get(shortcut)

        try:
            func()

        except Exception as e:
            self.Logtotextport(e)
