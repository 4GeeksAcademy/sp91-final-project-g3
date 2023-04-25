import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser} from "../services";

export const Login = props => {


    const [login, setLogin] = useState(
        {
            email: "",
            password: "",
        })

    const navigate = useNavigate()


    const handleChange = ({ target }) => {
        setLogin({ ...login, [target.name]: target.value }) // se setean los cambios en el usestate de Login                                                   
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
       const isLogin =  await loginUser(login)
       if(isLogin) { navigate("/profile")}
    }

    return (
        <React.Fragment>

            <form onChange={handleChange} onSubmit={handleSubmit} id="container-login" className="container">

                <h5 className="text-center">Iniciar Sesión en Jobs Hood</h5>

                <div id="login" className="border border-2 border-dark">
                    <div className="col">
                        <label htmlFor="form-login" className="form-label">Dirección Email</label>
                        <input type="email" name="email" className="form-control rounded-0" placeholder="email@gmail.com" required />
                    </div>
                    <div className="col">
                        <label htmlFor="inputPassword6" className="form-label">Contraseña</label>
                        <input type="password" name="password" className="form-control rounded-0" aria-labelledby="passwordHelpInline" placeholder="Contraseña" required />
                    </div>
                    <input type="submit" value="Iniciar Sesión" className="btn btn-dark mx-3 my-1  rounded-0"></input>
                </div>
            </form>

        </React.Fragment>

    );



};