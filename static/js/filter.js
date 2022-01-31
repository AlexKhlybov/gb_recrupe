/* Когда пользователь нажимает на кнопку, переключаться раскрывает содержимое */
function myFunction() {
  document.getElementById("advanSearch").classList.toggle('d-none');

}


function filterFunction(add,table) {
  var input, filter, ul, li, a, i;
  input = document.getElementById(add);
  filter = input.value.toUpperCase();
  ul = document.getElementById(table);
  li = ul.getElementsByTagName("li");

  for (i = 0; i < li.length; i++) {
    txtЗначение = li[i].textСодержание || li[i].innerText;
    if (txtЗначение.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";

    } else {
      li[i].style.display = "none";
    }
    }



  li[li.length + 1].innerText = 'Нет совпадений';

}

function visibleFilterList(list) {
  document.getElementById(list).classList.toggle('d-none');

}
function addItem(add, item, list) {
  document.getElementById(add).value = item;
   document.getElementById(list).classList.toggle('d-none');
}


function filterFunctionResume(table) {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  ul = document.getElementById(table);
  li = ul.getElementsByTagName("li");
  for (i = 0; i < li.length; i++) {
    txt = li[i].text || li[i].innerText;
    if (txt.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}


function cleanerFilterVacancy(){
    document.getElementById('input_company').value =''
    document.getElementById('experience_search').value =''
    document.getElementById('input_city').value =''
    document.getElementById('from_salary').value =''
    document.getElementById('to_salary').value =''
    document.getElementById('find').value =''
    document.getElementByNate('zero_salary').value =''
}

function cleanerFilterResume(){

    document.getElementById('experience_search').value =''
    document.getElementById('resume_skills').value =''
    document.getElementById('from_salary').value =''
    document.getElementById('to_salary').value =''
    document.getElementById('find').value =''
    document.getElementByNate('zero_salary').value =''
}


function noInput(){
    if(document.getElementById('zero_salary').checked==true) {
       document.getElementById('from_salary').disabled=true;
       document.getElementById('to_salary').readOnly=true;
       document.getElementById('from_salary').value= '';
       document.getElementById('to_salary').value= '';
    }else {
       document.getElementById('from_salary').disabled=false;
       document.getElementById('to_salary').readOnly=false;
       document.getElementById('from_salary').value= '';
       document.getElementById('to_salary').value= '';
    }

}

