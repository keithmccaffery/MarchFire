#!/bin/bash

# Start of the script
echo "$(date) - Starting sync of final.db to Azure File Share..."

# Replace these variables with your actual Azure storage account details and local file path
storage_account_name=firstfire

share_name=finaldatabase
source_file_path=/app/final.db
destination_file_path=final.db # The path where the file will be stored in the Azure File Share

# Attempt to upload the file
if az storage file upload --account-name $storage_account_name --account-key $storage_account_key --share-name $share_name --source $source_file_path --path $destination_file_path; then
    echo "$(date) - Successfully synced final.db to Azure File Share."
else
    echo "$(date) - Error: Failed to sync final.db to Azure File Share." >&2
fi

# End of the script
echo "$(date) - Sync script completed."