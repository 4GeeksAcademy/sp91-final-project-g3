import React from "react";
import dogpic from "../../img/dog1.jpg";
import { useState } from "react";

const CardOwner = (props) => {
  const [flip, setFlip] = useState(true);

  let imageStyle = {
    backgroundSize: "contain",
    backgroundPosition: "50%",
    objectFit: "cover",
    display: "block",
    width: "400px",
    height: "auto",
    overflow: "hidden",
    aspectRatio: "1",
  };

  return (
    <div className="col">
      <div className="image-flip">
        <div className="mainflip">
          {flip ? (
            <div className="frontside ">
              <div
                className="card"
                style={{ width: "18rem" }}
                onClick={() => setFlip(false)}
              >
                <img
                  className="card-img-top img-fluid"
                  src={dogpic}
                  alt="card image"
                  style={imageStyle}
                />
              </div>
              <div className="row mt-2 m-auto align-center">
                <div className="col-2"></div>
              </div>
            </div>
          ) : (
            <div className="backside">
              <div
                className="card"
                style={{ width: "18rem" }}
                onClick={() => setFlip(true)}
              >
                <div className="card-header"></div>
                <div className="card-body">
                  <h4 className="card-title">Nombre: {props.name}</h4>
                  <h5 className="card-text">Raza: {props.breed}</h5>
                  <h5 className="card-text">Edad: {props.age}</h5>
                  <button className="btn btn-info btn-md">
                    Editar informacion de {props.name}
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
export default CardOwner;
