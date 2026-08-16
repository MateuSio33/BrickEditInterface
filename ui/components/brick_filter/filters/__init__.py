from ui.components.brick_filter.filters.base_filter import FilterMode, FilterResult, BaseFilter
from ui.components.brick_filter.filters.color_filter import ColorFilter
from ui.components.brick_filter.filters.force_all_filter import ForceAllFilter
from ui.components.brick_filter.filters.group_filter import EditorGroupFilter, WeldGroupFilter

filter_classes: list[BaseFilter] = [
    ColorFilter,
    EditorGroupFilter,
    WeldGroupFilter,
    ForceAllFilter
]
