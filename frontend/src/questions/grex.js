console.log("Hello from grex.js");

// Grab reference to form
const formElem = document.querySelector('form');

// Submit handler
formElem.addEventListener('submit', (event) => {
  // on form submission, prevent default
  event.preventDefault();

  // construct a FormData object, which fires the formdata event
  new FormData(formElem);
});

// formdata handler to retrieve data
formElem.onformdata = (e) => {
  console.log('formdata fired');

  // Get the form data from the event object
  let data = e.formData;
  for (var value of data.values()) {
    console.log(value);
  }

  // TODO submit the data via fetch
};
