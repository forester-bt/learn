<p align="center">
    <img width="255" alt="Logo" src="examples/logo.png">
</p>
<h1 align="center">Forester — Documentation & Examples</h1>

## Book

The full documentation for [Forester](https://github.com/forester-bt/forester) is built with [mdbook](https://rust-lang.github.io/mdBook/) and deployed via GitHub Pages.

To build locally:

```bash
cargo install mdbook mdbook-graphviz mdbook-mermaid
mdbook build
```

## Examples

Code examples accompanying the Forester article series.

- [Higher-order trees](./examples/ho_article)
- [Trimming — runtime tree modification](./examples/trimming)
- [Remote actions](./examples/remote_action)
- [Export to ROS Nav2](./examples/export_ros_nav)
- [Daemons](./examples/daemons/simple_daemon)
- [Warm-up example (1D line sorting)](./examples/example1dtext)
- [Robotic simulation with Webots](./examples/webots)
- [Standalone .tree files](./examples/bt)
