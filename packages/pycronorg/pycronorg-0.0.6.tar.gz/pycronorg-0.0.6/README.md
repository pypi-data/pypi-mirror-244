## py-cron-org

A simple sdk for cron-job.org


### Installation

```bash
pip3 install pycronorg
```


### Usage

```python
>>> import os
>>> from dotenv import load_dotenv
>>> from pycronorg.sync import JobsApi
>>> 
>>>  
>>> assert load_dotenv()  
>>> token = os.environ['CRON_ORG_TOKEN']
>>> api = JobsApi(token)

#-------------------------------------create-------------------------------------
>>> job = api.create(
...      api.Schema(
...         title='hi, cron-job.org',
...         url='http://example.com',
...         scheldule=api.SchelduleSchema(
...             hours=[12],
...             minutes=[0],
...         ),
...     )
... )

#------------------------------------get-job-------------------------------------
>>> assert api.get(job.jobId)

#-------------------------------------update-------------------------------------
>>> api.update(
...     api.SchemaUpdate(
...         jobId=job.jobId,
...         scheldule=api.SchelduleSchema(
...             hours=[13],
...             minutes=[0],
...         )
...     )
... )

#--------------------------------retrieve-history--------------------------------
>>> history = api.retrive_history(job.jobId)

#------------------------------------get-all-------------------------------------
>>> jobs = api.all()

#-------------------------------------delete-------------------------------------
>>> api.delete(job.jobId)
>>> 
>>> 

```

## Contributing
We welcome contributions from the developer community to improve the Wallex SDK. If you are interested in contributing to the Wallex SDK, please follow the steps below:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes in your branch.
4. Write tests to ensure the changes are working as expected.
5. Submit a pull request with your changes.

## License
The Wallex SDK is licensed under the [MIT License](LICENSE).

