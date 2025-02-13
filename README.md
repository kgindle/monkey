
# Monkey

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/kgindle/monkey)
[![Discord](https://img.shields.io/discord/1339096899952574547)](https://discord.gg/AYzqUCrx)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Ollama](https://img.shields.io/badge/ollama-81008d?style=for-the-badge&logo=ollama&logoColor=fff)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![ChromaDB](https://img.shields.io/badge/chromadb-4A148C.svg?style=for-the-badge&logo=chromadb&logoColor=white)

Monkey 🐒 is a tool for creating autonomous agents that can read and write code
in your project. The name is inspired by the [Infinite Monkey Theorem]:

> If I let my fingers wander idly over the keys of a typewriter it might happen
> that my screed made an intelligible sentence. If an army of monkeys were
> strumming on typewriters they might write all the books in the British Museum.
> The chance of their doing so is decidedly more favorable than the chance of
> the molecules returning to one half of the vessel.
> 
> ---
> <cite>Arthur Eddington (1927)</cite>

Monkey is built with:

- [Ollama] - Evaluate LLM models like `codegemma-9b` or `llama3-8b`.
- [ChromaDB] - Vector database for embeddings.
- [Python] - Smartest snake ever now working with monkeys 😲.
- [SQLite] - World's most widely deployed database engine.

## How it works

Monkey uses a combination of LLMs and vector embeddings to read code, discuss
their understanding, and write code:

- **See:** Read code and understand it.
- **Hear:** Listen to feedback from you and other monkeys.
- **Do:** Write code based on the feedback and their understanding.

Monkey can use multiple autonomous agents (called *monkeys*) that each may
specialize in languages, codebases, use different models, have different
prompts, and more.

## Installation

To install Monkey:

```bash
git clone git@github.com:kgindle/monkey.git
cd monkey/
pip install -e .
```

You will now have the `monkey` command available. You can run `git pull` to
update to the latest version and the Python package will be updated
automatically.

Upon first run `monkey` will help you setup your system.

## Usage

To start using `monkey`, you need to create a [Monkeyfile] in the root of your
project. This file describes your project and how the monkeys will code,
although most fields are optional:

```yaml
name: hello-world
model: llama3-8b
test: monkeybars
```

Now you can run Monkey from within your project directory or any subdirectory.


### Monkeys Read Code

You can instruct Monkey to read and understand code using the `see` command:

```bash
monkey see
```

Running the `see` command tells Monkey that now is a safe time to read the code
in your project. This is done by taking a copy of your code and processing it
locally in the background. This means it's safe to go back to work while the
monkeys are reading the code.

The `see` command is safe to run multiple times as the content is cached, but
stress is put on the vector database and LLM resources.

You can also give specific paths to read:
    
```bash
monkey see src/main.py
```

This is described more in the [Command Options](#command-options) section.

### Listen to feedback

You can instruct the monkeys to listen to feedback using the `hear` command:

```
$ monkey hear
> Use the logging module instead of print statements.
```

This can be any feedback you want to provide to the monkeys. The monkeys will
use this feedback to improve their code writing and [Monkeymap](#monkeymap).

### Write code

You can instruct the monkeys to write code using the `do` command:

```bash
monkey do
```

Running the `do` command tells Monkey that now is a safe time to write code in
your project based on the code they have read and the feedback they have
received. If you have modified the code since, the monkeys will not write the
code.


### Command Options

All of the commands (`see`, `hear`, `do`) have some common options and
have the same argument pattern:

```bash
monkey [options] <command> [path...]
```

Where `[path...]` is any number of paths to files or directories to limit the
scope of the command to. If no files are provided, the scope is the entire
project.

For example, using the `monkey see ./foo` command will only read, index and
reason about code in the `foo` directory. Shared vector databases will still
be updated.

Using `monkey hear ./foo` will place that feedback in the context of the `foo`
directory. This is useful for providing feedback on specific parts of the
codebase.

With `monkey do ./foo` the monkeys will only edit the `foo` directory.

Each command also has the following options:

* `--monkey`: The name of the monkey to use. If not provided, all monkeys will
    be used.


## Monkeyfile

You describe your project and how the monkeys will code using a `Monkeyfile`.

This file is written in YAML and contains the following keys:

- `name`: The name of the project. This is optional and will be derived from the
  directory name if not provided.

- `model`: The default model to use for the monkeys. This can be any model
    configured with Ollama. By default `llama3-8b` is used.

- `ignore`: A list of files that the monkeys will ignore entirely. These files
    will not be read or affected by other commands. The files are specified as
    strings which may also include glob patterns, e.g. `["src/main.py",
    "src/foo/*.py"]`.

- `protected`: A list of files that the monkeys are allowed to read but cannot
    make changes to. The files are specified as strings which may also include
    glob patterns, e.g. `["src/main.py", "src/foo/*.py"]`. This is optional.

- `monkeys`: A dictionary of monkeys that will be coding in your project. The
    keys are the names of the monkeys and the values are dictionaries with the
    keys and values described below. By default there is a single monkey named
    `abu` that can code in any language without specialization in any specific
    tasks or part of the codebase.
    
    - `languages`: A list of languages the monkey can code in. The monkeys will
        only be able to code in these languages. The languages are specified as
        strings, e.g. `["python", "java"]`. By default the monkey can code in
        any language.
    
    - `model`: The specific model to use for this monkey as an override for the
        project default.
    
    - `prompt`: An extra string that is provided to the monkey when they are
        coding. This can be used to provide additional context or instructions
        to the monkey. By default the prompt is empty.

    - `scope`: A list of files that the monkey can edit. The files are specified
        as strings which may also include glob patterns, e.g. `["src/main.py",
        "src/foo/*.py"]`. By default the monkey can edit any file in the
        project.

### Access

Monkeys are not granted access to the `Monkeyfile` itself.

## Monkeydream

Monkeydream is the method of translating source files into descriptions of the
functionality that the code provides and the reverse. This is different than
simply converting that code to an embedding directly, since searching directly:

 - Finds code that is nearby in embedding space, but doesn't provide the same
   functionality.
 - Doesn't handle different implementations of the same functionality.

This is done by using LLMs to generate a description of the code that
is stored in a vector database. Later we can use the vector database to find
code that provides that functionality.

## Monkeytrip

Monkeytrip is the method of increasing and decreasing the description
specificity allowing for retrieval of code that may provide similar
functionality.

As an example, if the description is `"a function that reads a file"` we can
increase the specificity to `"a function that reads a file and returns the
contents as a string"` or decrease the specificity to `"a function that reads a
file and returns the contents as a list of lines"`.

When enumerating the possibilities to code, the monkeys can use this to find or
dream code that is similar but may need to be adjusted to fit the current
context.

## Monkeybars

Monkeybars is an instrumentation and testing framework to improve
discoverability. By giving better feedback to the monkeys about why the code is
failing beyond basic syntax errors they can learn faster and write better code.

These are designed to be:

 * Minimally intrusive as to not warp the monkeys understanding of the code.
 * Quick and easy to write as they are used to transfer knowledge to the
   monkeys.

A common instrumentation would be modifying the environment to fail fast instead
of waiting for a network timeout. Another instrumentation might be a safeguard
to avoid working with files that are too large.

## Monkeymap

A *Monkeymap* stores how monkeys understand and write code. It's composed of the
vector databases and metadata beyond. It can be specific to a project or shared
across multiple projects.

A Monkeymap can be exported into a `.monkeymap` file, which is a compressed
archive of all the data in a standalone file.

## License

Monkey is licensed under the MIT license. See the [LICENSE](/LICENSE.md) file
for more information. This is a permissive license that allows you to use,
modify, and distribute the software.

## Contributing

Contributions are welcome! Fork the repository and submit a pull request.

Looking for something to jump in on? Consider looking at issues with these
labels:

 - [Planning Issues] - Issues that are being prepared for implementation. This
    is a good place to start if you want to get a feel for the project. It's
    where contributors transform ideas into actionable tasks.
  
  - [Ready Issues] - Issues that are ready to be worked on. These are well
    defined and have a clear path to completion. This is a good place to start
    if you want to dive right in and know the underlying technologies.

## Acknowledgements

Monkey was originally developed by [Kristopher Gindlesperger].

Meta trained LLaMA and made it available under a permissive license. The cost of
training these models is exorbitant.

Thanks to the authors and contributors of [Ollama]. This project and its
community make it possible to run any model on any hardware.

Thanks to the authors and contributors of [ChromaDB]. This project allows for
the storage and retrieval of embeddings in a simple and efficient manner.

[Ollama]: https://ollama.com
[ChromaDB]: https://docs.trychroma.com
[Python]: https://www.python.org
[SQLite]: https://www.sqlite.org
[Infinite Monkey Theorem]: https://en.wikipedia.org/wiki/Infinite_monkey_theorem
[Kristopher Gindlesperger]: https://kgindle.com
[Monkany Labs]: https://monkany.com
[Monkeyfile]: #monkeyfile
[Planning Issues]: https://github.com/kgindle/monkey/labels/planning
[Ready Issues]: https://github.com/kgindle/monkey/labels/ready
