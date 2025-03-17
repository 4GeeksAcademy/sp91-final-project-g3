import React, { useEffect, useContext, useState } from "react";
import { useParams } from "react-router-dom";
import { Context } from "../store/appContext";

export const ArtistProfile = () => {

  const { store, actions } = useContext(Context);
  const { id } = useParams();
  const [artist, setArtist] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchArtist = async () => {
      const artistData = await actions.getArtistById(id);
      if (artistData) {
        setArtist(artistData);
      }
      setLoading(false);
    };
    fetchArtist();
  }, [id]);

  if (loading) {
    return <div className="container py-5 text-center">Cargando...</div>;
  }

  if (!artist) {
    return (
      <div className="container py-5 text-center">
        <h2>Artista no encontrado</h2>
        <p>El artista con ID {id} no existe.</p>
      </div>
    );
  }

  return (
    <div className="container py-5">
      <div className="row">
        <div className="col-md-4 text-center">
          <img
            src={store.usuario.image_url == null ? "https://i.imgur.com/24t1SYU.jpeg" : store.usuario.image_url}
            alt={`Artista ${artist.username}`}
            className="rounded-circle mb-3"
            style={{ width: "200px", height: "200px", objectFit: "cover" }}
          />
          <h2 style={{ color: "#1E3A5F" }}>{artist.username}</h2>
        </div>
        <div className="col-md-8">
          <div>
            <h3 style={{ color: "#1E3A5F" }}>Biografía</h3>
            <p className="lead">
              {artist.biography || "Este artista no tiene una biografía disponible."}
            </p>
          </div>
          <div>
            <h3 style={{ color: "#1E3A5F" }}>Contacto</h3>
            <p className="lead">
              {artist.email || "Este artista no tiene información de contacto disponible."}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};