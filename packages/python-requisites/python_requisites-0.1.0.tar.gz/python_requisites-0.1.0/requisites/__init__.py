import inspect
from types import MappingProxyType
from typing import Any, Callable, Dict, Optional, Text, Tuple

from .version import VERSION

__version__ = VERSION

ArgsType = Tuple[Any, ...]
KwargsType = Dict[Text, Any]


def collect_params(
    fun: Callable,
    *any_args,
    args: Optional[ArgsType] = None,
    kwargs: Optional[KwargsType] = None,
    requisites_raise_too_many_positional_args: bool = False,
    **extra_kwargs,
) -> Tuple[ArgsType, KwargsType]:
    """Collects the required positional and keyword arguments of a function.

    Parameters
    ----------
    fun : Callable
        A function.
    any_args : Any
        Any positional arguments.
    args : Optional[ArgsType], optional
        Positional arguments, by default None.
    kwargs : Optional[KwargsType], optional
        Keyword arguments, by default None.
    requisites_raise_too_many_positional_args : bool, optional
        Whether to raise an error if there are too many positional arguments, by default False.
    extra_kwargs : Any
        Extra keyword arguments.
    Raises
    ------
    TypeError
        If a required positional or keyword argument is missing.
    """

    signature_parameters: MappingProxyType[
        Text, "inspect.Parameter"
    ] = inspect.signature(fun).parameters

    var_positionals = ([i for i in args] if args else []) + [i for i in any_args]
    var_keywords = {k: v for k, v in kwargs.items()} if kwargs else {}
    var_keywords.update(
        {k: v for k, v in extra_kwargs.items() if k not in var_keywords}
    )
    collected_args = []
    collected_kwargs = {}
    has_var_positional = False
    has_var_keyword = False

    for param_name, param_meta in signature_parameters.items():
        if param_meta.kind == inspect.Parameter.POSITIONAL_ONLY:
            if not var_positionals:
                raise TypeError(f"Missing required positional argument: '{param_name}'")
            collected_args.append(var_positionals.pop(0))

        elif param_meta.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if param_name in var_keywords:
                collected_kwargs[param_name] = var_keywords.pop(param_name)
            elif var_positionals:
                collected_args.append(var_positionals.pop(0))
            elif param_meta.default != inspect.Parameter.empty:
                collected_kwargs[param_name] = param_meta.default
            else:
                raise TypeError(f"Missing required positional argument: '{param_name}'")

        elif param_meta.kind == inspect.Parameter.VAR_POSITIONAL:
            has_var_positional = True

        elif param_meta.kind == inspect.Parameter.KEYWORD_ONLY:
            if param_name in var_keywords:
                collected_kwargs[param_name] = var_keywords.pop(param_name)
            elif param_meta.default != inspect.Parameter.empty:
                collected_kwargs[param_name] = param_meta.default
            else:
                raise TypeError(f"Missing required keyword argument: '{param_name}'")

        elif param_meta.kind == inspect.Parameter.VAR_KEYWORD:
            has_var_keyword = True

        else:
            raise TypeError(f"Unsupported parameter type: '{param_meta.kind}'")

    if var_positionals:  # Still have positional arguments
        if has_var_positional:  # Has *args
            collected_args.extend(var_positionals)
        elif requisites_raise_too_many_positional_args:  # Without *args and raise
            raise TypeError(f"Too many positional arguments: {var_positionals}")
        else:
            pass  # Without *args and not raise

    if var_keywords:  # Still have keyword arguments
        if has_var_keyword:  # Has **kwargs
            collected_kwargs.update(var_keywords)
        else:
            pass  # Without **kwargs

    return (tuple(collected_args), collected_kwargs)
