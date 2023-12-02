# nudisxs

[![PyPI - Version](https://img.shields.io/pypi/v/nudisxs.svg)](https://pypi.org/project/nudisxs)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nudisxs.svg)](https://pypi.org/project/nudisxs)

-----

**Table of Contents**

- [Overview](#overview)
- [REQUIREMENTS](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Overview

The `nudisxs` package integrates Python with Fortran computational routines, offering a user-friendly interface for complex neutrino-nucleon interaction simulations. This includes both charged and neutral current exchange calculations.

## Requirements
- [LHAPDF](https://lhapdf.hepforge.org/). Install it with python support. Follow [installation](https://lhapdf.hepforge.org/install.html) instructions. Installations to a custom place like `/foo/lhapdf` requires setup of three variables
```console
export PATH=$PATH:/foo/lhapdf/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/foo/lhapdf/lib
export PYTHONPATH=$PYTHONPATH:/foo/lhapdf/lib/pythonX.Y/site-packages
```

## Installation

### Installing from PyPi
You can easily install `nudisxs` from PyPi using pip:
```console
pip install nudisxs
```
### Installing from Git
To install the latest development version directly from the repository:
```console
git clone git@git.jinr.ru:dnaumov/nudisxs.git
cd nudisxs
python install .
```

## Usage
Python Interface
The ```disxs.py``` module in ```nudisxs``` provides all necessary interfaces to the underlying Fortran code. This includes functions for initialization and calculation of cross-sections.

### Initialization
Common initialization functions:
  * most used:
    - init_neutrino()
    - init_pdf()
    - init_target()

  * for experts:
    - init_masses()
    - init_bend_factor()
    - init_q2_min()
    - init_abc()
    - init_structure_functions()
    - init_r_function()
    - init_final_hadron_mass()
    - init_fl_function()
    - init_qc()
- double differential cross-sections
```math
\frac{d^2\sigma}{dxdy}
```
   are available as  
  `disxs.xs_cc(e,x,y)` for charged current exchange and
  `disxs.xs_nc(e,x,y)` for neutral current exchange.
- some examples can be found in
  - `nudisxs/tests/test_dis.py`
  - `nudisxs/tests/test_dis_total.py`

## License

`nudisxs` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
