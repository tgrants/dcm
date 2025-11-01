# Contributing

Contributions are welcome.

Before contributing a new feature, please discuss the change you want to make via issue or contact [@tgrants](https://github.com/tgrants) directly.

## Issues

Before creating a new issue, ensure a similar one has not already been created by searching on GitHub under [Issues](https://github.com/tgrants/dcm/issues/).

For reporting vulerabilities, see [SECURITY.md](.github/SECURITY.md).

## Branches

We use the following branch structure:

- **main**: Main branch. Contains releases - working, tested and documented code.
- **dev**: Development branch. Contains working code but it might be less stable.
- **feature/task branches**: New features or fixes should be developed in their own branches.

```
main
└── dev
	├── feat/self-destruct-button
	└── fix/remove-unhinged-comments
```

### Branch Naming Convention

- **Features**: `feat/short-description` (e.g., `feat/self-destruct-button`)
- **Fixes**: `fix/short-description` (e.g., `fix/remove-unhinged-comments`)

## Workflow

- Create a branch for your changes
	- `git checkout -b feat/feature-name`
