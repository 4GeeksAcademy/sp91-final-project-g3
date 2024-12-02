import React, { useState, useContext } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";


const NewFoundPet = () => {
  const navigate = useNavigate();
  const { store, actions } = useContext(Context)

  const [newPetFound, setNewFoundPet] = useState({
    "species": "",
    "breed": "",
    "color": "",
    "gender": "",
    "description": "",
    "photo_1": "",
    "photo_2": "",
    "photo_3": "",
    "photo_4": "",
    "date": "",
    "zone": "",
    "pet_status": "Busco a mi familia"

  });

  function handleChange(e) {
    setNewPet({
      ...newPetFound, [e.target.id]: e.target.value
    })
  }
  console.log(newPetFound);

  
    const handleSubmit = (e) =>{
      e.preventDefault();
      console.log ("enviando post", newPetFound);
      actions.addNewPet(newPetFound);
      navigate("/");
  };
    
  
  return (
    <div className="container col-sm-10, col-md-8, col-lg-6 border rounded pet-form">
      <div className=" container p-2 ">
        <form onSubmit={handleSubmit}>
          
          <div className="mb-3">
            <label htmlForfor="species" className="form-label">ESPECIE</label>
            <select className="form-select" id="species" aria-label="Default select example" onChange={handleChange} >
              <option selected>Selecciona</option>
              <option value="1">Perro</option>
              <option value="2">Gato</option>
              <option value="3">Conejo</option>
              <option value="4">Ave</option>
              <option value="5">Reptil</option>
              <option value="6">otro</option>
            </select>
          </div>
          <div className="mb-3">
            <label htmlForfor="breed" className="form-label">RAZA</label>
            <input type="email" className="form-control" id="breed" placeholder="Ingresa la raza de tu mascota" value={newPetFound.breed} onChange={handleChange} />
          </div>
          <div className="row g-3 mb-3 ">
            <div className="col-md-6">
              <label htmlForfor="gender" className="form-label">GENERO</label>
              <select className="form-select" id="gender" aria-label="Selecionar genero" onChange={handleChange} >
                <option selected>Selecciona</option>
                <option value="male">Macho</option>
                <option value="female">Hembra</option>
                <option value="unknow">No lo sé</option>
              </select>
            </div>
            <div className="col-md-6">
              <label htmlForfor="color" className="form-label">COLOR</label>
              <input type="email" className="form-control" id="color" placeholder="Ingresa el color" value={newPetFound.color} onChange={handleChange} />
            </div>
          </div>
          <div className="mb-3">
            <label htmlForfor="description" className="form-label">DESCRIPCION</label>
            <textarea className="form-control" id="description" rows="3" value={newPetFound.description} onChange={handleChange}></textarea>
          </div>
          <div class="mb-3">
            <label for="formFileMultiple" class="form-label">¿TIENES FOTOS?</label>
            <input class="form-control" type="file" id="formFileMultiple" multiple />
          </div>
          <div className="d-block mb-3">
            <label htmlFor="date" className="form-label ">¿CUANDO LO ENCONTRASTE?</label>
            <input type="date" className="form-control" id="date" value={newPetFound.date} onChange={handleChange} />
          </div>
          <div className="d-block mb-3">
            <label htmlFor="zone" className="form-label">¿DÓNDE LO ENCONTRASTE?</label>
            <input type="text" className="form-control" id="zone" placeholder="Barrio/zona" value={newPetFound.zone} onChange={handleChange} />
          </div>
          <div class="d-grid gap-2 col-6 mx-auto ">
            <button class="btn btn-primary btn-publicar rounded-pill m-2" type="submit">Publicar</button>

          </div>
        </form>
      </div>
    </div >


  )
}

export default NewFoundPet