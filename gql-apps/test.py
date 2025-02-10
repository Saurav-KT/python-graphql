from graphene import Schema, ObjectType, String, Int, List, Field
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler

# static data
employers_data = [{"id": 1, "name": "Cisco", "contact_email": "test@cisco.com", "industry": "tech"},
                  {"id": 2, "name": "Zee", "contact_email": "test@zee.com", "industry": "Entertainment"},
                  ]
jobs_data = [
    {"id": 1, "title": "software engineer", "description": "develop web & mobile application", "employer_id": 1},
    {"id": 2, "title": "Marketing expert", "description": "Generates sales lead and prepare a report",
     "employer_id": 1},
    {"id": 3, "title": "Accountant", "description": "Manage financial records", "employer_id": 2}
]


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return [job for job in jobs_data if job["employer_id"] == root["id"]]


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(parent, info):
        return next((employer for employer in employers_data if employer["id"] == parent["employer_id"]), None)


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data

    def resolve_employers(root, info):
        return employers_data


schema = Schema(query=Query)

app = FastAPI()
# app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_playground_handler()))
