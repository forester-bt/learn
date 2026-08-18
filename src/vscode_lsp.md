# VSCode LSP

## Introduction

The Forester LSP provides language server support for the `.tree` language, delivered to VS Code through a thin client extension. The extension registers the `forester` language for `.tree` files, starts the LSP server over stdio, and surfaces highlighting, diagnostics, navigation, and formatting directly in the editor.

## Requirements

- Java 21+ (the language server is a Java application)

## Installation

1. Build the language server launcher:

   ```shell
   ./gradlew installDist
   ```

   The launcher is written to `build/install/forester-lsp/bin`.

2. From the `editors/vscode` folder, build and install the VS Code extension:

   ```shell
   npm install && npm run package && code --install-extension forester-lsp-client-0.0.1.vsix
   ```

   If the `code` command is not on your `PATH`, install the `.vsix` from the Extensions view: **...** menu → **Install from VSIX…**.

3. Configure the server path (Settings → search "forester", or in `settings.json`):

   ```json
   "forester.server.path": "/path/to/forester-lsp/build/install/forester-lsp/bin/forester-lsp"
   ```

   A path ending in `.jar` is also accepted (run via `java -jar`).

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
