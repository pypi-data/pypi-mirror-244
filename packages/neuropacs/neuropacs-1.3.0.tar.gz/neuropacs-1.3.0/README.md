# NeuroPACS Python SDK

## Install neuropacs from pip

```bash
pip install neuropacs
```

## Usage

```py
import neuropacs

api_key = "user_api_key"
server_url = "https://your_neuropacs_url"
product_id = "PD/MSA/PSP-v1.0"
prediction_format = "XML"

# PRINT CURRENT VERSION
version = neuropacs.PACKAGE_VERSION

#INITIALIZE NEUROPACS SDK
npcs = neuropacs.init(api_key, server_url)

#GENERATE AN AES KEY
aes_key = npcs.generate_aes_key()

#CONNECT TO NEUROPACS
connection_id = npcs.connect(api_key, aes_key)

#CREATE A NEW JOB
order_id = npcs.new_job(connection_id, aes_key)

#UPLOAD AN IMAGE (image can be a path or byte array)
upload_status = npcs.upload(image, order_id, connection_id, aes_key)

#UPLOAD A DATASET
upload_status = npcs.upload_dataset("your/dataset/path",connection_id, order_id, aes_key)

#START A JOB
job_start_status = npcs.run_job(connection_id, aes_key, product_id, order_id)

#CHECK JOB STATUS
job_status = npcs.check_status(order_id, connection_id, aes_key)

#RETRIEVE JOB RESULTS
job_results = npcs.get_results(prediction_format, order_id, connection_id, aes_key)
```
