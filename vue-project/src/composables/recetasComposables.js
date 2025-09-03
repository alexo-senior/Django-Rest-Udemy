import { readonly, ref } from "vue";

export function recetasComposable()

{
  let datos = ref([]);
  let error = ref(null);

  let getDatos = async()=>
  {
    try{
        const res = await fetch(`${import.meta.env.VITE_API_URL}recetas`,
          {headers:{'content-type':'application-json'}});
          datos.value = await res.json();
    } catch (err) {
      error.value=err;

    }

  };
  getDatos();

  return{
    datos:readonly(datos),
    error:readonly(error)
  }

}
