import aiohttp
import base64
from azure.devops.connection import Connection  
from azure.devops.v7_1.pipelines import PipelinesClient
from msrest.authentication import BasicAuthentication  
from azure.devops.v7_1.build import Timeline
import requests
import base64
import datetime
import pandas as pd
import asyncio
import json
from organize_data import edit_data
pipeline_id=619
pipeline_name = 'Capgemini_Azure_Internal_Release'
# 619 Capgemini_Azure_Internal_Release
# 580 CI_Azure_Internal_Release

pat="4q3nvsjfnf3czqwfb47ivsb62ir4cvnkjwknhjgqhmgtc4h47jza"
project_name = 'Maxwell'  
organization_url = 'https://dev.azure.com/slb2-swt'  
YEAR=2023
MONTH=11
DAY=18

excel_name=pipeline_name+".xlsx"


async def create_excel_schema():
    pd.DataFrame(columns=["create_date","build_id","job","time"]).to_excel(excel_name,index=False)


async def fetch_data(run_id,create_date):
        print(run_id)
        encoded_pat = base64.b64encode((":" + pat).encode()).decode()
        headers = {"Authorization":"Basic "+encoded_pat}
        async with aiohttp.ClientSession() as session:
            url = f"{organization_url}/{project_name}/_apis/build/builds/{run_id}/timeline?api-version=6.0&$orderby=startTime"
            async with session.get(url,headers=headers) as resp:
                print(f"GET ==> {url}")
                data = await resp.json()
                records = data["records"]
                new_data = {}
                new_data["records"] = []
                with open("realtime.json","w") as fp:
                        fp.write(json.dumps(records))
                for record in records:
                    if record["type"] == "Job" and record["name"] != "beforeBuild":
                        record["run_id"] = run_id
                        print(record["name"])
                        print(record["startTime"])
                        print(record["finishTime"])
                        new_data["records"].append(record)
                return new_data

async def get_succeeded_build_info():
    credentials = BasicAuthentication('', pat)  
    connection = Connection(base_url=organization_url, creds=credentials)
    client = PipelinesClient(organization_url,credentials)
    all_runs = client.list_runs(project_name,pipeline_id)
    all_succeed_run_ids=[]
    for run in all_runs:
        print(run)
        if run.state == "completed" and run.result == "succeeded":
            if run.created_date.year >= YEAR and run.created_date.month >= MONTH and run.created_date.day >= DAY:
                print(run)
                all_succeed_run_ids.append({"create_date":run.created_date.strftime("%Y-%m-%d %H:%M"),"id":run.id})
    return all_succeed_run_ids


async def main():
    dataframe=pd.read_excel(excel_name)
    all_succeeded_build_info = await get_succeeded_build_info()
    all_data = await asyncio.gather(*(fetch_data(run_info["id"],run_info["create_date"]) for run_info in all_succeeded_build_info))
    for json_content in all_data:
        records = json_content["records"]
        time_format = "%Y-%m-%dT%H:%M:%S"
        for record in records:
            if record["type"] == "Job" and record["name"] != 'Finalize build':
                if record["startTime"]  and record["finishTime"]:
                    start_time = record["startTime"][:19]
                    end_time = record["finishTime"][:19]
                    start_time = datetime.datetime.strptime(start_time,time_format)
                    end_time = datetime.datetime.strptime(end_time,time_format)
                    time = (end_time-start_time).total_seconds()/3600
                else:
                    time=None
                new_data = {f'startTime':record["startTime"],'build_id': record["run_id"], 'job': record["name"], 'time':time}
                print(new_data)
                dataframe = dataframe._append(new_data, ignore_index=True)
                dataframe.to_excel(excel_name,index=False)

pd.DataFrame(columns=["startTime","build_id","job","time"]).to_excel(excel_name,index=False)

# asyncio.run(create_excel_schema())
asyncio.run(main())


edit_data(file_name=excel_name)