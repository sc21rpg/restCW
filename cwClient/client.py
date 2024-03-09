import requests
from urllib.parse import urlencode
# URL of your Django server
base_url = ''
#http://localhost:8000
# Create a session
session = requests.Session()

def login(baseUrl):
    global base_url
    base_url = baseUrl
    # Ask the user for their username and password
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    # Endpoint for the login service
    url = f'{base_url}/api/login'
    
    # Data to be sent to the server
    data = urlencode({'username': username, 'password': password})
    
    # Headers for the request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    # Send a POST request to the server
    response = session.post(url, data=data, headers=headers)
    
    # If the request was successful, print the welcome message
    if response.status_code == 200:
        print(response.text)
    else:
        print('Login failed:', response.text)    

def logout():
    global base_url
    # Endpoint for the logout service
    url = f'{base_url}/api/logout'
    
    # Send a POST request to the server
    response = session.post(url)
    
    # If the request was successful, print the goodbye message
    if response.status_code == 200:
        print(response.text)
        base_url = ''
    else:
        print('Logout failed:', response.text)
        
def post_story():
    # Ask the user for the story details
    headline = input('Enter the headline: ')
    category = input('Enter the category (pol, art, tech, trivia): ')
    region = input('Enter the region (uk, eu, w): ')
    details = input('Enter the details: ')

    # Validate the inputs
    if len(headline) > 64 or len(details) > 128:
        print('Headline and details must be under 64 and 128 characters respectively.')
        return
    if category not in ['pol', 'art', 'tech', 'trivia']:
        print('Invalid category. Choose from pol, art, tech, trivia.')
        return
    if region not in ['uk', 'eu', 'w']:
        print('Invalid region. Choose from uk, eu, w.')
        return

    # Endpoint for the post story service
    url = f'{base_url}/api/stories'
    
    # Data to be sent to the server
    data = {
        'headline': headline,
        'category': category,
        'region': region,
        'details': details,
    }
    
    # Send a POST request to the server
    response = session.post(url, json=data)
    
    # If the request was successful, print the success message
    if response.status_code == 201:
        print('Story posted successfully.')
    else:
        print('Failed to post story:', response.text)

        

def get_stories():
    # Prompt the user for category
    category = input("Enter the category (or press Enter for all categories): ")
    if category == "":
        category = "*"

    # Prompt the user for region
    region = input("Enter the region (or press Enter for all regions): ")
    if region == "":
        region = "*"

    # Prompt the user for date
    date = input("Enter the date (in dd/mm/yyyy format, or press Enter for all dates): ")
    if date == "":
        date = "*"

    url = f"{base_url}/api/stories?story_cat={category}&story_region={region}&story_date={date}"
    response = session.get(url)

    if response.status_code == 200:
        stories = response.json()['stories']
        for story in stories:
            print(f"Headline: {story['headline']}")
            print(f"Category: {story['story_cat']}")
            print(f"Region: {story['story_region']}")
            print(f"Author: {story['author']}")
            print(f"Date: {story['story_date']}")
            print(f"Details: {story['story_details']}")
            print('---')
    else:
        print('Failed to retrieve stories:', response.text)

def list_services():
    pass
def get_news():
    pass

def delete_story(key):

    # Endpoint for the delete story service
    url = f'{base_url}/api/stories/{key}'

    # Send a DELETE request to the server
    response = session.delete(url)

    # If the request was successful, print the success message
    if response.status_code == 200:
        print('Story deleted successfully.')
    else:
        print('Failed to delete story:', response.text)

def main():
    while True:
        print('login')
        print('logout')
        print('post')
        print('news')
        print('list')
        print('delete')
        print('Exit')
        choice = input('Enter your choice: ')
        words = choice.split()
        if len(words) == 1:
            if choice == "logout":
                logout()
            elif choice == "post":
                post_story()
            elif choice == "list":
                list_services()
            elif choice == "exit":
                break
            else:
                print('Invalid choice. Please try again.')
        elif len(words) == 2:
            if words[0] == "login":
                login(words[1])
            elif words[0] == "delete":
                delete_story(words[1])
            else:
                print('Invalid choice. Please try again.')

        elif len(words) == 5:
            if words[0] == "news":
                get_news(words[1], words[2], words[3], words[4])
            else:
                print('Invalid choice. Please try again.')
        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()


