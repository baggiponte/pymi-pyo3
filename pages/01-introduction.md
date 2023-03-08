---
layout: two-cols
---

# 😵‍💫 What the f🦀k?
Why don't you [rewrite it in Rust™️](https://unhandledexpression.com/rust/2017/07/10/why-you-should-actually-rewrite-it-in-rust.html)

* A meme since 2017 *at least*.
* Some notable python libraries already have a Rust core:
  * [`orjson`](https://github.com/ijl/orjson) first commit dates to 2018.
  * [`pydantic`](https://github.com/pydantic/pydantic-core) is getting a Rust rewrite.
  * [`ruff`](https://github.com/pola-rs/polars) is a *blazingly fast* linter that just crossed 10.000 ⭐, though it's first commit dates to August 2022.
  * [`polars`](https://github.com/pola-rs/polars) a *blazingly fast* dataframe library with more than 15.000 ⭐.

::right::

![rust-meme-1](https://i.stack.imgur.com/pQoAq.png)

---

# 🏗️ Building Python + Rust Packages 
Two packaging steps

Not all *oxidised* Python libraries are created equal. For example, `ruff` Python interface is basically a single function that runs the Rust CLI, while `polars` is actually calling Rust code. We have to distinguish two different layers:

1. Packaging: making an **distributable artifact** that contains both Rust and Python code.
2. Calling Rust code from Python (and, to a lesser extent, viceversa).

---

# 🏗️ Building Python + Rust Packages 
The most popular tools

* `maturin`: Python CLI written in Rust for building and publishing Rust-based Python packages. 
  * offers the highest level of abstraction. For a lower level interface, see [`setuptools-rust`](https://github.com/PyO3/setuptools-rust) or [`milksnake`](https://github.com/getsentry/milksnake).
* `PyO3`: Rust library to write a native Python module in Rust, or to embed Python in a Rust binary
  * [`rust-cpython`](https://github.com/dgrunwald/rust-cpython) is also used.

---

# 📦 Installation and setup
Minimum supported versions

* Python>=3.6
* Rust>=1.41

<br>

>  💡 *Recommendation: version managers*
>
>  * Rust: [`rustup`](https://rust-lang.github.io/rustup/installation/index.html) is the official version manager.
>  * Python: [`pyenv`](https://github.com/pyenv/pyenv) or [`asdf`](https://github.com/asdf-vm/asdf).
>    * Try out [`rtx`](https://github.com/jdxcode/rtx): it's a - wait for it - Rust rewrite of `asdf`.

--- 

# 📦 Installation and setup
Initialise a project with `maturin`

```bash
pipx install maturin
```
<br>

>  💡 *Recommendation: installing Python CLIs*
>
> Use `pipx` to install Python CLIs. Installation instructions are [here](https://pypa.github.io/pipx/#install-pipx).

<br>

```bash
maturin new pymi-pyo3
```

<br>

* `maturin` will prompt you to choose the bindings you want to use: select `pyo3`.
* This will generate a `pymi-pyo3` folder inside the current one.

---

# 🔎 Directory Tree
An overview

```
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

```toml
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


```toml
[build-system]
requires = ["maturin>=0.14,<0.15"]
build-backend = "maturin"

[tool.maturin]
features = ["pyo3/extension-module"]
```

---

# 🔎 Directory Tree
Rust code: `src/lib.rs` (1)

```rust
use pyo3::prelude::*;                                       // <- rust equivalent of `from xyz import *` 

/// Formats the sum of two numbers as string.
#[pyfunction]                                               // <- macro: denotes a rust function
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {  //    that can be called from python 
    Ok((a + b).to_string())
}
```

---

# 🔎 Directory Tree
Rust code: `src/lib.rs` (2)

```rust
/// A Python module implemented in Rust.
#[pymodule]                                                 // <- macro: denotes a python module
fn pymi_pyo3(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}

```

