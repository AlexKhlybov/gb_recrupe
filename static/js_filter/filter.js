/* Когда пользователь нажимает на кнопку, переключаться раскрывает содержимое */
function myFunction() {
  document.getElementById("advanSearch").classList.toggle('d-none');

}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  select = document.getElementById("myDropdown");
  option = select.getElementsByTagName("option");
  for (i = 0; i < option.length; i++) {
    txtЗначение = option[i].textСодержание || option[i].innerText;
    if (txtЗначение.toUpperCase().indexOf(filter) > -1) {
      option[i].style.display = "";
    } else {
      option[i].style.display = "none";
    }
  }
}

function filterFunctionResume() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  ul = document.getElementById("myDropdown");
  li = ul.getElementsByTagName("li");
  for (i = 0; i < li.length; i++) {
    txtЗначение = li[i].textСодержание || li[i].innerText;
    if (txtЗначение.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}