import requests
import os

vercel_header = os.getenv("VERCEL_BACKEND_BYPASS")

def get_goals(iteration:int):
    header = {
        "x-vercel-protection-bypass":vercel_header
    }

    resp = requests.get(f"{os.getenv('MY_BACKEND_WEBSITE')}/lifeup/tasks/{iteration}/sprint_goals", headers=header)

    if resp.status_code == 200:
        # Decode the response content to a string
        content = resp.content.decode('utf-8')
        
        return content


def get_tasks(iteration:int):

    header = {
        "x-vercel-protection-bypass":vercel_header
    }

    resp = requests.get(f"{os.getenv('MY_BACKEND_WEBSITE')}/lifeup/tasks/{iteration}/tasks", headers=header)

    if resp.status_code == 200:
        # Decode the response content to a string
        content = resp.content.decode('utf-8')
        
        return content