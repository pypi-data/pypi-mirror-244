'''
# hintwith
Hints your function with an existing one.

## Usage

Use `hintwith()` to annotate a function with another one's annotations:

```py
>>> from hintwith import hintwith
>>> def a(x: int, y: int, z: int = 0) -> int:
...     """Sums x, y and z."""
...     return x + y + z
...
>>> @hintwith(a)
... def b(*args, **kwargs) -> float:
...     return float(a(*args, **kwargs))
...
```

Also, there is `hintwithmethod()` to annotate the function with a method rather than another
function.

## See Also
### Github repository
* https://github.com/Chitaoji/hintwith/

### PyPI project
* https://pypi.org/project/hintwith/

## License
This project falls under the BSD 3-Clause License.

### v0.1.0
* Initial release.

'''

from .__version__ import __version__
from .core import *

__all__ = ["hintwith", "hintwithmethod"]
