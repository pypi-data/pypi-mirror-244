# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpPie(Component):
    """A DvpPie component.
Antd Pie

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string | dict; optional):
    CSS classes to be added to the component.

- colorField (string; default 'type'):
    Color field.

- data (list; optional):
    Data.

- legendPosition (a value equal to: 'top', 'right'; default 'right'):
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

- showLabels (boolean; default True):
    Show Labels.

- showLegend (boolean; default True):
    Show legend.

- style (dict; optional):
    Inline CSS style.

- valueField (string; default 'value'):
    Value field."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dv_charts'
    _type = 'DvpPie'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, colorField=Component.UNDEFINED, valueField=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, legendPosition=Component.UNDEFINED, showLegend=Component.UNDEFINED, showLabels=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'colorField', 'data', 'legendPosition', 'loading_state', 'showLabels', 'showLegend', 'style', 'valueField']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'colorField', 'data', 'legendPosition', 'loading_state', 'showLabels', 'showLegend', 'style', 'valueField']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpPie, self).__init__(**args)
