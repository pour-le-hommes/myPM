import requests
import os

def get_goals(iteration:int):
    vercel_header = os.getenv("VERCEL_BACKEND_BYPASS")

    header = {
        "x-vercel-protection-bypass":vercel_header
    }

    resp = requests.get(f"https://personal-backend-eight.vercel.app/lifeup/tasks/{iteration}/sprint_goals", headers=header)

    if resp.status_code == 200:
        # Decode the response content to a string
        content = resp.content.decode('utf-8')
        
        return content


def get_tasks(iteration:int):
    vercel_header = os.getenv("VERCEL_BACKEND_BYPASS")

    header = {
        "x-vercel-protection-bypass":vercel_header
    }

    resp = requests.get(f"https://personal-backend-eight.vercel.app/lifeup/tasks/{iteration}/tasks", headers=header)

    if resp.status_code == 200:
        # Decode the response content to a string
        content = resp.content.decode('utf-8')
        
        return content