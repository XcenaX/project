function get_current_date(){
    var today = new Date();
    var date = today.getFullYear()+'_'+(today.getMonth()+1)+'_'+today.getDate();
    var time = today.getHours() + "_" + today.getMinutes() + "_" + today.getSeconds() + "_" + today.getMilliseconds();
    var dateTime = date+'_'+time;
    return dateTime;
}

function showElement(id){
    document.getElementById(id).style.display = "block";
}

function hideElement(id){
    document.getElementById(id).style.display = "none";
}



function closeAllFiterBlocks(element){
    blocks = document.getElementsByClassName("filter-block-active");
    console.log(element);
    for(var i = 0; i < blocks.length; i++){
        console.log(blocks[i]);
        if(element !== blocks[i]){
            blocks[i].classList.remove("filter-block-active")
        }        
    }
}

function open_request(element){
    element.parentElement.parentElement.parentElement.classList.toggle("active");
}

function openFilterBlock(element){
    element.children[2].classList.toggle("filter-block-active");
}

$( document ).ready(function() {
   filterBlocks = document.getElementsByClassName("filter-block");
   length = filterBlocks.length;
   for(var i = 0; i < length; i++){
       parent = filterBlocks[i].parentElement;
       parent.addEventListener("click", function(e) {            
            closeAllFiterBlocks(this.children[2]);
            openFilterBlock(this);
        });
   }
});

