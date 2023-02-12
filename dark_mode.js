const checkbox = document.getElementById('checkbox');
var state = false;

checkbox.addEventListener('change', ()=>{
  document.body.classList.toggle('dark');
  state != state;
})

if (state){
  document.body.classList.toggle('dark');
}