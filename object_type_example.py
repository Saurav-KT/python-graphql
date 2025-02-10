from graphene import Schema, ObjectType, String, Int, Field, List


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())
    # Dummy data store
    users = [
        {"id": 1, "name": "Saurav", "age": 30},
        {"id": 2, "name": "Sai", "age": 18},
        {"id": 3, "name": "Samba", "age": 28}
    ]

    @staticmethod
    def resolve_user(root, info, user_id):
        print(root)
        matched_users = [user for user in Query.users if user["id"] == user_id]
        if matched_users:
            return matched_users[0]

    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]


schema = Schema(query=Query)
# gql = '''
# query {
#     user(userId:2)
#     {
#     id
#     name
#     age
#     }
# }
# '''

gql = '''
query {
    usersByMinAge(minAge:30)
    {
    id
    name
    age
    }
}
'''

if __name__ == "__main__":
    result = schema.execute(gql, root_value="some data source")
    print(result)