function delete_cookie(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function switchSettings(element, id){
    if(!element.classList.contains("active")){
        activeItems = document.getElementsByClassName("section active");
        for(var i = 0; i < activeItems.length; i++){
            activeItems[i].classList.remove("active");
        }
        element.classList.add("active");
        if(id == "main_settings"){
            document.getElementById(id).classList.add("active");
            document.getElementById("schedule").classList.remove("active");
        } else{
            document.getElementById(id).classList.add("active");
            document.getElementById("main_settings").classList.remove("active");
        }
    }
}

function openOptions(element){
    element.parentElement.children[3].classList.toggle("active");
}

function openSchedule(element, id){
    activeDay = element.parentElement.getElementsByClassName("day active")[0];
    activeSchedule = element.parentElement.parentElement.getElementsByClassName("schedule active")[0];
    
    activeDay.classList.remove("active");
    activeSchedule.classList.remove("active");

    element.classList.add("active");
    element.parentElement.parentElement.children[1+id].classList.add("active");
}

function maxLengthCheck(object){
    if (object.value.length > object.maxLength){
        object.value = object.value.slice(0, object.maxLength)
    }
}

function createSchedule(element){
    tr = document.createElement("tr");
    htmlString = `
    <td>
        <div class="delete-schedule" title="Удалить расписание" onclick="removeSchedule(this)"></div>
        <input class="time" type="time" name="start_time" value="00:00">
        <span>-</span>
        <input class="time" type="time" name="end_time" value="00:00">
    </td>
    <td class="center text-center">
        <input type="number" class="count" name="count_people" value="0" max="999" min="1" maxlength="3" oninput="maxLengthCheck(this)">
    </td>
    <td class="text-center">
        <input type="number" class="count" name="price" value="0" max="999" min="1" maxlength="3" oninput="maxLengthCheck(this)">
        <span class="price">тг</span>
    </td> 
    `
    tr.innerHTML = htmlString.trim();
    table = element.parentElement.parentElement.parentElement;
    length = table.children.length;
    table.insertBefore(tr, table.children[length-1]);
}

function startLoading(){
    loadBlock = $("#load")[0];
    loadBlock.classList.add("active");
}

function finishLoading(){
    loadBlock = $("#load")[0];
    loadBlock.classList.remove("active");
}

function removeSchedule(element){
    tr = element.parentElement.parentElement;
    tr.remove();
}
function removeReservation(element){
    tr = element.parentElement.parentElement.parentElement;
    tr.remove();
}

function openDeleteNotification(element){
    showElement("delete_notification");
    document.getElementById("delete_button").onclick = function(){
        //нужно будет сделать запрос в апи
        removeSchedule(element);
        hideElement("delete_notification");
    }
}

function acceptReservation(element){
    removeReservation(element);
    //сделать запрос в апи
}

function cancelReservation(element){
    removeReservation(element);
    //сделать запрос в апи
}


function createSection(element){
    schedules = element.parentElement.parentElement.children[1];

    newSchedule = document.createElement("div");
    newSchedule.classList.add("item");

    htmlSchedules = `
    <table class="schedule active">
        <tr>
            <th>Время:</th>
            <th class="center text-center">Кол-во людей:</th>
            <th class="text-center">Цена:</th>
        </tr>                        
        <tr>
            <td>
                <div class="add-schedule" title="Добавить расписание" onclick="createSchedule(this)"></div>                                   
            </td>
            <td class="center text-center">
                
            </td>
            <td class="text-center">
                
            </td>                                    
        </tr>
    </table>`;
    for(var i = 0; i < 6; i++){
        htmlSchedules += `
        <table class="schedule">
            <tr>
                <th>Время:</th>
                <th class="center text-center">Кол-во людей:</th>
                <th class="text-center">Цена:</th>
            </tr>                        
            <tr>
                <td>
                    <div class="add-schedule" title="Добавить расписание" onclick="createSchedule(this)"></div>                                   
                </td>
                <td class="center text-center">
                    
                </td>
                <td class="text-center">
                    
                </td>                                    
            </tr>
        </table>`
    }
    htmlString = `    
        <div class="title-block">
            <div></div>
            <input class="text" value="Бассейн" name="title">
            <div class="options" onclick="openOptions(this)"></div>
            <div class="options-block" onclick="removeSchedule(this)">
                <div class="delete"></div>
                <div class="text">Удалить занятие</div>
            </div>
        </div>
        <div class="days">
            <div class="day active" onclick="openSchedule(this, 1)">Пн</div>
            <div class="day" onclick="openSchedule(this, 2)">Вт</div>
            <div class="day" onclick="openSchedule(this, 3)">Ср</div>
            <div class="day" onclick="openSchedule(this, 4)">Чт</div>
            <div class="day" onclick="openSchedule(this, 5)">Пт</div>
            <div class="day" onclick="openSchedule(this, 6)">Сб</div>
            <div class="day" onclick="openSchedule(this, 7)">Вс</div>
        </div>    
        `+htmlSchedules+`        
        <div class="save">Сохранить</div>`


    newSchedule.innerHTML = htmlString.trim();
    schedules.appendChild(newSchedule);
}

function submitMainPhoto(input){
    alert("Ваше фото сохранено(нет)");
}

function switchPriceType(element, type){
    if(!element.classList.contains("active")){
        element.classList.add("active");
        if(type == "default"){
            element.parentElement.children[1].classList.remove("active");
            element.parentElement.parentElement.children[2].children[0].classList.add("active");
            element.parentElement.parentElement.children[2].children[1].classList.remove("active");
        } else{
            element.parentElement.children[0].classList.remove("active");
            element.parentElement.parentElement.children[2].children[1].classList.add("active");
            element.parentElement.parentElement.children[2].children[0].classList.remove("active");
        }
    }
}

function deletePhoto(element){
    div = element.parentElement.parentElement;
    div.remove();
}

function deleteContact(element){
    element.parentElement.remove();
}

function openExitMenu(element){
    display = element.children[0].style.display;
    if(display === "block"){
        element.children[0].style.display = "none";
    } else{
        element.children[0].style.display = "block";
    }
}

function closeExitMenu(element){
    element.children[0].style.display = "none";
}

function addContact(element){
    contacts = element.parentElement;
    div = document.createElement("div");
    div.classList.add("contact-block");
    htmlString = `
    <input class="item" type="tel" placeholder="+7 000 000 00 00">
    <input class="item" type="email" placeholder="email@mail.ru">
    <div class="delete" onclick="deleteContact(this)"></div>`
    div.innerHTML = htmlString.trim();
    length = contacts.children.length;
    contacts.insertBefore(div, contacts.children[length-1]);
}

 

function sortTable(n, id) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById(id);
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc"; 
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
      //start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /*Loop through all table rows (except the
      first, which contains table headers):*/
      for (i = 1; i < (rows.length - 1); i++) {
        //start by saying there should be no switching:
        shouldSwitch = false;
        /*Get the two elements you want to compare,
        one from current row and one from the next:*/
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        /*check if the two rows should switch place,
        based on the direction, asc or desc:*/
        if (dir == "asc") {
          if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            //if so, mark as a switch and break the loop:
            shouldSwitch= true;
            break;
          }
        } else if (dir == "desc") {
          if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
            //if so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        //Each time a switch is done, increase this count by 1:
        switchcount ++;      
      } else {
        /*If no switching has been done AND the direction is "asc",
        set the direction to "desc" and run the while loop again.*/
        if (switchcount == 0 && dir == "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  }

// $( document ).ready(function() {
//     $('#main_table').DataTable();
// });