const dateInput = document.getElementById("date");
const timeInput = document.getElementById("time");
const submitButton = document.querySelector('input[type="submit"]');

function updateTimeMinAttribute() {
  const selectedDate = new Date(dateInput.value);
  const currentDate = new Date();

  if (
    selectedDate.getDate() === currentDate.getDate() &&
    selectedDate.getMonth() === currentDate.getMonth() &&
    selectedDate.getFullYear() === currentDate.getFullYear()
  ) {
    const currentTime = currentDate.toTimeString().slice(0, 5);
    timeInput.setAttribute("min", currentTime);
  } else {
    timeInput.setAttribute("min", "");
  }
}

submitButton.addEventListener("click", (event) => {
  updateTimeMinAttribute();
});
