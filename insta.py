
import instaloader
import tkinter as tk

def get_profile_details():
    # Get the username from the entry widget
    username = entry.get()

    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    # Load a profile by username
    profile = instaloader.Profile.from_username(loader.context, username)

    # Clear the text widget
    text.delete(1.0, tk.END)

    # Display the profile details
    text.insert(tk.END, f"Username: {profile.username}\n")
    text.insert(tk.END, f"Full Name: {profile.full_name}\n")
    text.insert(tk.END, f"Bio: {profile.biography}\n")
    text.insert(tk.END, f"Followers: {profile.followers}\n")
    text.insert(tk.END, f"Following: {profile.followees}\n")

    # Scrape and display followers
    text.insert(tk.END, "Followers:\n")
    for follower in profile.get_followers():
        text.insert(tk.END, f"{follower.username}\n")

    # Scrape and display followees (people the profile is following)
    text.insert(tk.END, "Following:\n")
    for followee in profile.get_followees():
        text.insert(tk.END, f"{followee.username}\n")

# Create a tkinter window
window = tk.Tk()
window.title("Instagram Profile Details")

# Create a label and entry widget for username input
label = tk.Label(window, text="Enter Username:")
label.pack()
entry = tk.Entry(window)
entry.pack()

# Create a button to get profile details
button = tk.Button(window, text="Get Details", command=get_profile_details)
button.pack()

# Create a text widget to display the profile details
text = tk.Text(window)
text.pack()

# Start the tkinter event loop
window.mainloop()
loader = instaloader.Instaloader()

# Login to Instagram (optional)
# loader.login("your_username", "your_password")

# Load a profile by username
profile = instaloader.Profile.from_username(loader.context, "rvcjinsta")

# Print basic profile information
print("Username:", profile.username)
print("Full Name:", profile.full_name)
print("Bio:", profile.biography)
print("Followers:", profile.followers)
print("Following:", profile.followees)

# Scrape and print followers
print("Followers:")
for follower in profile.get_followers():
    print(follower.username)

# Scrape and print followees (people the profile is following)
print("Following:")
for followee in profile.get_followees():
    print(followee.username)