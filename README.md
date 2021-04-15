# blob-trigger-strip-icc-profile

This function will triger on input blobs, load them as images with Pillow, convert to RGB as necessary and strip away embedded ICC profiles.

To run in Azure Functions, fill in `AzureWebJobsStorage` app setting with the connection string to your storage account. The input container name is `input`. You can amend it in the `functions.json`.

To run locally, create a `local.settings.json` with the following content -
```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "YOUR_AZURE_STORAGE_CONNECTION_STRING"
  }
}
```