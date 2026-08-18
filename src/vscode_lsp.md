# VSCode LSP

## Introduction

The Forester LSP provides language server support for the `.tree` language, delivered to VS Code through a thin client extension. The extension registers the `forester` language for `.tree` files, starts the LSP server over stdio, and surfaces highlighting, diagnostics, navigation, and formatting directly in the editor.

## Installation

See the [VS Code extension](https://github.com/forester-bt/forester-lsp/tree/master/editors/vscode) in the Forester LSP repository for installation instructions.

## Features

### Syntax Highlighting
Highlights the `.tree` language via LSP semantic tokens, distinguishing keywords (e.g. `root`, `sequence`), strings, numbers, and comments.

### Diagnostics
Reports parse errors inline as you type, backed by an ANTLR4-based parser.

### Completion
Provides autocompletion triggered on `"`, `/`, and `.`.

### Go to Definition
Navigates to the definition of tree nodes and references.

### Find References
Lists all references to a tree node across the workspace.

### Document Symbols
Shows the hierarchical outline / breadcrumbs of tree nodes.

### Formatting
Formats the document via the `Format Document` command.

### Editor Features
- **Comment toggling** for `//` line comments and `/* */` block comments.
- **Bracket matching** and auto-closing for `{}`, `[]`, `()`, and strings.

## Links
- [Repository](https://github.com/forester-bt/forester-lsp)
- [VS Code extension](https://github.com/forester-bt/forester-lsp/tree/master/editors/vscode)
