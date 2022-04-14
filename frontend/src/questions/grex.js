console.log("Hello from grex.js");

// Submit handler
document.getElementById("grexSubmitButton").onclick = function() {
  console.log("Hello from grex.js onclick!!");
  let grexInput = document.querySelectorAll("#grexForm [name='grexField']").values();
  console.log(grexInput);
}
