import React, { useState } from "react";
import "../../styles/signUp.css";
import { Navigate, useNavigate } from "react-router-dom";

export const Home = () => {
	const [showModal, setShowModal] = useState(false);
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const navigate = useNavigate()
	const handleClose = () => setShowModal(false);
	const handleShow = () => setShowModal(true);

	const handleEmailChange = (event) => {
		setEmail(event.target.value);
	};

	const handlePasswordChange = (event) => {
		setPassword(event.target.value);
	};
	const handleConfirmPassword = (event) => {
		setConfirmPassword(event.target.value);
	}

	const handleSubmit = (event) => {
		event.preventDefault();
		if (password !== confirmPassword) {
			alert("La contraseña no coincide");
			return;
		}
		fetch(process.env.BACKEND_URL + "/signup", {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email, password })
		})
			.then(res => res.json())
			.then(data => {
				if (data && data.access_token) {
					sessionStorage.setItem("token", data.access_token)
					handleClose();
					/* navigate("/user"); */
				}
			})
			.catch(error => {
				alert.error('Ha ocurrido un error', error);
			});
	};

	return (
		<div>
			<div>
				<button className="button-sign-up" onClick={handleShow}>Sign Up</button>

				{showModal && (
					<div className="modal">
						<div className="modal-content">
							<span className="close" onClick={handleClose}>&times;</span>
							<p className="modal-p">Sing Up</p>
							<form onSubmit={handleSubmit}>
								<input
									type="email"
									name="email"
									value={email}
									onChange={handleEmailChange}
									placeholder="Email"
								/>
								<input
									type="password"
									name="password"
									value={password}
									onChange={handlePasswordChange}
									placeholder="Contraseña"
								/>
								<input
									type="password"
									name="ConfirPassword"
									value={confirmPassword}
									onChange={handleConfirmPassword}
									placeholder="Confirmar Contraseña"
								/>
								<div>
									<button className="button-input close-button" onClick={handleClose}>Cerrar</button>
									<button
										className="button-input submit"
										type="submit">
										Enviar
									</button>
								</div>
							</form>

						</div>
					</div>
				)}
			</div>
		</div>
	);
};
