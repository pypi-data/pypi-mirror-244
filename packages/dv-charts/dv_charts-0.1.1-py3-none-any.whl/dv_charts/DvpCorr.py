# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpCorr(Component):
    """A DvpCorr component.
Antd Heatmap

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string | dict; optional):
    CSS classes to be added to the component.

- data (list; optional):
    Data.

- labelField (string; default 'p'):
    Label Field.

- loading_state (dict; optional):
    loading state.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- style (dict; optional):
    Inline CSS style.

- valueField (string; default 'value'):
    Value Field.

- xField (string; default 'x'):
    x Field.

- yField (string; default 'y'):
    y Field."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dv_charts'
    _type = 'DvpCorr'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, xField=Component.UNDEFINED, yField=Component.UNDEFINED, labelField=Component.UNDEFINED, valueField=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'data', 'labelField', 'loading_state', 'style', 'valueField', 'xField', 'yField']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'data', 'labelField', 'loading_state', 'style', 'valueField', 'xField', 'yField']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpCorr, self).__init__(**args)
