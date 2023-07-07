# Commerce Web App

This is a Django web application for an auction site called "Commerce". It allows users to create auction listings, place bids, add items to their watchlist, and comment on listings.

## Setup

1. Install the necessary dependencies by running `pip install -r requirements.txt`.

2. Apply database migrations by running `python manage.py migrate`.

3. Create a superuser account to access the Django admin interface by running `python manage.py createsuperuser`.

4. Start the Django development server with `python manage.py runserver`.

5. Access the web application by visiting `http://localhost:8000` in your browser.

## Features

- **Models**: The application includes models for auction listings, bids, comments, and user accounts.

- **Create Listing**: Users can create new auction listings by providing a title, description, starting bid, and optional image URL and category.

- **Active Listings Page**: The default route displays all currently active auction listings. Each listing shows its title, description, current price, and photo (if available).

- **Listing Page**: Clicking on a listing shows the details of that listing, including the current price. Signed-in users can add the item to their watchlist and place bids.

- **Watchlist**: Signed-in users can view their watchlist, which displays the listings they have added. Clicking on a listing takes the user to its specific page.

- **Categories**: Users can browse listings by category. Clicking on a category name shows all active listings in that category.

- **User Authentication**: The application includes user registration, login, and logout functionality. Certain actions, such as bidding or closing auctions, are restricted to authenticated users.

- **Django Admin Interface**: Administrators can manage listings, comments, and bids through the Django admin interface.
  
## Acknowledgements

This web application was developed as part of the CS50 Web Programming with Python and JavaScript course.
