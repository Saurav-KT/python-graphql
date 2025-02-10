from graphene import Schema, ObjectType, String

schema = Schema()
ggl = '''
{
hello(name:"text")
}
'''


class Query(ObjectType):
    hello = String(name=String(default_value="world"))

    def resolve_hello(self,info, name):
        return f"Hello {name}"


schema = Schema(query=Query)

if __name__ == "__main__":
    result = schema.execute(ggl)
    print(result)
