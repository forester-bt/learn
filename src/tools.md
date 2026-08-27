# Tools

The Forester ecosystem includes several auxiliary tools and libraries to help you write, analyze, and execute behavior trees.

## IntelliJ Plugin

The [Forester IntelliJ Plugin](https://github.com/forester-bt/forester-intellij-plugin) provides native IDE support for the `.tree` language. Features include:
* Syntax highlighting
* Code folding
* Code navigation
* Code formatting
* Code inspections and error highlighting
* Structure view
* Built-in tasks to visualize and simulate the tree directly from the IDE

## VSCode LSP

The [Forester LSP](https://github.com/forester-bt/forester-lsp) provides language server support for the `.tree` language in VS Code. Features include:
* Syntax highlighting via LSP semantic tokens
* Inline diagnostics (parse errors) via ANTLR4-based parsing
* Completion (triggered on `"`, `/`, and `.`)
* Go to definition and find references
* Document symbols (outline / breadcrumbs)
* Formatting
* Comment toggling and bracket matching / auto-closing

## CLI (`f-tree`)

The `f-tree` command-line interface is the primary utility for testing and manipulating trees without writing boilerplate application code. It supports:
* Running trees from the file system, configured with optional YAML run profiles.
* Simulating trees with stubbed actions using YAML profiles.
* Generating SVG visualizations of the tree structure.
* Printing built-in standard library headers (e.g., `std::actions`).