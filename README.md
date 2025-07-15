# 🛒 Django Auctions Platform

A fully functional online auction website built with Django. Users can create listings, place bids, add comments, manage watchlists, and browse by category. This project fulfills all requirements of the CS50 Web Programming Auction Project.

## 🚀 Features

- 🔐 **User Authentication**  
  Register, login, and logout with Django's authentication system.

- 📝 **Create Listings**  
  Users can create auction listings with title, description, starting bid, image URL, and category.

- 📋 **Active Listings Page**  
  Homepage shows all currently active listings with photo, price, and description.

- 📦 **Listing Detail Page**  
  View full listing details, place bids, add/remove from watchlist, leave comments, or close auction if you're the creator.

- 💰 **Bidding System**  
  Enforces bidding rules: new bids must be higher than all previous bids and at least equal to the starting bid.

- 🏆 **Auction Close & Winner Logic**  
  Listing owners can close auctions. The highest bidder becomes the winner, and winners are shown a success message.

- 💬 **Commenting**  
  Users can leave comments on listing pages.

- 👀 **Watchlist**  
  Users can add or remove listings from a personal watchlist and view them all in one place.

- 🗂️ **Categories**  
  Listings can be categorized. Users can browse listings by category.

- 🛠️ **Admin Interface**  
  Admins can view, edit, and delete listings, bids, and comments through the Django admin panel.

## 🧱 Models

- `User` (extends `AbstractUser`)
- `Listing` (title, description, starting bid, image, category, active, owner, winner)
- `Bid` (user, listing, amount)
- `Comment` (user, listing, content, timestamp)

## 🛠️ Tech Stack

- Python 3
- Django 5
- SQLite (default DB)
- HTML/CSS with Django templates

## 🧪 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/TAsamidinov/Commerce.git
   cd Commerce
