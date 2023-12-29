import requests
import json

# Replace this URL with the endpoint of your Flask GraphQL API
graphql_endpoint = "http://127.0.0.1:5000/graphql"

# Define your GraphQL query
graphql_query = """
query{
  allUsers{
    edges{
      node{
        ids
        username
        password
      }
    }
  }
}
"""
graphql_query2 = """
query{
  allPosts{
    edges{
      node{
        id
        ids
        title
        content
        date
        time 
        status
        userId
      }
    }
  }
}
"""

def fetch_data_from_graphql_api(query):
    # Define the GraphQL request headers
    headers = {
        "Content-Type": "application/json",
    }

    # Prepare the GraphQL request payload
    payload = {
        "query": query
    }

    try:
        # Send the GraphQL POST request
        response = requests.post(graphql_endpoint, headers=headers, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)
            return data
        else:
            # Print the error message if the request was not successful
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e}")
        return None

def user_checker(username,password,results) :
    for  x in results :
        if x['node']['username'] == username and x['node']['password'] == password :
            return  x['node']
    return False


def addtodo(id,ids,title,content,dates,time,status,userid) :
    querys = """mutation{
  mutatePost(id:%s,ids:%s,title:"%s",content:"%s",date:"%s",time:"%s",status:"%s",userId:"%s"){
    post{
      ids
    }
  }
}
    """
    k = querys%(id,ids,title,content,dates,time,status,userid)
    print(k)
    return fetch_data_from_graphql_api(k)


