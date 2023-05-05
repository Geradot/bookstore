Bookstore Web App
=================

This test project is positioned as an online bookstore. There are a pure JavaScript, HTML/CSS for the front end and Django — for the back end.

### Database architecture and data management

The principle of data storage and management is as follows:

*   An unauthorized user can view the list of books, as well as see page of a separate book. To add books to the shopping cart, and also, to view their shopping cart, the user needs to log in.
*   Table `Purchase` stores information about purchases (baskets) users. The key field is `paid`, which determines if the cart has been paid. Once the basket is paid, the field `purchase_date` is automatically filled current date. The logic of user purchases is thought out so that one user can have only one active basket (which has `paid=False`).
*   The `Purchase Item` table keeps a record of each book that is in the user's basket (regardless of whether the paid basket or not), in what quantity and for what amount this book was published (taking into account the quantity).
*   The total amount of the entire cart is stored in the previously mentioned table `Purchase`. The logic of working with data provides for recalculation this value every time the user changes some data in the basket (the number of books or their availability at all).

### UX/UI

Below are two components of the frontend code that determine usability. uses of this project are JavaScript and HTML/CSS.

#### The role of JavaScript

The Bookstore uses JavaScript for various tasks and pages to make the experience of using the site comfortable enough. Here are a few examples of where and for what purpose it is used:

*   On the main page above the books there is a panel with a search for books and filters by price/category. The code fully provides for all possible combinations of filters with a search string.
*   On the page of a specific book there is a block for adding a supply to basket. JS code provides:
    *   Correct operation of the `Amount` field. The field is text and is protected from entering any characters other than numbers (instead of non-numeric character in the field is written "1"). If the supply is in the cart, then the field input and the text next to "Amount" contain the value of the amount of this books in a basket. If there are no books in the basket, then the input field contains "1"
    *   Easily change the number of books using the `+` and `-`. They successfully add/subtract the number of books on one per click, and are also blocked if the field contains the maximum or minimum possible number, respectively.
    *   Adding an item to the cart on the click of a button `Add to Cart`. It will be blocked if the field number of books is empty.
    *   The following button logic: if the supply is in the cart (not important whether the user has just added or added before), instead of a button `Add to Cart` buttons appear `Change amount` and `Remove from Cart`. Button `Change amount` changes the number of books in the cart to new value of the Amount field and is blocked by the button principle `Add to Cart` and `Remove from Cart` removes item from the cart, after which these two buttons are removed and the again `Add to Cart`
*   On the user's shopping cart page, there is next to the name of each supply for easy removal from the basket without visiting the page of the book. If all items in the cart will be removed using the delete button or by using button `Purchase` (simulates the purchase process), the empty basket template.
*   The previous purchases overview page shows for user the most popular category of all the books he has purchased, along with the quantity.

#### The role of HTML/CSS

Of course, HTML is mandatory for use on a project, but opportunities use the right semantic tags in the right places. But the main thing that I want to note in appearance is the use of CSS:

*   Flexbox layout and Bootstrap are almost universally used. The site is well adapted to different screens.
*   On a particular book page, the main layout is Grid for convenient _custom_ positioning of blocks when changing screen width

Launching the Web Application
-----------------------------

To get the Bookstore up and running, run the following steps:

1.  Make sure you have installed [Python](https://www.python.org/) versions 3.11+ and [Django](https://www.djangoproject.com/) 4.1+. If you have some problems with it, check the [Django's documentation](https://docs.djangoproject.com/en/4.1/topics/install/) about it.
2.  Download the project to your computer.
3.  Open the terminal of your OS.
4.  Change to the main project directory where the script is located `manage.py`.
5.  Run `manage.py` with the `migrate` parameter to migrate preset models. Here's what it might look like:
    ```
    py manage.py migrate
    ```
6.  Run `manage.py` with the `runserver` and `--insecure` parameters (to work handlers of 404 and 500 errors). Here's what it might look like: 
    ```
    py manage.py runserver --insecure
    ```
7.  Go to the project website using the link (default: [127.0.0.1:8000](http://127.0.0.1:8000)).
