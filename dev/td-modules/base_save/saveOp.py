"""
SudoMagic | sudomagic.com
Authors   | Matthew Ragan, Ian Shelanskey
Contact   | contact@sudomagic.com
"""

# td python mods
import saveUtils


class SaveOpManager:
    """SaveOpManager
    """

    def __init__(self, ext_ops_DAT) -> None:
        """TODO: complete doc strings

        Args
        ---------------
        self (`callable`)
        > Class instance

        Returns
        ---------------
        None      
        """
        self.Ext_ops_DAT = ext_ops_DAT
        self.External_ops: list = []
        self._build_op_list()

    def add_save_op(self, td_operator: callable) -> None:
        """TODO: complete doc strings

        Args
        ---------------
        self (`callable`)
        > Class instance

        Returns
        ---------------
        None      
        """
        new_save_op: SaveOp = SaveOp(td_operator)
        self.External_ops.append(new_save_op)
        pass

    def check_hash_status(self) -> None:
        """TODO: complete doc strings

        Args
        ---------------
        self (`callable`)
        > Class instance

        Returns
        ---------------
        None      
        """
        pass

    @property
    def external_ops(self) -> None:
        """Returns a list of all external comps
        """
        children = root.findChildren(type=COMP)
        external_ops = [
            eachChild for eachChild in children if eachChild.par.externaltox != '']
        return external_ops

    @property
    def dirty_ops(self) -> None:
        """TODO: complete doc strings

        Args
        ---------------
        self (`callable`)
        > Class instance

        Returns
        ---------------
        None      
        """

        dirty_op_list = [
            each_ext_op for each_ext_op in self.External_ops if each_ext_op.is_dirty]
        return dirty_op_list

    def _build_op_list(self) -> None:
        """TODO: complete doc strings

        Args
        ---------------
        self (`callable`)
        > Class instance

        Returns
        ---------------
        None      
        """

        externals = self.external_ops
        external_list = []

        for each in externals:
            new_save_op: SaveOp = SaveOp(each)
            self.External_ops.append(new_save_op)

    def Check_external_ops(self) -> None:
        all_externals = self.external_ops
        tracked_ids = [each.id for each in self.External_ops]
        for each_external in all_externals:
            if each_external.id in tracked_ids:
                pass
            else:
                self.add_save_op(each_external)
                print(f"adding new tracked external op {each_external}")

        # force cook DAT with list of all ops
        self.Ext_ops_DAT.cook(force=True)

    def Dirty_check(self) -> None:
        self.Check_external_ops()
        for each_index, each_op in enumerate(self.External_ops):
            if each_op.td_op.valid:
                each_op: SaveOp = each_op
                each_op.dirty_check()
            else:
                self.External_ops.pop(each_index)

    def Ignore_current_dirty_state(self, target_op_id: int) -> None:
        target_op: SaveOp = self.get_save_op_by_id(target_op_id)
        target_op.op_hash = saveUtils.gen_hash_from_op(target_op.td_op)
        target_op.is_dirty = False

    def get_save_op_by_id(self, op_id: int) -> callable:
        op_by_id = None

        for each_op in self.External_ops:
            each_op: SaveOp = each_op
            if each_op.id == op_id:
                op_by_id = each_op
                break

        return each_op

    def Update_save_op_by_path(self, path: str, value: bool):
        """TODO: complete doc strings

        Args
        ---------------
        self (`callable`)
        > Class instance

        Returns
        ---------------
        None      
        """
        # for each_save_op_index, each_save_op in enumerate(self.External_ops):
        #     each_save_op: SaveOp = each_save_op
        #     if each_save_op.td_op.path == path:
        #         each_save_op.is_dirty = value
        #         each_save_op.op_hash = saveUtils.gen_hash_from_op(op(path))
        #         break
        #     else:
        #         pass
        pass


class SaveOp:
    """SaveOpManager
    """

    def __init__(self, td_operator: callable) -> None:
        """Class Object Init

            Notes
            ---------

            Args
            ---------
            self (`callable`)
            > Class instance

            td_operator (`callable`)
            > A TouchDesigner operator this save_op is built from

            op_hash (`callable`)
            > A has constructed from the state of the external op

            Returns
            ---------
            None
        """
        self._ext_op = td_operator
        self._is_dirty = tdu.Dependency(False)
        self.id = td_operator.id
        return

    def dirty_check(self) -> None:
        """TODO: complete doc strings

        Args
        ---------------
        self (`callable`)
        > Class instance

        Returns
        ---------------
        None      
        """

        old_hash = self._op_hash
        new_hash = saveUtils.gen_hash_from_op(self._ext_op)
        if new_hash != old_hash:
            self.is_dirty = True
            debug(f"{self._ext_op} is dirty")
        else:
            self.is_dirty = False

    @property
    def op_hash(self) -> callable:
        return self._op_hash

    @op_hash.setter
    def op_hash(self, new_hash: callable) -> None:
        self._op_hash = new_hash

    @property
    def td_op(self) -> callable:
        return self._ext_op

    @property
    def is_dirty(self) -> bool:
        """is_dirty getter

        Returns tdu.Dependency value

        Args
        ---------------
        self (`callable`)
        > Class instance

        state (`bool`)
        > The new state for the saveOp

        Returns
        ---------------
        is_dirty (`bool`)
        > The dirty state as a boolean      
        """
        return self._is_dirty.val

    @is_dirty.setter
    def is_dirty(self, state: bool):
        """is_dirty setter

        Updates tdu.Dependency value

        Args
        ---------------
        self (`callable`)
        > Class instance

        state (`bool`)
        > The new state for the saveOp

        Returns
        ---------------
        None      
        """
        self._is_dirty.val = state

    @property
    def last_saved(self) -> callable:
        if self._ext_op.par['Lastsaved']:
            return self._ext_op.par.Lastsaved
        else:
            return None

    @property
    def version(self) -> callable:
        if self._ext_op.par['Toxversion']:
            return self._ext_op.par.Toxversion
        else:
            return None

    @property
    def ext_path(self) -> callable:
        return self._ext_op.par.Externaltox

    @property
    def tags(self) -> callable:
        if 'submodule' in self._ext_op.tags:
            return 'submodule'
        elif 'devTool' in self._ext_op.tags:
            return 'DevTool'
        else:
            return ''
