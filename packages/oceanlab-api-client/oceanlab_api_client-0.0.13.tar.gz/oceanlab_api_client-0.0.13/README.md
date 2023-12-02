# OceanLab API Python Client

## Description
A client library for accessing OceanLab's TIBCO Data Virtualization REST API. 

## Installation
A Python package of the library is published on the Python Package Index (PyPI): https://pypi.org/project/oceanlab-api-client/ 

To install it: 
```
pip install oceanlab-api-client
```

## Usage

See the documentation on https://oceanlab.pages.sintef.no/documentation/ for examples of usage.

## Contributing

### When the API has changed
When the underlying OceanLab API changes, the client needs to follow suit. The client library is generated from the OceanLab API's OpenAPI specification using the CLI tool [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client).


#### Update generated library
1. Install v0.15.0 of the `openapi-python-client` tool [as described in their documentation](https://github.com/openapi-generators/openapi-python-client#installation).
1. Download the latest OpenAPI specification for the OceanLab API. It can be retrieved at `https://api-dev.oceanlab.sintef.no/rest/webservice.json`. See [How to query the OceanLab API](https://gitlab.sintef.no/oceanlab/documentation/-/wikis/How-to-query-the-OceanLab-API) for how to authenticate to the API.
1. Navigate to your local OceanLab API Python Client repository in a terminal. 
1. Copy the `webservice.json` OpenAPI specification to the repo, overwriting the one that's already there. Replace all occurences of `".` with `"` to remove the leading period (`.`).
1. Navigate one level up from the repository and run the following command: `openapi-python-client update --config oceanlab-api-python-client/openapi-python-client/config.yaml  --path oceanlab-api-python-client/webservice.json  --custom-template-path=oceanlab-api-python-client/openapi-python-client`. 
    <details>
    <summary><b>Resolution for warning messages</b></summary>

    If you get a warning when you generate the client, similar to `Cannot parse response for status code 200 (Attempted to generate duplicate models with name "RawDataResponse200"), response will be ommitted from generated client`, it is because there are endpoints with the same Operation ID. Edit `webservice.json` so that all the values with key "`operationId`" are unique.

    If you get a warning similar to `Cannot parse response for status code 200 (Attempted to generate duplicate models with name "RawDataResponse200ResponseResultItem"), response will be ommitted from generated client`, this is because of an [open bug](https://github.com/openapi-generators/openapi-python-client/issues/781). Replace all occurences of the key "field" in webservice.json with e.g. "attr_field".
    </details>
1. Increase the package version number in `pyproject.toml`.

The CI/CD pipeline will automatically publish the new version to the package repository, when the change is merged into main. 

**Important: Update the user documentation and examples to reflect the changes to the API.**

At the time of writing we are using version v0.15.0 of `openapi-python-client`. To upgrade the project to use a newer version of the tool to generate the library, note that you need to swap out the Jinja2 templates in the `openapi-python-client` folder with the newer version's templates and re-implement the project specific modifications. To find the project specific modifications, diff the original v0.15.0 templates (on GitHub) with the ones in this project. Be mindful that upgrading to a newer version of `openapi-python-client` may possibly introduce changes that require updating the usage guides.

### Adding new features
To add new features to the client, modify the relevant Jinja2 templates inside the `openapi-python-client` directory in the repository and update the library (see "Update generated library" section above). 

You might find it easiest to first modify the actual `*.py` files during development and testing, then replicate these changes in the Jinja2 template(s) and run the update command. Confirm that the generated code after running the update command is equal to the changes you made. Make sure to commit or otherwise save the changes you make before running the update command, so that you don't lose your work when the generator overwrites it!

If a template you need to modify is missing from the `openapi-python-client` directory, you can obtain it in the [source code of the relevant version of openapi-python-client (v0.15.0)](https://github.com/openapi-generators/openapi-python-client/tree/v0.15.0/openapi_python_client/templates). Commit the original template version before committing your modifications. 
