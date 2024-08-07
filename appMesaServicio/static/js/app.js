function listarTecnicos(){
    let url='/listarTecnicos'
    fetch(url,{
        method:'GET',
        headers:{
            "content-type":"application/json"
        }
    })

    .then(respuesta => respuesta.json())
    .then(resultado =>{
        
    })
}

function agregarIdCaso(id){
    document.getElementById('idCaso').value=id
}