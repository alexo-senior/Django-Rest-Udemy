import { readonly, ref } from "vue";

export function recetasComposable()

{
  let datos = ref([]);
  let error = ref(null);

  let getDatos = async()=>
  {

  };
  return{
    datos:readonly(datos),
    error:readonly(error)
  }

}
