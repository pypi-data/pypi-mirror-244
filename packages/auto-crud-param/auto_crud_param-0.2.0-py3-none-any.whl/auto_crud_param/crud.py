import panel as pn
import param as pm
from panel.widgets import Button, MultiSelect, TextInput


class CRUDListParameter(pm.Parameterized):
    items = pm.List(default=[])

    def create(self, item):
        self.items.append(item)

    def read(self, index):
        return self.items[index]

    def update(self, index, new_item):
        self.items[index] = new_item

    def delete(self, index):
        del self.items[index]


class CRUDMultiSelect(MultiSelect):
    def __init__(self, crud_param, **params):
        self.crud_param = crud_param
        super().__init__(**params)
        self.options = self.crud_param.items

        # Create buttons for CRUD operations
        self.create_button = Button(name='Create', button_type='primary')
        self.update_button = Button(name='Update', button_type='success')
        self.delete_button = Button(name='Delete', button_type='danger')
        self.confirm_delete_button = Button(
            name='Confirm Delete', button_type='danger', visible=False
        )

        # Add event handlers
        self.create_button.on_click(self.create_item)
        self.update_button.on_click(self.update_item)
        self.delete_button.on_click(self.delete_item)
        self.confirm_delete_button.on_click(self.confirm_delete)

        # Input for create/update
        self.input_dialog = TextInput(name='Item', placeholder='Enter item here')

    def panel(self):
        # Update the options of the MultiSelect widget whenever the crud_param changes
        self.crud_param.param.watch(
            lambda event: setattr(self, 'options', event.new), 'items'
        )

        return pn.Column(
            self.input_dialog,
            pn.Row(
                self.create_button,
                self.update_button,
                self.delete_button,
                self.confirm_delete_button,
            ),
            self,  # The MultiSelect widget itself
        )

    def create_item(self, event):
        new_item = self.input_dialog.value
        if new_item:
            self.crud_param.create(new_item)
            self.input_dialog.value = ''  # Reset input field
            self.options = self.crud_param.items  # Update options
            self.param.trigger('options')  # Explicitly trigger an update

    def update_item(self, event):
        updated_item = self.input_dialog.value
        if not updated_item:
            return

        selected_items = self.value
        if not selected_items:
            return

        for selected_item in selected_items:
            selected_index = self.options.index(selected_item)
            self.crud_param.update(selected_index, updated_item)

        self.input_dialog.value = ''  # Reset input field
        self.options = self.crud_param.items  # Update options
        self.param.trigger('options')  # Explicitly trigger an update

        def update_existing_item(self, event):
            updated_item = self.input_dialog.value
            if updated_item:
                selected_items = self.value
                if not selected_items:
                    return
                selected_index = self.options.index(selected_items[0])
                self.crud_param.update(selected_index, updated_item)
                self.input_dialog.value = ''  # Reset input field

    def delete_item(self, event):
        selected_items = self.value
        if not selected_items:
            return

        self.confirm_delete_button.visible = True

    def confirm_delete(self, event):
        selected_items = self.value
        if not selected_items:
            return

        # Delete all selected items
        for item in selected_items:
            if item in self.options:
                selected_index = self.options.index(item)
                self.crud_param.delete(selected_index)

        # Update the options and hide the confirm delete button
        self.options = self.crud_param.items
        self.confirm_delete_button.visible = False
        self.param.trigger('options')  # Explicitly trigger an update
