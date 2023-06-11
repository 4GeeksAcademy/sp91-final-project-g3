import React, { useContext, useState, useEffect } from "react";
import { Link } from "react-router-dom";
import LoginModal from "../pages/loginModal";
import "../../styles/register.css";
import { Context } from "../store/appContext";

export const FoodCard = () => {
    const {store, actions}= useContext(Context);
    function imgError(e){
        e.target.src="https://cdn.leonardo.ai/users/25acf724-d0fb-44e7-8da5-a5932af5eac9/generations/f3918add-a5b5-437e-9bed-186b25ef5636/DreamShaper_v5_3_An_AIpowered_machine_surrounded_by_a_vibr_1.jpg"
    }
    const restaurant = store.restaurantes
    const plates = store.restaurantes.plates

    return(
        <>   
        {store[plates] && store[plates].length > 0 && store[plates].map((element, index) =>{
                                return(
                <div className="col card gradient-custom-contrast"> 
                    <div key={index} className="card-img-top mx-0 p-1 m-1" alt="{item.url}">
                        <img  onError={imgError} className="card-img-top mx-0 p-1 pt-3" alt="restaurantImg"></img>
                        <Link to={`/order-food/${index}`}>
                            <div className="card-body">
                                <h5 className="card-body"><strong>{element.restaurantName}</strong></h5>
                            </div>
                        </Link>
                        <div className="footer card-body ms-auto px-auto">
                                <Link key={index} to={`/${element.restaurantName}/${index}`}>
                                    <div className="row g-3 gap-3">
                                        <button  className="btn btn-outline-primary col fw-bold rounded d-flex align-self-center justify-content-center">
                                            {element.plateName}
                                        </button>
                                        <button className="btn btn-outline-primary col fw-bold rounded d-flex align-self-center justify-content-center">{element.price} Pesos</button>
                                    </div>
                                </Link>
                        </div>
                    </div>
                    </div>
                                )})|| <h1 className="main-title gradient-custom">loading...</h1>}
            </>
    )
};

export default FoodCard;