# Crudantic

A simple persistence library for [Pydantic](https://docs.pydantic.dev/latest/) that uses Google Cloud Datastore (Firestore in Datastore mode) as its default backend.

Ideally suited for developers using Pydantic on GCP with cloud functions or other serverless infrastructure like CloudRun.

Because sometimes you don't need a relational database or fully featured ORM; you just need to stash and grab objects while preserving type safety in your code.

## Status

This is an alpha-preview with a minimal featureset:

- CRUD operations on objects
- Support for nested objects/entities via embedding
- Simple listing of objects by entity kind
- Backend is Google Cloud Firestore in Datastore mode

## Installation

```
pip install crudantic
```

Note: Intermittent issues with `pypi.org` registrations, the library is available from github via: `pip install TBS`

In the meantime, clone this repo and install from there.

## Usage

See `examples`

## Developing / Contributing

I'm happy to review pull requests for bug fixes and new functionality.

To develop on the library:

```
git clone git@github.com:dbb613/crudantic.git
cd crudantic
git checkout development
poetry install
poetry build
```

## Missing/Future Features

- Advanced configuration
- Nested objects are always embedded in the parent entity.
- Additional nested object strategies are planned:
  - Ancestor/descendant entity instances
  - Related top-level entity instances
- Transactions
- Schema versioning
- Enfore validate on Create/Save
- Filtering/Querying
- Bulk data migration
