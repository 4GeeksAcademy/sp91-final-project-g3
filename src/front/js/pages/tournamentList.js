import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import { TournamentCard } from "../component/tournamentCard.jsx";

export const TournamentList = () => {
    const { store, actions } = useContext(Context);

    useEffect(() => {
        actions.getTournaments();
        actions.getHost();   
    }, []);

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Tournaments</h2>
            <div className="row">
                {store.tournaments.length > 0 ? (
                    store.tournaments.map((tournament) => (
                        <TournamentCard 
                            key={tournament.id}
                            name={tournament.name}
                            img={tournament.image}
                            type={tournament.type}
                            rating={tournament.rating}
                            schedule={tournament.schedule}
                        />
                    ))
                ) : (
                    <p>No tournaments available.</p>
                )}
            </div>
        </div>
    );
};