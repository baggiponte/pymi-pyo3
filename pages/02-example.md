---
title: 🔎 Directory Tree
---

# 🔎 Directory Tree
An overview

```text {all|4|6|8-9|10}
.
├── .github
│  └── workflows
│     └── CI.yml        # <- publish to pypi whenever you push a new tag
├── src
│  └── lib.rs           # <- rust source code
├── .gitignore
├── Cargo.lock
├── Cargo.toml          # <- rust lib configs
└── pyproject.toml      # <- python lib configs
```

---

# 🔎 Directory Tree
The Rust side: `Cargo.toml`

* Rust's equivalent of `pyproject.toml`

```toml {all|6-13|7|13|15-16}
[package]
name = "pymi-pyo3"
version = "0.1.0"
edition = "2021"

[lib]
name = "pymi_pyo3"
# "cdylib" is necessary to produce a shared library for Python to import from.
#
# Downstream Rust code  will not be able to `use string_sum;`
# unless the "rlib" or "lib" crate type is also included, e.g.:
# crate-type = ["cdylib", "rlib"]
crate-type = ["cdylib"] 

[dependencies]
pyo3 = "0.18.1"
```

---

# 🔎 Directory Tree
The Rust side: `Cargo.lock`

* A `requirements.txt` on steroids.
  * Not officially supported in Python: [PEP665](https://peps.python.org/pep-0665/) was rejected.
  * Lockfiles are implemented nonetheless: see `pdm.lock` and `poetry.lock`.

---

# 🔎 Directory Tree
The Python side: `pyproject.toml`

* `maturin` is the build-backend (see [here](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html) and [here](https://chadsmith-software.medium.com/pep-517-and-518-in-plain-english-47208ca8b7a6)).
* In the `maturin` table, we instruct it to use `pyo3`.


```toml {all|1-3|5-6}
[build-system]
requires = ["maturin>=0.14,<0.15"]
build-backend = "maturin"

[tool.maturin]
features = ["pyo3/extension-module"]
```

---

# 🔎 Directory Tree
Rust code: `src/lib.rs`

```rust {all|1|4-7|4|5|10-14|10|11|12|3,9}
use pyo3::prelude::*;                                       // <- rust equivalent of `from xyz import *` 

/// Formats the sum of two numbers as string.               // docstring! supports markdown, rendered as HTML
#[pyfunction]                                               // <- procedural macro: denotes a rust function
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {  //    that can be called from python 
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]                                                 // <- procedural macro: denotes a python module
fn pymi_pyo3(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;   // <- declarative macro
    Ok(())
}
```

<!--
* can override the default module name with `#[pyo3(name = "custom_name")]`
-->

---

# 🔎 Directory Tree
Other macros

```rust


```
