# Python Client to call Inferless API

## Installation
```console
$ pip install inferless
```

## Usage
This client can be used to call Inferless API from your python code. It supports both synchronous and asynchronous calls.
### Constants
Fetch the URL and API_KEY from the Inferless console https://console-dev.inferless.com/
```python
URL = "<url>"
API_KEY = "<api_key>"
data = { "inputs" : 
          [
              {
                "name": "prompt",
                "shape": [
                  1
                ],
                "datatype": "BYTES",
                "data": [
                  "Once upon a time"
                ]
              }
          ]
        }
```

### Synchrounous call
An example to call Inferless API synchronously
```python
import inferless
import datetime
def main():
    t1 = datetime.datetime.now()
    data = inferless.call(URL, API_KEY, data)
    t2 = datetime.datetime.now()
    print(f"time taken: {t2-t1}")

main()
```
Output
```console
time taken: 0:00:05.218835
```
For a particular url, the synchronous call took approximately 5 seconds to complete.

### Asynchronous call
An example to call Inferless API asynchronously
```python
import inferless
import asyncio
import datetime
async def main():
    t1 = datetime.datetime.now()
    task = asyncio.create_task(inferless.async_call(URL, API_KEY, data))
    # You can implement any other async methods here while this call is being executed
    await asyncio.sleep(3)
    data = await asyncio.gather(task)
    t2 = datetime.datetime.now()
    print(f"time taken: {t2-t1}")

asyncio.run(main())
```
Output
```console
time taken: 0:00:05.646579
```
For the same url, the asynchronous call also took 5 seconds to complete despite the fact that we have added a 3 second delay in the code. This is because the call to Inferless API is being executed asynchronously while the other code is being executed.