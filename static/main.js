let currentItem=null;
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken'); 


function getUser()
{
    let url='http://127.0.0.1:8000/api/user';
    fetch(url)
    .then(response=>response.json()).then(function(data){
        document.getElementById("user").innerHTML=data.email;
        document.getElementById("logout").innerHTML="Logout"
        
    }).catch((error)=>{
            console.log(" getUser error");
        });

    buildNotesList();
    
}

function buildNotesList()
{

    let url='http://127.0.0.1:8000/api/notes-list';
    let notesTable=document.getElementById('notes-list');
    notesTable.innerHTML="";
    
    fetch(url)
    .then(response => response.json())
    .then(function(data){
        let list=data;
        for(let i in list)
        {   
            
            let row = `
                    <tr id="note-${list[i].id}">
                        <td  style="border-bottom: 2px solid black;border-top: 2px solid black;text-align: center;font-size:20px; color: black;">
                            ${list[i].title}
                        </td>
                    </tr>  
                    `
            notesTable.innerHTML+=row;


        }

        for(let i in list)
        {
            let getNote=document.getElementById(`note-${list[i].id}`);
            getNote.addEventListener('click', (function(item){
                return function(){
                    clickNote(item)
                }
            })(list[i]))
        }

        }
        ).catch((error)=>{
            console.log("buildNotesList error");
        });

}
function clickNote(item)
{

    document.getElementById('notetitle').value=`${item.title}`;
    document.getElementById('notebody').value=`${item.text}`;
    currentItem=item;
    let editedAt=String(item.date).split(".");
    let timeIndex=editedAt.indexOf('T');
    let getDate=editedAt[0].substring(0,timeIndex-1);
    let getTime=editedAt[0].substring(timeIndex+1);
    document.getElementById('editedat').innerHTML=" Edited at "+editedAt[0].substring(0,editedAt[0].indexOf('T')) + " " + editedAt[0].substring(editedAt[0].indexOf('T')+1);
}

function formSubmit()
{

    url='http://127.0.0.1:8000/api/add-note';
    let method='POST';
    if(currentItem!=null)
    {
        url=`http://127.0.0.1:8000/api/edit-note/${currentItem.id}`;
        method='PUT';
    }

    let title=document.getElementById("notetitle").value;
    let text=document.getElementById("notebody").value;

    let note={
        'title':title,
        'text':text
    };

    
    if(title.length>0 && text.length>0)
    {
        fetch(url, {
            method:method,
            headers:{
                'Content-type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify(note)
        }
        ).then(function(response){
            document.getElementById('noteform').reset();
            buildNotesList();
            currentItem=null;  
            document.getElementById('editedat').innerHTML="";  
        })
    }
     
}

function deleteItem()
{
    let confirmDelete=confirm("Are you sure you want to delete this note ?")
    if(currentItem!=null && confirmDelete)
    {
        let url=`http://127.0.0.1:8000/api/edit-note/${currentItem.id}`;
        fetch(url, {
            method:'DELETE',
            headers:{
                'Content-type':'application/json',
                'X-CSRFToken':csrftoken,
            }
        }
        ).then(function(response){
            document.getElementById('noteform').reset();
            buildNotesList();
            currentItem=null;
            document.getElementById('editedat').innerHTML="";
        })

    }

}
function newNote()
{
    document.getElementById('noteform').reset();
    currentItem=null;
}

