# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.
Button component

Keyword arguments:

- id (default 'button'):
    Component id.

- color (default 'primary'):
    MUI button color.

- disableElevation (optional):
    Disable elevation.

- disableFocusRipple (optional)

- disableRipple (optional):
    Button has no ripple effect.

- disabled (optional):
    Button is disabled.

- endIcon (optional):
    Material Icon name to display at end of button -
    https://v4.mui.com/components/material-icons/.

- href (optional):
    Button link.

- iconColor (optional):
    Icon color.

- margin (default 2):
    Component margin.

- nClicks (default 0):
    Number of times the button has been clicked.

- setProps (optional):
    Used to enable Dash-assigned component callback.

- size (default 'medium'):
    MUI button size, small | medium | large.

- startIcon (optional):
    Material Icon name to display at start of button -
    https://v4.mui.com/components/material-icons/.

- text (optional):
    Button text.

- variant (default 'contained'):
    MUI button variant.

- width (optional):
    Component width."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'Button'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, text=Component.UNDEFINED, variant=Component.UNDEFINED, color=Component.UNDEFINED, iconColor=Component.UNDEFINED, size=Component.UNDEFINED, margin=Component.UNDEFINED, disabled=Component.UNDEFINED, disableRipple=Component.UNDEFINED, disableFocusRipple=Component.UNDEFINED, disableElevation=Component.UNDEFINED, startIcon=Component.UNDEFINED, endIcon=Component.UNDEFINED, href=Component.UNDEFINED, width=Component.UNDEFINED, nClicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'color', 'disableElevation', 'disableFocusRipple', 'disableRipple', 'disabled', 'endIcon', 'href', 'iconColor', 'margin', 'nClicks', 'setProps', 'size', 'startIcon', 'text', 'variant', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'color', 'disableElevation', 'disableFocusRipple', 'disableRipple', 'disabled', 'endIcon', 'href', 'iconColor', 'margin', 'nClicks', 'setProps', 'size', 'startIcon', 'text', 'variant', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Button, self).__init__(**args)
