export async function getDatosHome()
{
  let respuesta = await fetch(`${import.meta.env.VITE_API_URL}recetas-home`,{headers:
    {'content-type':'aplication/json'}
  });
  const resultado = await respuesta.json();
  return resultado
}

