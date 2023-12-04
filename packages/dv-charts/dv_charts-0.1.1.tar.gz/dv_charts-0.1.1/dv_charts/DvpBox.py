# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpBox(Component):
    """A DvpBox component.
Plotly Box plot

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- bgColor (string; optional):
    Background color.

- className (string | dict; optional):
    CSS classes to be added to the component.

- data (list; optional):
    Data.

- groupBy2Field (string | boolean; optional):
    Group by field 2 (color field).

- groupbyField (string | boolean; optional):
    Group by field.

- legendLayout (a value equal to: 'vertical', 'horizontal'; optional):
    legend Layout.

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

- showLegend (boolean; default True):
    Show legend.

- style (dict; optional):
    Inline CSS style.

- valueField (string; default 'values'):
    Value Field.

- wrapperHeight (number; optional):
    wrapperHeight.

- wrapperWidth (number; optional):
    wrapperWidth.

- xAxisTitle (string; optional):
    X axis title.

- yAxisTitle (string; optional):
    Y axis title."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dv_charts'
    _type = 'DvpBox'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, valueField=Component.UNDEFINED, groupbyField=Component.UNDEFINED, groupBy2Field=Component.UNDEFINED, wrapperHeight=Component.UNDEFINED, wrapperWidth=Component.UNDEFINED, xAxisTitle=Component.UNDEFINED, yAxisTitle=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, legendLayout=Component.UNDEFINED, legendPosition=Component.UNDEFINED, showLegend=Component.UNDEFINED, bgColor=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'bgColor', 'className', 'data', 'groupBy2Field', 'groupbyField', 'legendLayout', 'legendPosition', 'loading_state', 'showLegend', 'style', 'valueField', 'wrapperHeight', 'wrapperWidth', 'xAxisTitle', 'yAxisTitle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'bgColor', 'className', 'data', 'groupBy2Field', 'groupbyField', 'legendLayout', 'legendPosition', 'loading_state', 'showLegend', 'style', 'valueField', 'wrapperHeight', 'wrapperWidth', 'xAxisTitle', 'yAxisTitle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpBox, self).__init__(**args)
