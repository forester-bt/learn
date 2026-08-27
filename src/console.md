# Console f-tree

The console utility `f-tree` can be installed using `cargo` and can be used to run, simulate and visualize the tree.

The [Intellij plugin](intellij.md) basically wraps this utility and provides the same functionality.

```shell
cargo install f-tree
```

and then be used with

```shell
~ f-tree --help
Usage: f-tree [OPTIONS] <COMMAND>

Commands:
  print-std-actions  Print the list of std actions from 'import std::actions'
  sim                Runs simulation. Expects a simulation profile
  run                Runs the tree from the file system. Accepts an optional run profile in yaml
  vis                Runs visualization. Output is in svg format.
  help               Print this message or the help of the given subcommand(s)

Options:
  -v, --verbose  Print verbose logs
  -h, --help     Print help
  -V, --version  Print version


```
