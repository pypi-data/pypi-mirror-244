# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpDesPie(Component):
    """A DvpDesPie component.
Antd Pie

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string | dict; optional):
    CSS classes to be added to the component.

- data (list; optional):
    Data.

- labels (dict; optional):
    labels - A dict to remape the numbers into category.

- legendPosition (a value equal to: 'top', 'right'; optional):
    Legend Position.

- loading_state (dict; optional):
    loading state.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- missingValues (list; default [99999, 88888, 9999, 8888, 8881, 8882, 7777, 6666]):
    missingValues.

- showLabels (boolean; optional):
    Show Labels.

- showLegend (boolean; optional):
    Show legend.

- style (dict; optional):
    Inline CSS style.

- variable (string; optional):
    Variable.

- wrapperHeight (string | number; optional):
    wrapperHeight."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dv_charts'
    _type = 'DvpDesPie'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, variable=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, missingValues=Component.UNDEFINED, wrapperHeight=Component.UNDEFINED, labels=Component.UNDEFINED, showLegend=Component.UNDEFINED, showLabels=Component.UNDEFINED, legendPosition=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'data', 'labels', 'legendPosition', 'loading_state', 'missingValues', 'showLabels', 'showLegend', 'style', 'variable', 'wrapperHeight']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'data', 'labels', 'legendPosition', 'loading_state', 'missingValues', 'showLabels', 'showLegend', 'style', 'variable', 'wrapperHeight']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpDesPie, self).__init__(**args)
