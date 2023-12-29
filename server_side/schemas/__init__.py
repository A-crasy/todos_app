import graphene
from graphene import relay, Field, String, ObjectType ,Int
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from db import (
    User as UserDBModel,
    Todo as PostDBModel,
    session
)


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = UserDBModel
        interfaces = (relay.Node,)


class PostSchema(SQLAlchemyObjectType):
    class Meta:
        model = PostDBModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_users = SQLAlchemyConnectionField(UserSchema.connection)

    all_posts = SQLAlchemyConnectionField(PostSchema.connection)





class UserMutation(graphene.Mutation):

    class Arguments:
        id = graphene.String()
        ids = graphene.String()
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(lambda: UserSchema)

    def mutate(self, info,id,ids, username, email,password):
        user = UserDBModel(
            id = id ,
            ids = ids  ,
            username=username,
            email=email ,
            password  = password
        )

        session.add(user)
        session.commit()

        return UserMutation(user=user)


class PostMutation(graphene.Mutation):
    class Arguments:
        ids = graphene.Int()
        id = graphene.Int()
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        date = graphene.String(required=True)
        time = graphene.String(required=True)
        status = graphene.String(required=True)
        user_id = graphene.String(required=True)

    post = graphene.Field(lambda: PostSchema)

    def mutate(self, info,ids,id, user_id, title, content,date,time,status):
        new_post = PostDBModel(
            ids = ids ,
            id = id ,
            title=title,
            content=content,
            date = date,
            time = time,
            status = status,
            user_id = user_id
        )

        session.add(new_post)
        session.commit()

        return PostMutation(post=new_post)


class Mutation(graphene.ObjectType):
    mutate_user = UserMutation.Field()
    mutate_post = PostMutation.Field()










schema = graphene.Schema(query=Query, mutation=Mutation)