# exponential_counter

[![PyPI - Version](https://img.shields.io/pypi/v/exponential-counter.svg)](https://pypi.org/project/exponential-counter)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/exponential-counter.svg)](https://pypi.org/project/exponential-counter)

-----

**Table of Contents**

- [Usage](#usage)
- [Installation](#installation)
- [License](#license)

## Usage
```
from exponential_counter import ExponentialCounter, LinearCounter
counter = LinearCounter(max_value=4)
values = [counter() for i in range(8)]
# [0, 1, 2, 3, 4, 4, 4, 4]

counter = ExponentialCounter(start=4, step=3, max_value=32)
values = [counter() for i in range(6)]
# [4, 12, 32, 32, 32, 32]
```

## Installation

```console
pip install exponential-counter
```

## License

`exponential-counter` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
