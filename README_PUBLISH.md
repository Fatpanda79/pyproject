# Publishing to PyPI

This guide explains how to publish `car-rental-api` to PyPI.

## Prerequisites

1. **Create a PyPI Account**: Register at [pypi.org](https://pypi.org/account/register/)

2. **Create an API Token**: 
   - Go to Account Settings → API tokens
   - Create a new token with scope "Entire account"
   - Save it securely

3. **Install build tools**:
   ```bash
   pip install build twine
   ```

## Steps to Publish

### 1. Update version in `pyproject.toml`
Edit the version field:
```toml
[project]
version = "1.0.0"
```

### 2. Update your email in `pyproject.toml`
Replace the placeholder email:
```toml
authors = [
    {name = "Fatpanda79", email = "your-email@example.com"}
]
```

### 3. Build the package
```bash
python -m build
```
This creates distribution files in `dist/` directory.

### 4. Upload to PyPI
```bash
python -m twine upload dist/*
```
- When prompted for username, enter: `__token__`
- When prompted for password, enter your API token

### 5. Verify your package
Visit: `https://pypi.org/project/car-rental-api/`

## After Publishing

Users can install your package with:
```bash
pip install car-rental-api
```

### Running the server
```bash
python -m uvicorn car_rental_api.api_server:app --reload
```

### Running the client
```bash
python -m car_rental_api.api_client
```

## Updating the Package

To release a new version:
1. Update the version in `pyproject.toml`
2. Run `python -m build`
3. Run `python -m twine upload dist/*`

## Troubleshooting

- **403 Forbidden**: Check your API token is correct
- **Package name already exists**: Choose a different name in `pyproject.toml`
- **Invalid files**: Ensure all Python files have no syntax errors

## Resources

- [PyPI Help](https://pypi.org/help/)
- [setuptools Documentation](https://setuptools.pypa.io/)
- [twine Documentation](https://twine.readthedocs.io/)
