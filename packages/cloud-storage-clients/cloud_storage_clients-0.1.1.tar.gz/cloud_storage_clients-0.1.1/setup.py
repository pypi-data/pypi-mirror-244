# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloud_storage_clients',
 'cloud_storage_clients.azure',
 'cloud_storage_clients.gcs',
 'cloud_storage_clients.repositories',
 'cloud_storage_clients.s3']

package_data = \
{'': ['*']}

install_requires = \
['azure-identity>=1.15.0,<2.0.0',
 'azure-storage-blob>=12.19.0,<13.0.0',
 'boto3>=1.33.1,<2.0.0',
 'google-cloud-storage>=2.13.0,<3.0.0',
 'hvac>=1.2,<2.0']

setup_kwargs = {
    'name': 'cloud-storage-clients',
    'version': '0.1.1',
    'description': 'Storage clients for different cloud providers',
    'long_description': '## cloud-storage-clients\n\n`cloud-storage-clients` is a Python library for having an unique interface over different cloud storage providers.\nIt can be used to connect a python client to providers.\nThis package is maintained by [Picsellia](https://fr.picsellia.com/).\n\nThis has been conceived for you to override classes.\nFor example, override VaultRepository if you retrieve credentials in another way.\nYou can create or override factories of client to add some additional parameters.\n\n## Installation\n\nAdd it to your [poetry](https://python-poetry.org/)  environment\n```bash\npoetry add cloud-storage-clients\n```\n\nOr use the package manager [pip](https://pip.pypa.io/en/stable/) to install it.\n```bash\npip install cloud-storage-clients\n```\n\n## Usage\n\n### Basic client usage to retrieve a specific object name from an S3 bucket\n```python\nfrom cloud_storage_clients.connector import Connector\nfrom cloud_storage_clients.s3.client import S3Client\n\nconnector = Connector(client_type="s3", bucket="my-bucket")\n\nclient = S3Client(connector, {"access_key_id": "access-key", "secret_access_key": "secret-access-key" })\n\nwith open("/path/object-name.jpg", "wb") as file:\n    response = client.get("object-name.jpg")\n    file.write(response.content)\n\n```\n\n### Pool Instanciation\n```python\nfrom cloud_storage_clients.connector import Connector\nfrom cloud_storage_clients.s3.factory import S3ClientFactory\nfrom cloud_storage_clients.repositories.vault_adapter import DefaultVaultAdapter, TokenCredentials\nfrom cloud_storage_clients.repositories.vault import VaultCredentialRepository\nfrom cloud_storage_clients.pool import ClientPool\n\n# Login to your Vault by creating a VaultAdapter and its repository\nvault_adapter = DefaultVaultAdapter(\n    url="http://localhost:7200",\n    credentials=TokenCredentials(token="vault_token", unseal_key="unseal_key")\n)\nrepository = VaultCredentialRepository(adapter=vault_adapter)\n\n# Instantiate a ClientPool and add an S3ClientFactory for minio client_type\npool = ClientPool(default_repository=repository)\npool.register_factory("minio", factory=S3ClientFactory())\n\n# Create a connector object\nconnector = Connector(client_type="minio", bucket="my-bucket")\n\n# Use pool to instantiate a client that have its credentials in Vault\nclient = pool.get_client(connector)\n\n# Generate a presigned url that an user without access to your bucket can download\npresigned_url = client.get_download_url("object-name", 3600).url\n\n\n\n```\n',
    'author': 'picsellia',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
