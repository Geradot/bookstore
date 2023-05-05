const searchBar = document.getElementById("search-bar");
const bookList = document.getElementById("book-list");
const noResults = document.getElementById("no-results");
const filterPrice = document.getElementById("filter-price");
const filterCategory = document.getElementById("filter-category");

let filteredBooks = [];

// It helps searchBar + filters to work
let allBooks = [...bookList.children];

function filterBooksByCategory(category) {
  if (category === "all") {
    return allBooks;
  } else {
    return allBooks.filter((book) => book.dataset.category === category);
  }
}
function filterBooksByPrice(price) {
  switch (price) {
    case "0-15":
      return allBooks.filter(
        (book) =>
          parseFloat(
            book.querySelector(".card-footer__price span").textContent
          ) < 15
      );
    case "15-25":
      return allBooks.filter(
        (book) =>
          parseFloat(
            book.querySelector(".card-footer__price span").textContent
          ) > 15 &&
          parseFloat(
            book.querySelector(".card-footer__price span").textContent
          ) < 25
      );
    case "25+":
      return allBooks.filter(
        (book) =>
          parseFloat(
            book.querySelector(".card-footer__price span").textContent
          ) > 25
      );
    default:
      return allBooks;
  }
}

function filteredAndSearchedBooks() {
  const searchText = searchBar.value.toLowerCase();
  const filteredBooksByPrice = filterBooksByPrice(filterPrice.value);
  const filteredBooksByCategory = filterBooksByCategory(filterCategory.value);
  const result = filteredBooksByCategory
    .filter((book) => filteredBooksByPrice.includes(book))
    .filter((book) =>
      book
        .querySelector(".card-title")
        .textContent.toLowerCase()
        .includes(searchText.toLowerCase())
    );
  return result;
}

function displayBooks() {
  // filteredBooks = filterBooksByPrice(filterPrice.value);

  const books = filteredAndSearchedBooks();
  bookList.innerHTML = "";
  if (books.length > 0) {
    noResults.style.display = "none";
    books.forEach((card) => {
      bookList.appendChild(card);
    });
  } else noResults.style.display = "flex";
}

filterPrice.addEventListener("change", () => {
  displayBooks();
});

filterCategory.addEventListener("change", () => {
  displayBooks();
})

searchBar.addEventListener("input", () => {
  displayBooks();
});

displayBooks();
