const removeLinks = document.querySelectorAll(".link-danger") ?? null;
const purchaseForm = document.querySelector("#purchase-form") ?? null;
const emailInput = document.querySelector('input[type="email"]');
if (removeLinks) {
  if (purchaseForm) {
    purchaseForm.querySelector('input').addEventListener("input", () => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (emailRegex.test(emailInput.value)) {
        purchaseForm.querySelector("button").disabled = false;
      } else {
        purchaseForm.querySelector("button").disabled = true;
      }
    });
    purchaseForm.addEventListener("submit", (e) => {
      e.preventDefault();
      fetch("/purchase_paid", {
        method: "PUT",
      }).then((res) => {
        if (res.ok) showEmptyCart();
      });
    });
  }
  removeLinks.forEach((link) => {
    link.addEventListener("click", () => {
      fetch(`/remove_from_cart/${link.dataset.id}`, {
        method: "DELETE",
      }).then(() => {
        link.parentElement.parentElement.parentElement.removeChild(
          link.parentElement.parentElement.parentElement.querySelector(
            `tr[data-id='${link.dataset.id}`
          )
        );

        if (document.querySelectorAll(".link-danger").length === 0) {
          showEmptyCart();
        }
      });
    });
  });
}

function showEmptyCart() {
  document.querySelector("body").removeChild(document.querySelector("main"));
  emptyCart = document.createElement("main");
  emptyCart.setAttribute(
    "class",
    "empty-cart container d-flex flex-column gap-3 justify-content-center align-items-center"
  );
  emptyCart.innerHTML = `
            <img
                src="/static/bookstore/media/images/header/cart.svg"
                alt="Cart"
                class="cart-icon"
            >
            <p class="display-6">Your cart is empty</p>`;
  document
    .querySelector("body")
    .insertBefore(emptyCart, document.querySelector("body>footer"));
}
