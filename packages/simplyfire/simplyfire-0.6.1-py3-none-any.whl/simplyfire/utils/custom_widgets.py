"""
Useful widgets for the UI - combines tkinter UI widgets with variables
for simpler value setting and retrieval.

Simplyfire - customizable analysis of electrophysiology data
Copyright (C) 2022 Megumi Mori
This program comes with ABSOLUTELY NO WARRANTY

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import tkinter as Tk
from tkinter import ttk

from simplyfire.utils import validation
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib as mpl
import yaml
from simplyfire import app
import os

#### values ####
entry_width = 10

class VarWidget():
    def __init__(
            self,
            parent=None,
            name=None,
            value=None,
            default=None,
            type=None,
    ):
        self.name = name
        if type is None or type == str:
            self.var = Tk.StringVar()
        elif type == int:
            self.var = Tk.IntVar()
        elif type == bool:
            self.var = Tk.BooleanVar()
        elif type == float:
            self.var = Tk.DoubleVar()
        if default is not None:
            self.default=default
        else:
            self.default = ""
        # elif name is not None:
        #     if config.default_vars.get('default_{}'.format(name), None) is not None:
        #         self.default = config.default_vars['default_{}'.format(name)]
        #     else:
        #         self.default=""
        if value is not None:
            try:
                self.var.set(value)
            except:
                pass
        # elif name is not None:
        #     if config.user_vars.get(name, None) is not None:
        #         self.var.set(config.user_vars[name])
        #     elif config.system_vars.get(name, None) is not None:
        #         self.var.set(config.system_vars[name])
        #     else:
        #         self.var.set(self.default)
        else:
            self.var.set(self.default)

        self.undo_value = self.get()

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)

    def get_default(self):
        return self.default

    def set_to_default(self):
        self.set(self.default)

    def get_widget(self):
        return self

class VarEntry(VarWidget, Tk.Entry):
    def __init__(
            self,
            parent,
            name=None,
            value=None,
            default=None,
            validate_type=None,
            width=None,
            type=None,
            **kwargs
    ):
        self.validate_type=validate_type
        VarWidget.__init__(
            self,
            parent=parent,
            name=name,
            value=value,
            default=default,
            type=type
        )
        if width is None:
            width = entry_width
        Tk.Entry.__init__(
            self,
            master=parent,
            textvariable=self.var,
            width=width,
            justify=Tk.RIGHT,
        )

        self.prev = self.get()
        self.validate_type = validate_type
        self.validate(event=None, validation_type=validate_type, undo=False)
        self.bind('<FocusOut>', lambda e, v=validate_type: self.validate(e, v), add='+')
        self.bind('<Return>', lambda e, v=validate_type: self.validate(e, v), add="+")

    def revert(self):
        if validation.validate(self.validate_type, self.prev):
            self.set(self.prev)
        else:
            self.set_to_default()
            self.prev = self.default

    def set(self, value=""):
        # cannot use Tk.StringVar.set() due to validatecommand conflict
        self.delete(0, len(self.var.get()))
        self.insert(0, value)

    def validate(self, event, validation_type, undo=True):
        value = self.get()
        if validation.validate(validation_type, self.var.get()):
            self.undo_value = self.prev
            # if value != self.prev and undo:
            #     interface.add_undo([lambda v=self.prev:self.undo(v)])
            self.prev = value
            return True
        elif validation_type == 'int':
            try:
                new_value = str(int(float(value)))
                # self.set(new_value)
                # if new_value != self.prev and undo:
                #     interface.add_undo([lambda v=self.prev:self.undo(v)])
                self.prev = new_value
                return True
            except:
                self.revert()
                return False
        else:
            self.revert()
            return False

    def get(self):
        # if validation.is_na(self.var.get()):
        #     return None
        # return validation.convert(self.validate_type, self.var.get())
        return self.var.get()
    def undo(self, value):
        self.set(value)
        self.focus_set()
        self.prev = value

class VarOptionmenu(VarWidget, ttk.OptionMenu):
    def __init__(
            self,
            parent,
            name=None,
            value=None,
            default="",
            options=None,
            command=None,
            type=None,
            **kwargs
    ):
        VarWidget.__init__(
            self,
            parent=parent,
            name=name,
            value=value,
            default=default,
            type=type
        )
        if options is None:
            options = []
        if value is None:
            value = default
        self.command = command
        ttk.OptionMenu.__init__(
            self,
            parent,
            self.var,
            value,
            *options,
            command=self.command,
            **kwargs
        )

    def command_undo(self, e=None):
        if self.undo_value == self.get():
            return None
        try:
            self.set_undo()
            self.command(e)
        except Exception:
            pass

    def clear_options(self):
        self['menu'].delete(0, 'end')

    def add_command(self, label="", command=None, **kwargs):
        self['menu'].add_command(label=label, command=command, **kwargs)

    def set(self, val):
        if val != self.get():
            self.undo_value = self.get()
            self.var.set(val)


class VarCheckbutton(VarWidget, ttk.Checkbutton):
    def __init__(
            self,
            parent,
            name=None,
            value=None,
            default=None,
            command=None,
            type=None,
            **kwargs
    ):
        VarWidget.__init__(
            self,
            name=name,
            parent=parent,
            value=value,
            default=default,
            type=type
        )
        ttk.Checkbutton.__init__(
            self,
            master=parent,
            variable=self.var,
            command=command,
            **kwargs
        )
    #     self.var.trace_add('write', self.toggle)
    #
    # def toggle(self, var=None, val=None, e=None):
    #     interface.add_undo([
    #         self.invoke,
    #         self.interface.undo_stack.pop
    #     ])

class VarText(VarWidget, Tk.Text):
    def __init__(
            self,
            parent,
            name="",
            value="",
            default="",
            lock=False,
            type=None,
            **kwargs
    ):
        VarWidget.__init__(
            self,
            parent=parent,
            name=name,
            value=value,
            default=default,
            type=type,
        )
        Tk.Text.__init__(
            self,
            master=parent,
            **kwargs
        )
        # print(self.get())
        self.lock = lock
        if lock:
            Tk.Text.configure(self, state='disabled')
        self.var.set(value)


    def set(self, value):
        disable = False
        if self['state'] == 'disabled':
            disable = True
            self.config(state='normal')
        self.delete(1.0, Tk.END)
        # self.insert(1.0, value)
        self.var.set(value)
        Tk.Text.insert(self, 1.0, value)
        if disable:
            self.config(state='disabled')

    def clear(self):
        disable = False
        if self['state'] == 'disabled':
            disable=True
            self.config(state='normal')
        self.delete(1.0, Tk.END)
        self.var.set("")
        if disable:
            self.config(state='disabled')

    def insert(self, text):
        disable = False
        if self['state'] == 'disabled':
            disable = True
            self.config(state='normal')
        Tk.Text.insert(self, Tk.END, text)
        self.var.set(self.var.get()+text)
        if disable:
            self.config(state='disabled')

    # def get(self):
    #     return Tk.Text.get(self, 1.0, Tk.END)

class VarScale(VarWidget, ttk.Scale):
    def __init__(
            self,
            parent,
            value=0,
            default=0,
            from_=100,
            to=100,
            orient=Tk.VERTICAL,
            command=None,
            type=float,
            **kwargs
    ):
        VarWidget.__init__(
            self,
            parent=parent,
            value=value,
            default=default,
            type=type
        )
        ttk.Scale.__init__(
            self,
            master=parent,
            variable=self.var,
            from_=from_,
            to=to,
            orient=orient,
            command=command,
            **kwargs
        )

class VarLabel(VarWidget, ttk.Label):
    def __init__(
            self,
            parent,
            value="",
            default="",
            **kwargs
    ):
        VarWidget.__init__(
            self,
            parent=parent,
            value=value,
            default=default
        )
        ttk.Label.__init__(
            self,
            master=parent,
            text=value
        )

    def set(self, value):
        self.config(text = value)


class NavigationToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, parent):
        # self.toolitems = [t for t in self.toolitems if t[0] in ('Pan', 'Zoom', 'Save')]
        self.toolitems = (
            ('Pan', '', 'move', 'pan'),
            # (None,None,None,None),
            ('Zoom', '', 'zoom_to_rect', 'zoom'),
            # (None,None,None,None),
            ('Save', '', 'filesave', 'save_figure')
        )
        NavigationToolbar2Tk.__init__(self, canvas, parent, pack_toolbar=False)

        # self.add_toolitem(name='test', position=-1, image='img/arrow.png')

        # self.test_button = self._custom_button('test', command=self.test)

        self.defaultextension = '.png'

    def _custom_button(self, text, command, **kwargs):
        button = Tk.Button(master=self, text=text, padx=2, pady=2, command=command, **kwargs)
        button.pack(side = Tk.LEFT, fill='y')
        return button

    def pan(self):
        NavigationToolbar2Tk.pan(self)
        if self.mode == 'pan/zoom':
            self.canvas.get_tk_widget().config(cursor='fleur')
        else:
            self.canvas.get_tk_widget().config(cursor='arrow')

    def zoom(self):
        NavigationToolbar2Tk.zoom(self)
        if self.mode == 'zoom rect':
            self.canvas.get_tk_widget().config(cursor='cross')
        else:
            self.canvas.get_tk_widget().config(cursor='arrow')
    def test(self, e=None):
        if self.mode == 'test':
            self.mode = None
        else:
            self.mode = 'test'

        self._update_buttons_checked() ################ this is what you need to update the checked buttons in toolbar
        # self.test_button.config(relief='sunken')

        self.canvas.widgetlock(self)

    def save_figure(self, *args):
        #overwrite nagive save_figure function
        filetypes = self.canvas.get_supported_filetypes().copy()
        default_filetype = self.canvas.get_default_filetype()

        # Tk doesn't provide a way to choose a default filetype,
        # so we just have to put it first
        default_filetype_name = filetypes.pop(default_filetype)
        sorted_filetypes = ([(default_filetype, default_filetype_name)]
                            + sorted(filetypes.items()))
        tk_filetypes = [(name, '*.%s' % ext) for ext, name in sorted_filetypes]

        # adding a default extension seems to break the
        # asksaveasfilename dialog when you choose various save types
        # from the dropdown.  Passing in the empty string seems to
        # work - JDH!
        # defaultextension = self.canvas.get_default_filetype()
        defaultextension = ''
        # initialdir = os.path.expanduser(mpl.rcParams['savefig.directory'])
        try:
            initialdir = app.interface.recordings[0].filedir
            initialfile = app.interface.recordings[0].filename+'_image'
        except:
            initialdir = os.path.expanduser(mpl.rcParams['savefig.directory'])
            initialfile = os.path.splitext(self.canvas.get_default_filename())[0]
        fname = Tk.filedialog.asksaveasfilename(
            master=self.canvas.get_tk_widget().master,
            title='Save the figure',
            filetypes=tk_filetypes,
            defaultextension=defaultextension,
            initialdir=initialdir,
            initialfile=initialfile,
            )

        if fname in ["", ()]:
            return

        self.defaultextension = os.path.splitext(fname)[1]
        # Save dir for next time, unless empty str (i.e., use cwd).
        if initialdir != "":
            mpl.rcParams['savefig.directory'] = (
                os.path.dirname(str(fname)))
        try:
            # This method will handle the delegation to the correct type
            self.canvas.figure.set_linewidth(0)
            self.canvas.figure.savefig(fname, transparent=True)
            self.canvas.figure.set_linewidth(1)
        except Exception as e:
            Tk.messagebox.showerror("Error saving file", str(e))


class PseudoFrame():
    """
    this class is used to store information similarly to ScrollableOptionFrame
    """
    def __init__(self):
        self.data = {}

    def get_value(self, key):
        return self.data[key]

    def set_value(self, key, value):
        self.data[key] = value

    def safe_dump_vars(self):
        return yaml.safe_dump(self.data)

class DataTable(Tk.Frame):
    def __init__(self, parent, bindings=None):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.table = ttk.Treeview(self)
        self.table.grid(column=0, row=0, sticky='news')

        self.vsb = ttk.Scrollbar(self, orient=Tk.VERTICAL, command=self.table.yview)
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.table.configure(yscrollcommand=self.vsb.set)

        hsb = ttk.Scrollbar(self, orient=Tk.HORIZONTAL, command=self.table.xview)
        hsb.grid(column=0, row=1, sticky='ew')
        self.table.configure(xscrollcommand=hsb.set)

        if bindings is None:
            bindings = ('copy', 'select all', 'deselect', 'delete')
        if 'copy' in bindings:
            for key in app.interpreter.get_keys('copy'):
                self.table.bind(key, self.copy, add="+")
        if 'select all' in bindings:
            for key in app.interpreter.get_keys('select_all'):
                self.table.bind(key, self.select_all, add="+")
        if 'deselect' in bindings:
            for key in app.interpreter.get_keys('deselect'):
                self.table.bind(key, self.unselect, add="+")
        if 'delete' in bindings:
            for key in app.interpreter.get_keys('delete'):
                self.table.bind(key, self.delete_selected, add="+")

        self.menu = Tk.Menu(self.table, tearoff=0)

        self.table.bind("<Button-3>", self.popup, add="+")

    def popup(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def add_menu_command(self, **kwargs):
        """
        adds a command to right-click menu
        use **kwargs for tkinter.Menu.add_command kwargs
        """
        self.menu.add_command(**kwargs)
    #     self.table.bind('<Button-3>', self.get_element)
    #
    # def get_element(self, e):
    #     print(self.table.identify_region(e.x, e.y))

    def add_menu_separator(self):
        self.menu.add_separator()


    def copy(self, event=None):
        selected = self.table.selection()
        text = ""
        for c in self.displaycolumns:
            text = f'{text}{c}\t'
        text = text[:-1] + '\n'
        if len(selected) > 0:
            for i in selected:
                data = self.table.set(i)
                for c in self.displaycolumns:
                    text = text + '{}\t'.format(data[c])
                text = text[:-1] + '\n'
        try:
            app.root.clipboard_clear()
            app.root.clipboard_append(text)
        except:
            pass
    def copy_all(self, event=None):
        items = self.table.get_children()
        text = ""
        for c in self.columns:
            text = text + '{}\t'.format(c)
        text = text + '\n'
        for i in items:
            data = self.table.set(i)
            for c in self.columns:
                text = text + '{}\t'.format(data[c])
            text = text + '\n'
        try:
            app.root.clipboard_clear()
            app.root.clipboard_append(text)
        except:
            pass

    def select_all(self, event=None):
        self.table.selection_set(self.table.get_children())

    def define_columns(self, columns, sort=True, iid_header=None, stretch=False):
        # columns should be in tuple to avoid mutation
        self.table.config(displaycolumns=())
        self.table.config(columns=columns, show='headings')
        self.table.config(displaycolumns=columns)
        self.sort=sort
        self.iid_header = iid_header
        self.columns = columns
        self.displaycolumns=columns

        if sort:
            for i, col in enumerate(columns):
                self.table.heading(i, text=col, command=lambda _col = col: self._sort(_col, False))
                self.table.column(i, stretch=stretch)
        else:
            for i, col in enumerate(columns):
                self.table.heading(i, text=col)
                self.table.column(i, stretch=stretch)

    def add_columns(self, columns):
        all_columns = [i for i in self.columns]
        for c in columns:
            if c not in all_columns:
                all_columns.append(c)
        self.define_columns(all_columns, self.sort, self.iid_header)

    def set_iid(self, iid):
        self.iid_header = iid

    def _sort(self, col, reverse):
        try:
            l = [(float(self.table.set(k, col)), k) for k in self.table.get_children('')]
        except:
            l = [(self.table.set(k, col), k) for k in self.table.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.table.move(k, "", index)
        self.table.heading(col, command = lambda _col=col: self._sort(_col, not reverse))
        try:
            self.table.see(self.table.selection()[0])
        except:
            pass

    def add(self, datadict, parent='', index='end'): # data in the form of a dict
        new_columns = [key for key in datadict if key not in self.columns]
        if new_columns:
            self.add_columns(new_columns)
        self.table.insert(parent, index, iid=datadict.get(self.iid_header, None),
                          values=[datadict.get(i, None) for i in self.columns])

    def append(self, dataframe):
        if dataframe is None:
            return None
        total = dataframe.shape[0]
        try:
            dataframe=dataframe[[k for k in self.columns if k in dataframe.columns]]
            for i, (idx, row) in enumerate(dataframe.iterrows()):
                try:
                    self.table.insert('', 'end', iid=row[self.iid_header],
                                      values=[row.get(k, None) for k in self.columns])
                    app.pb['value'] = i/total*100
                    app.pb.update()
                except Exception as e:

                    pass
        except Exception as e:

            pass
        app.pb['value']=0
        app.pb.update()
    def set_data(self, dataframe):
        self.table.selection_remove(*self.table.selection())
        self.table.delete(*self.table.get_children())
        self.append(dataframe)

    def fit_columns(self, event=None):
        if len(self.columns)>0:
            w = int((self.winfo_width()-self.vsb.winfo_width())/len(self.columns))
            for i in self.displaycolumns:
                self.table.column(i, width=w)

    def show_columns(self, columns):
        self.displaycolumns=columns
        self.table.config(displaycolumns=columns)


    def clear(self):
        self.table.selection_remove(*self.table.selection())
        self.table.delete(*self.table.get_children())

    def hide(self):
        items = self.table.get_children()
        self.table.detach(*items)

    def unhide(self):
        items = self.table.get_children()


    ##### selection control #####
    def unselect(self, event=None):
        self.table.selection_remove(*self.table.selection())

    def selection_set(self, iid):
        self.table.selection_set(*[str(i) for i in iid])
        try:
            self.table.see(str(iid[-1]))
        except:
            pass
    def selection_toggle(self, iid):
        self.table.selection_toggle(*[str(i) for i in iid])
        try:
            self.table.see(self.table.selection()[-1])
        except:
            pass
    def delete(self, iid:list):
        try:
            self.table.selection_remove(*[str(i) for i in iid])
        except:
            pass
        self.table.delete(*[str(i) for i in iid])

    def delete_selected(self, e=None):
        selection = self.table.selection()
        self.table.selection_remove(*selection)
        self.table.delete(*selection)
        return selection

    def export(self, filename, mode='w'):
        with open(filename, mode) as f:
            items = self.table.get_children()
            f.write(','.join(self.displaycolumns))
            f.write('\n')
            for i in items:
                data = self.table.set(i)
                f.write(','.join([str(data.get(c)) for c in self.displaycolumns]))
                f.write('\n')



