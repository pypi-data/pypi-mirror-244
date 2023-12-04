# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpDesBox(Component):
    """A DvpDesBox component.
A component to build box

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    Classname.

- data (list; optional):
    A list of values.

- groupBy (string; optional):
    Group by.

- labels (dict; optional):
    labels - A dict to remape the numbers into category.

- missingValues (list; default [99999, 88888, 9999, 8888, 8881, 8882, 7777, 6666]):
    missingValues.

- style (dict; optional):
    Inline CSS style.

- variable (string; optional):
    Variable Y Field.

- wrapperHeight (string | number; default 500):
    wrapperHeight.

- yAxisTitle (string; optional):
    Y axis title."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dv_charts'
    _type = 'DvpDesBox'
    @_explicitize_args
    def __init__(self, data=Component.UNDEFINED, variable=Component.UNDEFINED, groupBy=Component.UNDEFINED, missingValues=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, labels=Component.UNDEFINED, yAxisTitle=Component.UNDEFINED, wrapperHeight=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'data', 'groupBy', 'labels', 'missingValues', 'style', 'variable', 'wrapperHeight', 'yAxisTitle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'data', 'groupBy', 'labels', 'missingValues', 'style', 'variable', 'wrapperHeight', 'yAxisTitle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpDesBox, self).__init__(**args)
