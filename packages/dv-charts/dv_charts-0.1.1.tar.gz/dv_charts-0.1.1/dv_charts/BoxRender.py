# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class BoxRender(Component):
    """A BoxRender component.
Box inputs

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- height (number; optional):
    Height.

- inputs (dict; optional):
    Inputs.

- width (number; optional):
    Width."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dv_charts'
    _type = 'BoxRender'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, inputs=Component.UNDEFINED, height=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'height', 'inputs', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'height', 'inputs', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(BoxRender, self).__init__(**args)
