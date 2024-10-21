# Draftsmith CLI

<p><img src="./assets/logo.png" style="float: left; width: 80px" /></p>

Draftsmith CLI is an implementation of an api client for the [Draftsmith API](https://github.com/RyanGreenup/draftsmith_api). The API provides a REST API to interface with a PostgreSQL database of notes, this CLI allows the user to interface with the API from the command line whilst providing a reference for implementing the API in your own projects.

Draftsmith is an open source knowledge management paradigm designed for personal use. The hope is to provide sophisticated features such as Semantic Mediawiki and Notion whilst keeping the project open, easy to fork and stable to use.

## Overview

This cli is a simple implementation of the Draftsmith API, it allows users to create and modify notes. The client implementation is contained in:

- [src/tasks.py](./src/tasks.py)
    - [Tests](./tests/test_tasks.py)
- [src/notes.py](./src/notes.py)
    - [Tests](./tests/test_notes.py)
- [src/tags.py](./src/tags.py)
    - [Tests](./tests/test_tags.py)

This client implementation serves to document the API and provide a reference for implementing the API in other projects.

## Installation

To get started with NoteMaster:

### Backend

Install the backend API by following the [API Setup Guide](https://ryangreenup.github.io/draftsmith_api/installation.html), this is essentially a `docker compose up` command.

### Interfaces

2. **CLI Client**
   - Install Python and dependencies.
       - `pipx install --force  https://github.com/RyanGreenup/draftsmith_cli`

3. [**PyQt GUI**](https://github.com/RyanGreenup/draftsmith)
   - `pipx install https://github.com/RyanGreenup/draftsmith`

4. **Web UI (Flask)**
   - To Be Implemented

## Usage

- **CLI Commands**: The CLI commands are described through the `--help` flag.
  - `draftsmith --help`
  - `draftsmith notes --help`
  - `draftsmith tags --help`
  - `draftsmith tasks --help`
- **Graphical Interfaces**: Check the user manuals for PyQt and Flask UIs for detailed navigation tips.

## Contribution

I warmly welcome contributions from the community!

- **Fork the Repository**: Make the changes you’d like to see.
- **Submit a Pull Request**: I'd be thrilled to review and merge all contributions.
    - Please ensure that your code has tests and adheres to the `ruff` / `black` formatter.
- **Report Issues**: Help me by reporting bugs or suggesting features via the issue tracker.

## Roadmap

- [ ] Implement Flask or Django Web UI.
- [ ] Develop a Jetpack / Flutter mobile application for Android.
- [ ] Implement the PyQT GUI.
- [ ] Implement Structured Data and features similar to [Semantic Mediawiki](https://www.semantic-mediawiki.org/wiki/Semantic_MediaWiki), notion and [Dokuwiki's Struct Plugin](https://www.dokuwiki.org/plugin:struct) features.
- [ ] Implement real-time collaboration features.
- [ ] Implement Semantic Search and Tagging via OpenAI API such as [ollama](https://ollama.com/)
    - See [this issue](https://github.com/RyanGreenup/draftsmith_api/issues/2)
- [ ] Implement RAG over notes
- [ ] Implement a Kanban board view
- [ ] Implement a timeline view
- [ ] Implement a mindmap view
- [ ] Implement a table view for structured data
- [ ] Implement a graph view
- [ ] Implement a calendar view

## Join Our Community

Connect with me on Discord (`Eisenvig`) / Matrix (`@eisenvig:matrix.org`), or follow me on [Mastodon](`@ryangreenup@mastodon.social`) for the latest updates.

---

Structured thinking is increasingly important now that LLM's are making information more accessible than ever before.

