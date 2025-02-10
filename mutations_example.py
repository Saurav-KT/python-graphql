from graphene import Schema, ObjectType, String, Int, Field, List, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


# add the new record
class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, name, age):
        user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)


# edit the existing record
class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id, name=None, age=None):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break
        if not user:
            return None
        if name is not None:
            user["name"] = name
        if age is not None:
            user["age"] = age

        return UpdateUser(user=user)


class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    user = Field(UserType)

    def mutate(root, info, user_id):
        user = None
        for idx, u in enumerate(Query.users):
            if u["id"] == user_id:
                user = u
                del Query.users[idx]
                break

        if not user:
            return None
        return DeleteUser(user=user)


class Query(ObjectType):
    user = Field(UserType, user_id=Int())

    # Dummy data store
    users = [
        {"id": 1, "name": "Saurav", "age": 30},
        {"id": 2, "name": "Sai", "age": 18},
        {"id": 3, "name": "Samba", "age": 28},
        {"id": 4, "name": "Karthik", "age": 28}
    ]

    @staticmethod
    def resolve_user(root, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        if matched_users:
            return matched_users[0]


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = Schema(query=Query, mutation=Mutation)
gql_query = '''
query {
    user(userId:1)
    {
    id
    name
    age
    }
}
'''

# create user query
# gql = '''
# mutation {
#     createUser(name:"Priya", age:28)
#     {
#    user{
#    id
#    name
#    age
#    }
#     }
# }
# '''

# update user query
# gql_update = '''
# mutation {
#     updateUser(userId:1,name:"Updated User", age:49)
#     {
#    user{
#    id
#    name
#    age
#    }
#     }
# }
# '''

# update user query
gql_delete = '''
mutation {
    deleteUser(userId:1)
    {
   user{
   id
   name
   age
   }
    }
}
'''

if __name__ == "__main__":
    result = schema.execute(gql_query)
    print(result)
    result = schema.execute(gql_delete)
    print(result)
    result = schema.execute(gql_query)
    print(result)
