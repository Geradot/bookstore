const MIN_AMOUNT = 1;
const MAX_AMOUNT = 20;

const bookId = document.querySelector(".specific-book").dataset.id;
const inputField = document.querySelector("#amount");
const minusButton = document.querySelector(".decrement");
const plusButton = document.querySelector(".increment");
const price = parseFloat(document.querySelector(".book-price").textContent);
const totalPriceSpan = document.querySelector(".total-price");
const buttonsBlock = document.querySelector(".specific-book__order_buttons");

// Main buttons
let addToCart = document.querySelector(".add-to-cart") ?? null;
let removeFromCart = document.querySelector(".remove-from-cart") ?? null;
let changeAmount = document.querySelector(".change-amount") ?? null;

// Text about amount in Cart
let textAmountInCart = document.querySelector(".text-amount-in-cart") ?? null;

let value = parseInt(inputField.value);
minusButton.disabled = value === MIN_AMOUNT;
plusButton.disabled = value === MAX_AMOUNT;

function updateValue(newValue) {
  if (newValue <= MIN_AMOUNT) {
    newValue = MIN_AMOUNT;
    minusButton.disabled = true;
    plusButton.disabled = false
  } else if (newValue >= MAX_AMOUNT) {
    newValue = MAX_AMOUNT;
    plusButton.disabled = true;
  } else {
    minusButton.disabled = false;
    plusButton.disabled = false;
  }
  value = newValue;
  if (addToCart) addToCart.disabled = false;
  if (changeAmount) changeAmount.disabled = false;
  inputField.value = value;
  totalPriceSpan.textContent = (value * price).toFixed(2);
}

minusButton.addEventListener("click", () => {
  updateValue(value - 1);
});

plusButton.addEventListener("click", () => {
  updateValue(value + 1);
});

inputField.addEventListener("input", () => {
  console.log(inputField.value);
  const newValue = parseInt(inputField.value);
  if (newValue < MIN_AMOUNT) {
    updateValue(1);
  } else if (newValue > MAX_AMOUNT) {
    updateValue(MAX_AMOUNT);
  } else {
    if (!isNaN(newValue)) {
      updateValue(newValue);
    } else {
      if (addToCart) addToCart.disabled = true;
      if (changeAmount) changeAmount.disabled = true;
      let reg = /[^0-9]/;
      if (!reg.test(inputField.value)) {
        updateValue(1); 
      }
    }
  }
});

buttonsBlock?.addEventListener("click", (e) => {
  if (e.target && e.target.matches("button.add-to-cart")) {
    addItem(e);
  } else if (e.target.matches("button.remove-from-cart")) {
    removeItem(bookId);
    document.querySelector(".amount__text-block").removeChild(textAmountInCart);
    buttonsBlock.removeChild(changeAmount);
    buttonsBlock.removeChild(removeFromCart);
    addToCart = createButton("Add to Cart", "add-to-cart", "success");
    buttonsBlock.appendChild(addToCart);
  } else if (e.target.matches("button.change-amount")) {
    changeAmountItem(e);
  }
});

function addItem() {
  fetch("/add_to_cart", {
    method: "POST",
    body: JSON.stringify({
      bookId: bookId,
      amount: inputField.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      textAmountInCart = document.createElement("span");
      textAmountInCart.setAttribute(
        "class",
        "d-flex my-auto text-amount-in-cart"
      );
      textAmountInCart.innerHTML = `(in cart:&nbsp;<span>${data["amount"]}</span>)`;
      document
        .querySelector(".amount__text-block")
        .appendChild(textAmountInCart);

      removeFromCart = createButton(
        "Remove from Cart",
        "remove-from-cart",
        "danger"
      );
      changeAmount = createButton("Change amount", "change-amount", "success");

      buttonsBlock.removeChild(addToCart);
      buttonsBlock.appendChild(changeAmount);
      buttonsBlock.appendChild(removeFromCart);
    });
} // the end of addItem()

function removeItem(bookId) {
  fetch(`/remove_from_cart/${bookId}`, {
    method: "DELETE",
  }).then(() => {
    updateValue(1);
  });
}

function changeAmountItem() {
  if (textAmountInCart.querySelector("span").textContent != inputField.value)
    fetch(`/change_amount/${bookId}`, {
      method: "PUT",
      body: JSON.stringify({
        amount: inputField.value,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        textAmountInCart.querySelector("span").textContent = data["amount"];
      });
}

/**
 * @param {string} buttonTitle title of Button
 * @param {string} buttonClass main class (for js or another)
 * @param {string} buttonBSClass bootstrap's button class (success, danger, info etc. WITHOUT 'btn-')
 * @returns {object} a custom button
 * @example function("Remove from Cart", "remove-from-cart", "danger")
 */
function createButton(buttonTitle, buttonMainClass, buttonBSClass = "primary") {
  let button = document.createElement("button");
  button.setAttribute("class", buttonMainClass + ` btn btn-${buttonBSClass}`);
  button.textContent = buttonTitle;
  return button;
}
