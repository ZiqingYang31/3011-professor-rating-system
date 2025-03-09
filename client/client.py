current_user_token = None
import requests

session = requests.Session() 
BASE_URL = "http://127.0.0.1:8000/rating/"  

def register():

    global BASE_URL

    url = BASE_URL + "register/"
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    data = {"username": username, "email": email, "password": password}
    try:
        response = session.post(url, json=data)
        response.raise_for_status()  
        data = response.json()
        if response.status_code == 201:
            print("Registration successful!")
            login()
        else:
            print("Registration failed. Error:", data.get("error", "Unknown error"))
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"JSON decode error occurred: {json_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def login():

    global current_user_token, BASE_URL
    
    url = input("Enter service URL (e.g., sc22zy.pythonanywhere.com or http://127.0.0.1:8000/rating/): ").strip()
    
    if not url.startswith("http"):
        url = "http://" + url 

    if not url.endswith("/"):
        url += "/"

    BASE_URL = url 
    login_url = BASE_URL + "api-token-auth/"

    username = input("Enter username: ")
    password = input("Enter password: ")

    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(login_url, json=data)
        response_data = response.json()
        
        if response.status_code == 200:
            current_user_token = response_data.get("token")
            print("Login successful! Token:", current_user_token)
        else:
            print("Login failed. Error:", response_data.get("error", "Unknown error"))

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Check if the URL is correct and the server is running.")
    except requests.exceptions.JSONDecodeError:
        print("Error: Server did not return JSON. Response:", response.text)


def logout():

    global session, current_user_token
    session = requests.Session()  
    current_user_token = None 
    print("Logged out successfully!")


def list_module_instances():

    global BASE_URL
    url = BASE_URL + "module-instances/"
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        print("Code\tName\tYear\tSemester\tTaught by")
        for instance in data:
            professors = ", ".join([prof["name"] for prof in instance["professors"]])
            print(f"{instance['module']['code']}\t{instance['module']['name']}\t{instance['year']}\t{instance['semester']}\t{professors}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"JSON decode error occurred: {json_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def view_professor_ratings():
    global BASE_URL
    url = BASE_URL + "professors/ratings/" 
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = session.get(url, headers=headers)  
        response.raise_for_status()  
        ratings = response.json() 
        for rating in ratings:
            avg_rating = rating['average_rating']
            if avg_rating is not None and avg_rating != 'No Ratings':
                try:
                    avg_rating = int(avg_rating)  
                    print(f"The rating of Professor {rating['name']} ({rating['id']}) is {'*' * avg_rating}")
                except ValueError:
                    print(f"Invalid rating data for Professor {rating['name']} ({rating['id']}).")
            else:
                print(f"The rating of Professor {rating['name']} ({rating['id']}) is No Ratings")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        print(f"Request URL: {url}")  
        print(f"Response: {err.response.text if err.response else 'No response'}") 


def view_average_rating():
    """
    查看某教授在某课程的平均评分
    """
    global BASE_URL
    professor_id = input("Enter professor ID: ")
    module_code = input("Enter module code: ")

    url = BASE_URL + f"professors/{professor_id}/modules/{module_code}/average/"
    print(f"Request URL: {url}") 

    headers = {
        "Authorization": f"Token {current_user_token}", 
        "Content-Type": "application/json"
    }

    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"The average rating of Professor {data['professor_name']} in module {data['module_name']} is {data['average_rating']}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"JSON decode error occurred: {json_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def rate():
    global current_user_token, BASE_URL
    if not current_user_token:
        print("You need to log in first!")
        return
    print(f"Current Token: {current_user_token}")

    professor_id = input("Enter professor ID: ").strip()
    module_code = input("Enter module code: ").strip()
    year = input("Enter teaching year: ").strip()
    semester = input("Enter semester: ").strip()

    rating = input("Enter rating (1-5): ").strip()
    if rating not in ["1", "2", "3", "4", "5"]:
        print("Invalid rating! Please enter a number between 1 and 5.")
        return

    instance_url = f"{BASE_URL}module-instances/"
    try:
        response = session.get(instance_url)
        response.raise_for_status()
        module_instances = response.json()
        module_instance_id = None

        for instance in module_instances:
            if (instance["module"]["code"] == module_code and 
                str(instance["year"]) == year and 
                str(instance["semester"]) == semester):
                module_instance_id = instance["id"]
                break

        if module_instance_id is None:
            print("No matching module instance found. Check your input.")
            return

        rating_url = BASE_URL + "ratings/"
        headers = {
            "Authorization": f"Token {current_user_token}",
            "Content-Type": "application/json"
        }

        data = {
            "professor": professor_id,
            "module_instance": module_instance_id,  
            "rating": int(rating)
        }

        response = session.post(rating_url, json=data, headers=headers)

        if response.status_code == 400:
            response_data = response.json()
            print(f"Failed to submit rating. Error: {response_data.get('detail', 'Unknown error')}")
            return

        response.raise_for_status()
        response_data = response.json()

        if response.status_code == 201:
            print("Rating submitted successfully!")
        else:
            print("Failed to submit rating. Error:", response_data)
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")



def main():
    global BASE_URL

    while True:
        print("\nCommands:")
        print("1. register")
        print("2. login")
        print("3. logout")
        print("4. list - View all modules and professors")
        print("5. view - View ratings of all professors")
        print("6. average - View average rating of a professor in a module")
        print("7. rate - Rate a professor in a module instance")
        print("8. exit")
        command = input("Enter command: ").strip().lower()

        if command == "register":
            register()
        elif command == "login":
            login()
        elif command == "logout":
            logout()
        elif command == "list":
            list_module_instances()
        elif command == "view":
            view_professor_ratings()
        elif command == "average":
            view_average_rating()
        elif command == "rate":
            rate()
        elif command == "exit":
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()